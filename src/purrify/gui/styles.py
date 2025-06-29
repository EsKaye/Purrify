"""
Aphrodite-Inspired Theme for Purrify GUI

This module defines the beautiful, flowing aesthetic inspired by
Aphrodite - goddess of love, beauty, and cleansing waters.
"""

from dataclasses import dataclass
from typing import Dict, Any
import tkinter as tk
from tkinter import ttk
import json

@dataclass
class AphroditeColors:
    """Aphrodite-inspired color palette."""
    
    # Primary colors - flowing waters and rose petals
    primary_rose: str = "#FF6B9D"      # Soft rose pink
    primary_pearl: str = "#F8F9FA"     # Pearl white
    primary_azure: str = "#4ECDC4"     # Azure blue-green
    primary_lavender: str = "#A8A4CE"  # Soft lavender
    
    # Secondary colors - golden sunlight and sea foam
    secondary_gold: str = "#FFD93D"    # Golden sunlight
    secondary_foam: str = "#E8F4FD"    # Sea foam
    secondary_coral: str = "#FF8A80"   # Coral accent
    secondary_sage: str = "#95D5B2"    # Sage green
    
    # Background colors - ethereal and flowing
    bg_primary: str = "#FAFBFF"        # Pure white with blue tint
    bg_secondary: str = "#F0F4FF"      # Soft blue-white
    bg_accent: str = "#E8F2FF"         # Light blue accent
    bg_dark: str = "#2C3E50"           # Deep blue-gray
    
    # Text colors
    text_primary: str = "#2C3E50"      # Dark blue-gray
    text_secondary: str = "#7F8C8D"    # Medium gray
    text_light: str = "#BDC3C7"        # Light gray
    text_white: str = "#FFFFFF"        # Pure white
    
    # Status colors
    success: str = "#27AE60"           # Emerald green
    warning: str = "#F39C12"           # Orange
    error: str = "#E74C3C"             # Red
    info: str = "#3498DB"              # Blue
    
    # Gradient colors
    gradient_start: str = "#FF6B9D"    # Rose
    gradient_middle: str = "#4ECDC4"   # Azure
    gradient_end: str = "#A8A4CE"      # Lavender

class AphroditeTheme:
    """Aphrodite-inspired theme for Purrify GUI."""
    
    def __init__(self):
        self.colors = AphroditeColors()
        self.fonts = self._setup_fonts()
        self.styles = self._setup_styles()
    
    def _setup_fonts(self) -> Dict[str, Any]:
        """Setup beautiful fonts for the interface."""
        return {
            'title': ('Helvetica Neue', 24, 'bold'),
            'heading': ('Helvetica Neue', 18, 'bold'),
            'subheading': ('Helvetica Neue', 14, 'bold'),
            'body': ('Helvetica Neue', 12, 'normal'),
            'body_small': ('Helvetica Neue', 10, 'normal'),
            'button': ('Helvetica Neue', 12, 'bold'),
            'caption': ('Helvetica Neue', 9, 'normal'),
        }
    
    def _setup_styles(self) -> Dict[str, Any]:
        """Setup ttk styles for the interface."""
        return {
            'main_frame': {
                'background': self.colors.bg_primary,
                'relief': 'flat',
                'borderwidth': 0
            },
            'card_frame': {
                'background': self.colors.bg_secondary,
                'relief': 'flat',
                'borderwidth': 1,
                'highlightthickness': 1,
                'highlightbackground': self.colors.primary_lavender,
                'highlightcolor': self.colors.primary_azure
            },
            'button_primary': {
                'background': self.colors.primary_rose,
                'foreground': self.colors.text_white,
                'font': self.fonts['button'],
                'relief': 'flat',
                'borderwidth': 0,
                'padx': 20,
                'pady': 10,
                'cursor': 'hand2'
            },
            'button_secondary': {
                'background': self.colors.primary_azure,
                'foreground': self.colors.text_white,
                'font': self.fonts['button'],
                'relief': 'flat',
                'borderwidth': 0,
                'padx': 20,
                'pady': 10,
                'cursor': 'hand2'
            },
            'button_ghost': {
                'background': 'transparent',
                'foreground': self.colors.primary_rose,
                'font': self.fonts['button'],
                'relief': 'flat',
                'borderwidth': 1,
                'highlightthickness': 1,
                'highlightbackground': self.colors.primary_rose,
                'padx': 20,
                'pady': 10,
                'cursor': 'hand2'
            },
            'label_title': {
                'background': 'transparent',
                'foreground': self.colors.text_primary,
                'font': self.fonts['title'],
                'justify': 'center'
            },
            'label_heading': {
                'background': 'transparent',
                'foreground': self.colors.text_primary,
                'font': self.fonts['heading'],
                'justify': 'left'
            },
            'label_body': {
                'background': 'transparent',
                'foreground': self.colors.text_secondary,
                'font': self.fonts['body'],
                'justify': 'left'
            },
            'progress_bar': {
                'background': self.colors.bg_accent,
                'troughcolor': self.colors.bg_secondary,
                'borderwidth': 0,
                'relief': 'flat'
            }
        }
    
    def apply_theme(self, root: tk.Tk):
        """Apply the Aphrodite theme to the root window."""
        root.configure(bg=self.colors.bg_primary)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure common styles
        style.configure('TFrame', background=self.colors.bg_primary)
        style.configure('TLabel', background=self.colors.bg_primary, foreground=self.colors.text_primary)
        style.configure('TButton', 
                       background=self.colors.primary_rose,
                       foreground=self.colors.text_white,
                       font=self.fonts['button'],
                       borderwidth=0,
                       focuscolor='none')
        
        # Configure progress bar
        style.configure('Aphrodite.Horizontal.TProgressbar',
                       background=self.colors.primary_rose,
                       troughcolor=self.colors.bg_secondary,
                       borderwidth=0,
                       lightcolor=self.colors.primary_rose,
                       darkcolor=self.colors.primary_rose)
        
        # Configure entry
        style.configure('TEntry',
                       fieldbackground=self.colors.bg_secondary,
                       foreground=self.colors.text_primary,
                       borderwidth=1,
                       relief='flat')
        
        # Configure treeview
        style.configure('Treeview',
                       background=self.colors.bg_secondary,
                       foreground=self.colors.text_primary,
                       fieldbackground=self.colors.bg_secondary,
                       borderwidth=0)
        
        style.configure('Treeview.Heading',
                       background=self.colors.primary_lavender,
                       foreground=self.colors.text_white,
                       borderwidth=0)
    
    def get_gradient_colors(self) -> list:
        """Get gradient colors for animations."""
        return [
            self.colors.gradient_start,
            self.colors.gradient_middle,
            self.colors.gradient_end
        ]
    
    def get_animation_colors(self) -> Dict[str, str]:
        """Get colors for specific animations."""
        return {
            'scanning': self.colors.primary_azure,
            'cleaning': self.colors.primary_rose,
            'optimizing': self.colors.secondary_gold,
            'success': self.colors.success,
            'warning': self.colors.warning,
            'error': self.colors.error
        } 