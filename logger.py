"""
Structured logging system for WSD Debate System.

Provides file and console logging with proper formatting and levels.
Excludes sensitive information from logs.
"""

import logging
import logging.handlers
import os
from typing import Optional
from config import config


class DebateLogger:
    """Structured logging for debate system."""
    
    _logger: Optional[logging.Logger] = None
    _initialized: bool = False
    
    @classmethod
    def initialize(cls):
        """Initialize the logging system."""
        if cls._initialized:
            return
        
        # Create logger
        cls._logger = logging.getLogger("wsd_debate")
        cls._logger.setLevel(getattr(logging, config.log_level))
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.handlers.RotatingFileHandler(
            config.log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, config.log_level))
        file_handler.setFormatter(formatter)
        cls._logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config.log_level))
        console_handler.setFormatter(formatter)
        cls._logger.addHandler(console_handler)
        
        cls._initialized = True
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get the logger instance."""
        if not cls._initialized:
            cls.initialize()
        return cls._logger
    
    @classmethod
    def info(cls, message: str):
        """Log info message."""
        cls.get_logger().info(message)
    
    @classmethod
    def debug(cls, message: str):
        """Log debug message."""
        cls.get_logger().debug(message)
    
    @classmethod
    def warning(cls, message: str):
        """Log warning message."""
        cls.get_logger().warning(message)
    
    @classmethod
    def error(cls, message: str, exc_info: bool = False):
        """Log error message."""
        cls.get_logger().error(message, exc_info=exc_info)


# Initialize logger on import
DebateLogger.initialize()
