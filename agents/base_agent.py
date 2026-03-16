"""
Base agent class for WSD Debate System.

Provides abstract base class for all specialized agents.
Includes caching, retry logic, and rate limiting.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import hashlib
import asyncio
from datetime import datetime, timedelta
from logger import DebateLogger
from models import SideCase, AgentResponse
from config import config


class LLMCache:
    """Simple in-memory cache for LLM responses."""
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache.
        
        Args:
            ttl_seconds: Time to live for cached items (default 1 hour)
        """
        self._cache: Dict[str, tuple[str, datetime]] = {}
        self.ttl_seconds = ttl_seconds
    
    def _hash_prompt(self, prompt: str) -> str:
        """Generate hash key for prompt."""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def get(self, prompt: str) -> Optional[str]:
        """Get cached response if available and not expired."""
        key = self._hash_prompt(prompt)
        if key in self._cache:
            response, timestamp = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
                return response
            else:
                del self._cache[key]  # Remove expired item
        return None
    
    def set(self, prompt: str, response: str) -> None:
        """Cache a response."""
        key = self._hash_prompt(prompt)
        self._cache[key] = (response, datetime.now())
    
    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum calls allowed per window
            window_seconds: Time window in seconds
        """
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._call_times: list = []
    
    async def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        # Remove old calls outside the window
        self._call_times = [t for t in self._call_times if t > cutoff]
        
        if len(self._call_times) >= self.max_calls:
            # Wait until oldest call exits the window
            wait_time = (self._call_times[0] - cutoff).total_seconds() + 0.1
            await asyncio.sleep(wait_time)
            self._call_times.pop(0)
        
        self._call_times.append(datetime.now())


class DebateAgent(ABC):
    """Abstract base class for all debate agents."""
    
    # Class-level cache and rate limiter (shared across instances)
    _cache = LLMCache()
    _rate_limiter = RateLimiter(max_calls=10, window_seconds=60)
    
    def __init__(self, name: str, model: str = None, use_cache: bool = True):
        """
        Initialize agent.
        
        Args:
            name: Agent name
            model: LLM model to use (defaults to config.groq_model)
            use_cache: Enable caching for LLM responses
        """
        self.name = name
        self.model = model or config.groq_model
        self.logger = DebateLogger
        self.use_cache = use_cache
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute agent task.
        
        Args:
            **kwargs: Task-specific arguments
            
        Returns:
            Dictionary with results
        """
        pass
    
    def _create_response(
        self,
        task: str,
        result: Dict[str, Any],
        execution_time_ms: Optional[int] = None
    ) -> AgentResponse:
        """
        Create a standardized response.
        
        Args:
            task: Task description
            result: Task results
            execution_time_ms: Execution time in milliseconds
            
        Returns:
            AgentResponse object
        """
        return AgentResponse(
            agent_name=self.name,
            task=task,
            result=result,
            execution_time_ms=execution_time_ms
        )
    
    async def _call_llm(self, prompt: str, max_retries: int = 3) -> str:
        """
        Call the Groq LLM API with caching, retry logic, and rate limiting.
        
        Args:
            prompt: Prompt to send to LLM
            max_retries: Maximum number of retry attempts
            
        Returns:
            LLM response text
            
        Raises:
            ValueError: If prompt is empty
            Exception: If all retry attempts fail
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Check cache first
        if self.use_cache:
            cached_response = self._cache.get(prompt)
            if cached_response:
                self.logger.debug(f"{self.name}: Using cached response for prompt")
                return cached_response
        
        # Implement retry logic with exponential backoff
        last_exception = None
        for attempt in range(max_retries):
            try:
                # Apply rate limiting
                await self._rate_limiter.wait_if_needed()
                
                from groq import Groq
                
                client = Groq(api_key=config.groq_api_key)
                message = client.chat.completions.create(
                    model=config.groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.groq_temperature,
                    max_tokens=config.groq_max_tokens,
                )
                response = message.choices[0].message.content
                
                # Cache the response
                if self.use_cache:
                    self._cache.set(prompt, response)
                
                return response
                
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    # Calculate exponential backoff: 1s, 2s, 4s...
                    wait_time = 2 ** attempt
                    self.logger.warning(
                        f"{self.name}: LLM call failed (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {wait_time}s: {str(e)}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    self.logger.error(
                        f"{self.name}: LLM call failed after {max_retries} attempts: {str(e)}",
                        exc_info=True
                    )
        
        raise last_exception or Exception("LLM call failed after all retry attempts")
    
    def _log_start(self, task: str):
        """Log task start."""
        self.logger.info(f"{self.name}: Starting {task}")
    
    def _log_end(self, task: str, duration_ms: int = 0):
        """Log task end."""
        if duration_ms:
            self.logger.info(f"{self.name}: Completed {task} in {duration_ms}ms")
        else:
            self.logger.info(f"{self.name}: Completed {task}")
    
    def _log_error(self, task: str, error: str):
        """Log task error."""
        self.logger.error(f"{self.name}: Error in {task}: {error}")
    
    def _validate_prompt_input(self, motion: str, side_name: str = None) -> None:
        """
        Validate essential prompt inputs.
        
        Args:
            motion: The debate motion
            side_name: The side name (Optional)
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not motion or not motion.strip():
            raise ValueError("Motion cannot be empty or whitespace only")
        
        if len(motion) < 10:
            raise ValueError("Motion must be at least 10 characters long")
        
        if len(motion) > 2000:
            raise ValueError("Motion must be less than 2000 characters")
        
        if side_name and side_name not in ["Proposition", "Opposition"]:
            raise ValueError(f"Invalid side: {side_name}. Must be 'Proposition' or 'Opposition'")
    
    def _validate_team_members(self, members: list) -> None:
        """
        Validate team members list.
        
        Args:
            members: List of team member names
            
        Raises:
            ValueError: If team members list is invalid
        """
        if not members or len(members) == 0:
            raise ValueError("Team must have at least one member")
        
        if len(members) > 10:
            raise ValueError("Team cannot have more than 10 members")
        
        for member in members:
            if not member or not member.strip():
                raise ValueError("Team member names cannot be empty")
            
            if len(member) > 100:
                raise ValueError(f"Team member name too long: {member}")
