"""
Purrify Core Module

This module contains the core functionality for the Purrify system optimization utility.
It provides platform-agnostic interfaces and base classes for all Purrify modules.
"""

__version__ = "2.0.0"
__author__ = "Purrify Team"
__description__ = "Core functionality for Purrify system optimization utility"

from .engine import PurrifyEngine
from .scanner import BaseScanner
from .cleaner import BaseCleaner
from .optimizer import BaseOptimizer
from .config import CoreConfig
from .logger import setup_logger

# Core models
from .models.scan_result import ScanResult
from .models.clean_result import CleanResult
from .models.opt_result import OptimizationResult

# Core utilities
from .utils.file_utils import FileUtils
from .utils.hash_utils import HashUtils
from .utils.format_utils import FormatUtils
from .utils.validation import ValidationUtils

__all__ = [
    # Core classes
    "PurrifyEngine",
    "BaseScanner", 
    "BaseCleaner",
    "BaseOptimizer",
    "CoreConfig",
    "setup_logger",
    
    # Models
    "ScanResult",
    "CleanResult", 
    "OptimizationResult",
    
    # Utilities
    "FileUtils",
    "HashUtils",
    "FormatUtils",
    "ValidationUtils",
    
    # Version info
    "__version__",
    "__author__",
    "__description__"
] 