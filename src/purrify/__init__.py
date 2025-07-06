"""
Purrify - AI-Driven System Optimization Utility

A cross-platform system optimization tool that uses AI to clean caches,
optimize files, and improve system performance on macOS and Windows.
"""

__version__ = "2.0.0"
__author__ = "Purrify Team"
__email__ = "team@purrify.app"
__description__ = "AI-Driven System Optimization Utility for macOS and Windows"

# Core imports
from .core.engine import PurrifyEngine
from .core.config import Config
from .core.logger import setup_logger

# Main application entry point
def main():
    """Main entry point for the Purrify application."""
    from .main import main as app_main
    return app_main()

# Version info
__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "PurrifyEngine",
    "Config",
    "setup_logger",
    "main",
] 