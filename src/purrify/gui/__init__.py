"""
Purrify GUI Module

This module provides a beautiful, fluid GUI interface for the Purrify
system optimization utility with Aphrodite-inspired aesthetics.
"""

from .main_window import PurrifyGUI
from .styles import AphroditeTheme
from .animations import FluidAnimations
from .widgets import *

__all__ = [
    'PurrifyGUI',
    'AphroditeTheme', 
    'FluidAnimations'
] 