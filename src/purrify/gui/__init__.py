"""
Purrify GUI Module

This module provides a beautiful, fluid GUI interface for the Purrify
system optimization utility with Aphrodite-inspired aesthetics.

The GUI module includes:
- Main application window with fluid animations
- Aphrodite-inspired theme system
- Custom widgets with beautiful styling
- Real-time system monitoring and optimization
- Cross-platform compatibility

Author: Purrify Team
Version: 2.0.0
License: MIT
"""

from .main_window import PurrifyGUI
from .styles import AphroditeTheme
from .animations import FluidAnimations
from .widgets import (
    AphroditeButton,
    AphroditeCard,
    AphroditeProgressBar,
    AphroditeStatusCard,
    AphroditeAnimatedCanvas,
    AphroditeMenuBar
)

__all__ = [
    'PurrifyGUI',
    'AphroditeTheme', 
    'FluidAnimations',
    'AphroditeButton',
    'AphroditeCard',
    'AphroditeProgressBar',
    'AphroditeStatusCard',
    'AphroditeAnimatedCanvas',
    'AphroditeMenuBar'
] 