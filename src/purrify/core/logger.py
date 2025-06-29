"""
Purrify Logging Configuration

This module provides centralized logging configuration for the Purrify
system optimization utility with structured logging and different log levels.
"""

import sys
import os
from pathlib import Path
from typing import Optional
from loguru import logger


def setup_logger(
    verbose: bool = False,
    log_file: Optional[str] = None,
    log_level: str = "INFO"
) -> None:
    """
    Setup logging configuration for Purrify.
    
    Args:
        verbose: Enable verbose logging
        log_file: Path to log file (optional)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Remove default logger
    logger.remove()
    
    # Determine log level
    if verbose:
        log_level = "DEBUG"
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        # Default log file location
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        log_file = str(logs_dir / "purrify.log")
    
    # Console logging format
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # File logging format (more detailed)
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=console_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler
    logger.add(
        log_file,
        format=file_format,
        level="DEBUG",  # Always log everything to file
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # Add error file handler
    error_log_file = str(Path(log_file).parent / "purrify_errors.log")
    logger.add(
        error_log_file,
        format=file_format,
        level="ERROR",
        rotation="5 MB",
        retention="90 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Logging system initialized")
    logger.info(f"Log level: {log_level}")
    logger.info(f"Log file: {log_file}")
    logger.info(f"Error log file: {error_log_file}")


def get_logger(name: str = "purrify"):
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


class PurrifyLogger:
    """
    Custom logger class for Purrify with additional functionality.
    """
    
    def __init__(self, name: str = "purrify"):
        """
        Initialize the Purrify logger.
        
        Args:
            name: Logger name
        """
        self.logger = get_logger(name)
        self.name = name
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, **kwargs)
    
    def success(self, message: str, **kwargs):
        """Log success message."""
        self.logger.success(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(message, **kwargs)
    
    def bind(self, **kwargs):
        """Bind additional context to logger."""
        return self.logger.bind(**kwargs)
    
    def log_operation(self, operation: str, status: str, details: dict = None):
        """
        Log operation with structured data.
        
        Args:
            operation: Operation name
            status: Operation status (started, completed, failed)
            details: Additional operation details
        """
        log_data = {
            "operation": operation,
            "status": status,
            "logger": self.name
        }
        
        if details:
            log_data.update(details)
        
        if status == "started":
            self.info(f"Operation started: {operation}", **log_data)
        elif status == "completed":
            self.success(f"Operation completed: {operation}", **log_data)
        elif status == "failed":
            self.error(f"Operation failed: {operation}", **log_data)
        else:
            self.info(f"Operation {status}: {operation}", **log_data)
    
    def log_performance(self, operation: str, duration: float, metrics: dict = None):
        """
        Log performance metrics.
        
        Args:
            operation: Operation name
            duration: Operation duration in seconds
            metrics: Additional performance metrics
        """
        log_data = {
            "operation": operation,
            "duration": duration,
            "logger": self.name
        }
        
        if metrics:
            log_data.update(metrics)
        
        self.info(f"Performance: {operation} took {duration:.2f}s", **log_data)
    
    def log_system_event(self, event_type: str, description: str, data: dict = None):
        """
        Log system events.
        
        Args:
            event_type: Type of system event
            description: Event description
            data: Additional event data
        """
        log_data = {
            "event_type": event_type,
            "description": description,
            "logger": self.name
        }
        
        if data:
            log_data.update(data)
        
        self.info(f"System event: {event_type} - {description}", **log_data)


# Global logger instance
purrify_logger = PurrifyLogger()


def log_function_call(func):
    """
    Decorator to log function calls.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger_name = f"{func.__module__}.{func.__name__}"
        func_logger = PurrifyLogger(logger_name)
        
        func_logger.log_operation(
            operation=func.__name__,
            status="started",
            details={
                "args_count": len(args),
                "kwargs_count": len(kwargs)
            }
        )
        
        try:
            result = func(*args, **kwargs)
            func_logger.log_operation(
                operation=func.__name__,
                status="completed"
            )
            return result
        except Exception as e:
            func_logger.log_operation(
                operation=func.__name__,
                status="failed",
                details={"error": str(e)}
            )
            raise
    
    return wrapper


def log_async_function_call(func):
    """
    Decorator to log async function calls.
    
    Args:
        func: Async function to decorate
        
    Returns:
        Decorated async function
    """
    async def wrapper(*args, **kwargs):
        logger_name = f"{func.__module__}.{func.__name__}"
        func_logger = PurrifyLogger(logger_name)
        
        func_logger.log_operation(
            operation=func.__name__,
            status="started",
            details={
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "async": True
            }
        )
        
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            func_logger.log_operation(
                operation=func.__name__,
                status="completed"
            )
            
            func_logger.log_performance(
                operation=func.__name__,
                duration=duration
            )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            func_logger.log_operation(
                operation=func.__name__,
                status="failed",
                details={"error": str(e)}
            )
            
            func_logger.log_performance(
                operation=func.__name__,
                duration=duration
            )
            
            raise
    
    return wrapper


# Import time module for async decorator
import time 