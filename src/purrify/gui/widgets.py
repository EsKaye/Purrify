"""
Custom Widgets for Purrify GUI

This module provides beautiful, custom widgets with Aphrodite-inspired
design and fluid animations.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict, Any
from .styles import AphroditeTheme
from .animations import FluidAnimations, ProgressAnimation

class AphroditeButton(tk.Button):
    """Beautiful button with Aphrodite-inspired design."""
    
    def __init__(self, parent, text: str, command: Callable = None, 
                 style: str = "primary", **kwargs):
        self.theme = AphroditeTheme()
        self.style = style
        
        # Get button style
        button_style = self.theme.styles[f'button_{style}']
        
        super().__init__(
            parent,
            text=text,
            command=command,
            **button_style,
            **kwargs
        )
        
        # Bind hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    
    def _on_enter(self, event):
        """Handle mouse enter event."""
        if self.style == "primary":
            self.configure(background=self.theme.colors.primary_lavender)
        elif self.style == "secondary":
            self.configure(background=self.theme.colors.secondary_sage)
        else:  # ghost
            self.configure(background=self.theme.colors.primary_rose, 
                          foreground=self.theme.colors.text_white)
    
    def _on_leave(self, event):
        """Handle mouse leave event."""
        if self.style == "primary":
            self.configure(background=self.theme.colors.primary_rose)
        elif self.style == "secondary":
            self.configure(background=self.theme.colors.primary_azure)
        else:  # ghost
            self.configure(background="transparent", 
                          foreground=self.theme.colors.primary_rose)
    
    def _on_click(self, event):
        """Handle click event with ripple effect."""
        # Create ripple effect
        x, y = event.x, event.y
        canvas = tk.Canvas(self, width=self.winfo_width(), height=self.winfo_height(),
                          bg="transparent", highlightthickness=0)
        canvas.place(x=0, y=0)
        
        # Animate ripple
        self._animate_ripple(canvas, x, y)
    
    def _animate_ripple(self, canvas: tk.Canvas, x: int, y: int):
        """Animate ripple effect on button click."""
        radius = 0
        max_radius = max(self.winfo_width(), self.winfo_height())
        
        def animate():
            nonlocal radius
            if radius < max_radius:
                canvas.delete("ripple")
                alpha = 1.0 - (radius / max_radius)
                # Create a simple color adjustment for the ripple effect
                color = self._adjust_color_alpha_simple(self.theme.colors.primary_pearl, alpha)
                
                canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    outline=color,
                    width=2,
                    tags="ripple"
                )
                
                radius += 5
                canvas.after(20, animate)
            else:
                canvas.destroy()
        
        animate()
    
    def _adjust_color_alpha_simple(self, color: str, alpha: float) -> str:
        """Simple color alpha adjustment for button ripples."""
        # Convert hex to RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Apply alpha
        r = int(r * alpha)
        g = int(g * alpha)
        b = int(b * alpha)
        
        return f"#{r:02x}{g:02x}{b:02x}"

class AphroditeCard(tk.Frame):
    """Beautiful card widget with rounded corners and shadow."""
    
    def __init__(self, parent, title: str = "", **kwargs):
        self.theme = AphroditeTheme()
        
        super().__init__(
            parent,
            **self.theme.styles['card_frame'],
            **kwargs
        )
        
        self.title_label = None
        if title:
            self.title_label = tk.Label(
                self,
                text=title,
                **self.theme.styles['label_heading']
            )
            self.title_label.pack(pady=(10, 5), padx=10, anchor="w")
    
    def add_widget(self, widget, **pack_options):
        """Add a widget to the card."""
        widget.pack(padx=10, pady=5, fill="x", **pack_options)

class AphroditeProgressBar(tk.Frame):
    """Beautiful animated progress bar."""
    
    def __init__(self, parent, **kwargs):
        self.theme = AphroditeTheme()
        
        super().__init__(parent, **kwargs)
        
        # Create canvas for progress bar
        self.canvas = tk.Canvas(
            self,
            height=30,
            bg=self.theme.colors.bg_secondary,
            highlightthickness=0
        )
        self.canvas.pack(fill="x", padx=10, pady=5)
        
        # Progress animation
        self.progress_anim = ProgressAnimation(self.canvas, self.theme)
        
        # Progress text
        self.progress_text = tk.Label(
            self,
            text="0%",
            **self.theme.styles['label_body']
        )
        self.progress_text.pack(pady=(0, 5))
        
        # Bind resize event
        self.canvas.bind("<Configure>", self._on_resize)
    
    def set_progress(self, value: float, animate: bool = True):
        """Set progress value (0.0 to 1.0)."""
        if animate:
            self.progress_anim.animate_progress(value)
        else:
            self.progress_anim.progress = value
            self.progress_anim._draw_progress()
        
        # Update text
        percentage = int(value * 100)
        self.progress_text.configure(text=f"{percentage}%")
    
    def _on_resize(self, event):
        """Handle canvas resize."""
        self.progress_anim._draw_progress()

class AphroditeStatusCard(tk.Frame):
    """Status card with beautiful icons and animations."""
    
    def __init__(self, parent, title: str, value: str, icon: str = "✨", 
                 status: str = "normal", **kwargs):
        self.theme = AphroditeTheme()
        
        super().__init__(
            parent,
            **self.theme.styles['card_frame'],
            **kwargs
        )
        
        # Icon and title
        icon_label = tk.Label(
            self,
            text=icon,
            font=("Arial", 24),
            bg="transparent",
            fg=self.theme.colors.primary_rose
        )
        icon_label.pack(pady=(10, 5))
        
        title_label = tk.Label(
            self,
            text=title,
            **self.theme.styles['label_body']
        )
        title_label.pack(pady=(0, 5))
        
        # Value
        self.value_label = tk.Label(
            self,
            text=value,
            **self.theme.styles['label_heading']
        )
        self.value_label.pack(pady=(0, 10))
        
        # Status indicator
        self.status_colors = {
            'success': self.theme.colors.success,
            'warning': self.theme.colors.warning,
            'error': self.theme.colors.error,
            'normal': self.theme.colors.primary_azure
        }
        
        self.status_indicator = tk.Frame(
            self,
            width=10,
            height=10,
            bg=self.status_colors.get(status, self.theme.colors.primary_azure)
        )
        self.status_indicator.pack(pady=(0, 10))
    
    def update_value(self, value: str):
        """Update the value display."""
        self.value_label.configure(text=value)
    
    def update_status(self, status: str):
        """Update the status indicator."""
        color = self.status_colors.get(status, self.theme.colors.primary_azure)
        self.status_indicator.configure(bg=color)

class AphroditeAnimatedCanvas(tk.Canvas):
    """Canvas with built-in fluid animations."""
    
    def __init__(self, parent, **kwargs):
        self.theme = AphroditeTheme()
        
        super().__init__(
            parent,
            bg=self.theme.colors.bg_primary,
            highlightthickness=0,
            **kwargs
        )
        
        # Initialize animations
        self.animations = FluidAnimations(self, self.theme)
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", self._on_resize)
    
    def start_water_flow(self):
        """Start water flow animation."""
        self.animations.start_water_flow()
    
    def start_cleansing_waves(self):
        """Start cleansing waves animation."""
        self.animations.start_cleansing_waves()
    
    def start_gradient_flow(self):
        """Start gradient flow animation."""
        self.animations.start_gradient_flow()
    
    def stop_animations(self):
        """Stop all animations."""
        self.animations.stop_animations()
    
    def _on_click(self, event):
        """Handle canvas click with ripple effect."""
        self.animations.start_ripple_effect(event.x, event.y)
    
    def _on_resize(self, event):
        """Handle canvas resize."""
        # Redraw background
        self.delete("background")
        self.create_rectangle(
            0, 0, event.width, event.height,
            fill=self.theme.colors.bg_primary,
            outline="",
            tags="background"
        )

class AphroditeMenuBar(tk.Frame):
    """Beautiful menu bar with Aphrodite design."""
    
    def __init__(self, parent, **kwargs):
        self.theme = AphroditeTheme()
        
        super().__init__(
            parent,
            bg=self.theme.colors.bg_secondary,
            height=60,
            **kwargs
        )
        
        self.pack_propagate(False)
        
        # Menu items
        self.menu_items = {}
        self.active_item = None
    
    def add_menu_item(self, text: str, command: Callable = None, icon: str = ""):
        """Add a menu item."""
        item_frame = tk.Frame(
            self,
            bg=self.theme.colors.bg_secondary,
            relief="flat",
            borderwidth=0
        )
        item_frame.pack(side="left", padx=5, pady=10)
        
        # Icon
        if icon:
            icon_label = tk.Label(
                item_frame,
                text=icon,
                font=("Arial", 16),
                bg="transparent",
                fg=self.theme.colors.text_secondary
            )
            icon_label.pack()
        
        # Text
        text_label = tk.Label(
            item_frame,
            text=text,
            **self.theme.styles['label_body']
        )
        text_label.pack()
        
        # Bind events
        item_frame.bind("<Enter>", lambda e, f=item_frame: self._on_item_enter(f))
        item_frame.bind("<Leave>", lambda e, f=item_frame: self._on_item_leave(f))
        item_frame.bind("<Button-1>", lambda e, cmd=command: self._on_item_click(cmd))
        
        text_label.bind("<Enter>", lambda e, f=item_frame: self._on_item_enter(f))
        text_label.bind("<Leave>", lambda e, f=item_frame: self._on_item_leave(f))
        text_label.bind("<Button-1>", lambda e, cmd=command: self._on_item_click(cmd))
        
        if icon:
            icon_label.bind("<Enter>", lambda e, f=item_frame: self._on_item_enter(f))
            icon_label.bind("<Leave>", lambda e, f=item_frame: self._on_item_leave(f))
            icon_label.bind("<Button-1>", lambda e, cmd=command: self._on_item_click(cmd))
        
        self.menu_items[text] = item_frame
    
    def _on_item_enter(self, item_frame):
        """Handle menu item enter."""
        item_frame.configure(bg=self.theme.colors.bg_accent)
        for child in item_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(fg=self.theme.colors.primary_rose)
    
    def _on_item_leave(self, item_frame):
        """Handle menu item leave."""
        item_frame.configure(bg=self.theme.colors.bg_secondary)
        for child in item_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(fg=self.theme.colors.text_secondary)
    
    def _on_item_click(self, command):
        """Handle menu item click."""
        if command:
            command() 