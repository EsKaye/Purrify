"""
Fluid Animations for Purrify GUI

This module provides beautiful, flowing animations inspired by
Aphrodite's cleansing waters and graceful movements.
"""

import tkinter as tk
import math
import time
import threading
import random
from typing import Callable, Optional, List
from .styles import AphroditeTheme

class FluidAnimations:
    """Beautiful fluid animations for the Purrify interface."""
    
    def __init__(self, canvas: tk.Canvas, theme: AphroditeTheme):
        self.canvas = canvas
        self.theme = theme
        self.colors = theme.colors
        self.animation_running = False
        self.particles = []
        self.waves = []
        self.ripples = []
    
    def start_water_flow(self, duration: float = 3.0):
        """Start a beautiful water flow animation."""
        self.animation_running = True
        self._create_water_particles()
        self._animate_water_flow(duration)
    
    def start_cleansing_waves(self, duration: float = 2.0):
        """Start cleansing wave animations."""
        self.animation_running = True
        self._create_cleansing_waves()
        self._animate_waves(duration)
    
    def start_ripple_effect(self, x: int, y: int, color: str = None):
        """Start a ripple effect from a specific point."""
        if color is None:
            color = self.colors.primary_azure
        
        ripple = {
            'x': x,
            'y': y,
            'radius': 0,
            'max_radius': 100,
            'color': color,
            'alpha': 1.0,
            'speed': 2
        }
        self.ripples.append(ripple)
        self._animate_ripples()
    
    def start_gradient_flow(self, duration: float = 4.0):
        """Start a flowing gradient animation."""
        self.animation_running = True
        gradient_colors = self.theme.get_gradient_colors()
        self._animate_gradient(gradient_colors, duration)
    
    def stop_animations(self):
        """Stop all running animations."""
        self.animation_running = False
        self.particles.clear()
        self.waves.clear()
        self.ripples.clear()
        self.canvas.delete("animation")
    
    def _create_water_particles(self):
        """Create water particles for flow animation."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        for _ in range(20):
            particle = {
                'x': 0,
                'y': canvas_height * 0.2 + random.random() * canvas_height * 0.6,
                'vx': 1 + random.random() * 2,
                'vy': -0.5 + random.random() * 1,
                'size': 2 + random.random() * 4,
                'alpha': 0.3 + random.random() * 0.7,
                'color': self.colors.primary_azure
            }
            self.particles.append(particle)
    
    def _animate_water_flow(self, duration: float):
        """Animate water particles flowing across the canvas."""
        if not self.animation_running:
            return
        
        self.canvas.delete("water_particles")
        canvas_width = self.canvas.winfo_width()
        
        for particle in self.particles:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around if off screen
            if particle['x'] > canvas_width:
                particle['x'] = -10
                particle['y'] = self.canvas.winfo_height() * 0.2 + random.random() * self.canvas.winfo_height() * 0.6
            
            # Draw particle
            alpha = int(particle['alpha'] * 255)
            color = self._adjust_color_alpha(particle['color'], alpha)
            
            self.canvas.create_oval(
                particle['x'] - particle['size'],
                particle['y'] - particle['size'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size'],
                fill=color,
                outline="",
                tags="water_particles"
            )
        
        # Schedule next frame
        self.canvas.after(50, lambda: self._animate_water_flow(duration))
    
    def _create_cleansing_waves(self):
        """Create cleansing wave animations."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        for i in range(3):
            wave = {
                'x': canvas_width * 0.1,
                'y': canvas_height * 0.3 + i * canvas_height * 0.2,
                'amplitude': 20 + i * 10,
                'frequency': 0.02 + i * 0.01,
                'phase': i * math.pi / 3,
                'color': self.colors.primary_rose,
                'width': 3 + i * 2
            }
            self.waves.append(wave)
    
    def _animate_waves(self, duration: float):
        """Animate cleansing waves."""
        if not self.animation_running:
            return
        
        self.canvas.delete("waves")
        canvas_width = self.canvas.winfo_width()
        
        for wave in self.waves:
            points = []
            for x in range(0, int(canvas_width * 0.8), 5):
                y = wave['y'] + wave['amplitude'] * math.sin(
                    wave['frequency'] * x + wave['phase']
                )
                points.extend([x, y])
            
            if len(points) >= 4:
                self.canvas.create_line(
                    points,
                    fill=wave['color'],
                    width=wave['width'],
                    smooth=True,
                    tags="waves"
                )
            
            wave['phase'] += 0.1
        
        # Schedule next frame
        self.canvas.after(50, lambda: self._animate_waves(duration))
    
    def _animate_ripples(self):
        """Animate ripple effects."""
        if not self.ripples:
            return
        
        self.canvas.delete("ripples")
        
        for ripple in self.ripples[:]:
            # Update ripple
            ripple['radius'] += ripple['speed']
            ripple['alpha'] -= 0.02
            
            if ripple['alpha'] <= 0 or ripple['radius'] > ripple['max_radius']:
                self.ripples.remove(ripple)
                continue
            
            # Draw ripple
            alpha = int(ripple['alpha'] * 255)
            color = self._adjust_color_alpha(ripple['color'], alpha)
            
            self.canvas.create_oval(
                ripple['x'] - ripple['radius'],
                ripple['y'] - ripple['radius'],
                ripple['x'] + ripple['radius'],
                ripple['y'] + ripple['radius'],
                outline=color,
                width=2,
                tags="ripples"
            )
        
        # Schedule next frame
        self.canvas.after(30, self._animate_ripples)
    
    def _animate_gradient(self, colors: List[str], duration: float):
        """Animate flowing gradient."""
        if not self.animation_running:
            return
        
        self.canvas.delete("gradient")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Create flowing gradient
        for i in range(0, canvas_width, 5):
            color_index = (i // 50) % len(colors)
            next_color_index = (color_index + 1) % len(colors)
            
            # Interpolate between colors
            blend_factor = (i % 50) / 50
            color = self._blend_colors(colors[color_index], colors[next_color_index], blend_factor)
            
            self.canvas.create_line(
                i, 0, i, canvas_height,
                fill=color,
                width=5,
                tags="gradient"
            )
        
        # Schedule next frame
        self.canvas.after(100, lambda: self._animate_gradient(colors, duration))
    
    def _adjust_color_alpha(self, color: str, alpha: int) -> str:
        """Adjust color alpha for transparency effects."""
        # Convert hex to RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Apply alpha
        r = int(r * alpha / 255)
        g = int(g * alpha / 255)
        b = int(b * alpha / 255)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Blend two colors with a factor."""
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Blend
        r = int(r1 * (1 - factor) + r2 * factor)
        g = int(g1 * (1 - factor) + g2 * factor)
        b = int(b1 * (1 - factor) + b2 * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"

class ProgressAnimation:
    """Animated progress bar with fluid effects."""
    
    def __init__(self, canvas: tk.Canvas, theme: AphroditeTheme):
        self.canvas = canvas
        self.theme = theme
        self.progress = 0
        self.target_progress = 0
        self.animation_running = False
    
    def animate_progress(self, target: float, duration: float = 1.0):
        """Animate progress to target value."""
        self.target_progress = target
        self.animation_running = True
        self._update_progress(duration)
    
    def _update_progress(self, duration: float):
        """Update progress animation."""
        if not self.animation_running:
            return
        
        # Smooth interpolation
        diff = self.target_progress - self.progress
        if abs(diff) > 0.01:
            self.progress += diff * 0.1
            self._draw_progress()
            self.canvas.after(20, lambda: self._update_progress(duration))
        else:
            self.progress = self.target_progress
            self._draw_progress()
            self.animation_running = False
    
    def _draw_progress(self):
        """Draw the animated progress bar."""
        self.canvas.delete("progress")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Background
        self.canvas.create_rectangle(
            0, 0, canvas_width, canvas_height,
            fill=self.theme.colors.bg_secondary,
            outline="",
            tags="progress"
        )
        
        # Progress bar
        progress_width = int(canvas_width * self.progress)
        if progress_width > 0:
            self.canvas.create_rectangle(
                0, 0, progress_width, canvas_height,
                fill=self.theme.colors.primary_rose,
                outline="",
                tags="progress"
            )
        
        # Progress text
        percentage = int(self.progress * 100)
        self.canvas.create_text(
            canvas_width // 2, canvas_height // 2,
            text=f"{percentage}%",
            font=self.theme.fonts['heading'],
            fill=self.theme.colors.text_primary,
            tags="progress"
        ) 