"""
Base agent class for WSD Debate System.

Provides abstract base class for all specialized agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
from logger import DebateLogger
from models import SideCase, AgentResponse
from config import config


class DebateAgent(ABC):
    """Abstract base class for all debate agents."""
    
    def __init__(self, name: str, model: str = None):
        """
        Initialize agent.
        
        Args:
            name: Agent name
            model: LLM model to use (defaults to config.groq_model)
        """
        self.name = name
        self.model = model or config.groq_model
        self.logger = DebateLogger
    
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
    
    async def _call_llm(self, prompt: str) -> str:
        """
        Call the Groq LLM API.
        
        Args:
            prompt: Prompt to send to LLM
            
        Returns:
            LLM response text
        """
        try:
            from groq import Groq
            
            client = Groq(api_key=config.groq_api_key)
            message = client.chat.completions.create(
                model=config.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.groq_temperature,
                max_tokens=config.groq_max_tokens,
            )
            return message.choices[0].message.content
        except Exception as e:
            self.logger.error(f"LLM call failed in {self.name}: {str(e)}", exc_info=True)
            raise
    
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
