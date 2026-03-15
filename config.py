"""
Configuration management for WSD Debate System.

Handles environment variables, API keys, and system settings.
Supports environment-based configuration with sensible defaults.
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        load_dotenv()
        
        # API Configuration
        self.groq_api_key: str = os.getenv("GROQ_API_KEY", "")
        self.groq_model: str = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
        self.groq_temperature: float = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
        self.groq_max_tokens: int = int(os.getenv("GROQ_MAX_TOKENS", "8192"))
        
        # Debate Configuration
        self.default_num_arguments: int = int(os.getenv("DEFAULT_NUM_ARGUMENTS", "3"))
        self.default_num_rebuttals: int = int(os.getenv("DEFAULT_NUM_REBUTTALS", "3"))
        
        # Logging Configuration
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_file: str = os.getenv("LOG_FILE", "logs/wsd_debate.log")
        self.debug_mode: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
        
        # Execution Configuration
        self.timeout_seconds: int = int(os.getenv("TIMEOUT_SECONDS", "300"))
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
        self.parallel_execution: bool = os.getenv("PARALLEL_EXECUTION", "true").lower() == "true"
    
    def validate(self) -> bool:
        """Validate critical configuration."""
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        return True
    
    def to_dict(self) -> dict:
        """Return configuration as dictionary."""
        return {
            "groq_api_key": "[REDACTED]",  # Don't expose in logs
            "groq_model": self.groq_model,
            "groq_temperature": self.groq_temperature,
            "groq_max_tokens": self.groq_max_tokens,
            "default_num_arguments": self.default_num_arguments,
            "default_num_rebuttals": self.default_num_rebuttals,
            "log_level": self.log_level,
            "debug_mode": self.debug_mode,
            "parallel_execution": self.parallel_execution,
        }


# Global config instance
config = Config()
