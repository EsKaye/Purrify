"""
Main GUI Window for Purrify

This module provides the main application window with beautiful
Aphrodite-inspired design and fluid animations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
from typing import Dict, Any, Optional
import time

from ..core.config import Config
from ..core.engine import PurrifyEngine
from .styles import AphroditeTheme
from .widgets import (
    AphroditeButton, AphroditeCard, AphroditeProgressBar,
    AphroditeStatusCard, AphroditeAnimatedCanvas, AphroditeMenuBar
)

class PurrifyGUI:
    """Main GUI application for Purrify with Aphrodite-inspired design."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.theme = AphroditeTheme()
        self.config = Config()
        self.engine = PurrifyEngine(self.config)
        
        # GUI state
        self.current_page = "home"
        self.scan_running = False
        self.clean_running = False
        self.optimize_running = False
        
        # Initialize GUI
        self._setup_window()
        self._apply_theme()
        self._create_widgets()
        self._setup_layout()
        self._start_background_animations()
    
    def _setup_window(self):
        """Setup the main window."""
        self.root.title("🐱 Purrify - AI-Driven System Optimization")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
    
    def _apply_theme(self):
        """Apply the Aphrodite theme."""
        self.theme.apply_theme(self.root)
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Menu bar
        self.menu_bar = AphroditeMenuBar(self.root)
        self.menu_bar.add_menu_item("🏠 Home", self._show_home_page, "🏠")
        self.menu_bar.add_menu_item("🔍 Scan", self._show_scan_page, "🔍")
        self.menu_bar.add_menu_item("🧹 Clean", self._show_clean_page, "🧹")
        self.menu_bar.add_menu_item("⚡ Optimize", self._show_optimize_page, "⚡")
        self.menu_bar.add_menu_item("📊 Reports", self._show_reports_page, "📊")
        self.menu_bar.add_menu_item("⚙️ Settings", self._show_settings_page, "⚙️")
        
        # Main content area
        self.main_frame = tk.Frame(self.root, bg=self.theme.colors.bg_primary)
        
        # Animated background canvas
        self.background_canvas = AphroditeAnimatedCanvas(
            self.main_frame,
            width=1000,
            height=700
        )
        
        # Content frame
        self.content_frame = tk.Frame(
            self.main_frame,
            bg="transparent"
        )
        
        # Create pages
        self._create_home_page()
        self._create_scan_page()
        self._create_clean_page()
        self._create_optimize_page()
        self._create_reports_page()
        self._create_settings_page()
        
        # Status bar
        self.status_bar = tk.Frame(
            self.root,
            bg=self.theme.colors.bg_secondary,
            height=30
        )
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready to purify your system ✨",
            **self.theme.styles['label_body']
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def _setup_layout(self):
        """Setup the main layout."""
        # Menu bar
        self.menu_bar.pack(fill="x")
        
        # Main content
        self.main_frame.pack(fill="both", expand=True)
        self.background_canvas.pack(fill="both", expand=True)
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Status bar
        self.status_bar.pack(fill="x", side="bottom")
        
        # Show home page by default
        self._show_home_page()
    
    def _create_home_page(self):
        """Create the home page."""
        self.home_page = tk.Frame(self.content_frame, bg="transparent")
        
        # Welcome title
        title_label = tk.Label(
            self.home_page,
            text="🐱 Welcome to Purrify",
            **self.theme.styles['label_title']
        )
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(
            self.home_page,
            text="AI-Driven System Optimization with Aphrodite's Grace",
            **self.theme.styles['label_body']
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Quick action buttons
        button_frame = tk.Frame(self.home_page, bg="transparent")
        button_frame.pack(pady=20)
        
        AphroditeButton(
            button_frame,
            text="🔍 Quick Scan",
            command=self._quick_scan,
            style="primary"
        ).pack(side="left", padx=10)
        
        AphroditeButton(
            button_frame,
            text="🧹 Safe Clean",
            command=self._safe_clean,
            style="secondary"
        ).pack(side="left", padx=10)
        
        AphroditeButton(
            button_frame,
            text="⚡ Optimize",
            command=self._quick_optimize,
            style="ghost"
        ).pack(side="left", padx=10)
        
        # System status cards
        status_frame = tk.Frame(self.home_page, bg="transparent")
        status_frame.pack(pady=40)
        
        self.cpu_card = AphroditeStatusCard(
            status_frame,
            title="CPU Usage",
            value="0%",
            icon="⚡",
            status="normal"
        )
        self.cpu_card.pack(side="left", padx=10)
        
        self.memory_card = AphroditeStatusCard(
            status_frame,
            title="Memory",
            value="0%",
            icon="🧠",
            status="normal"
        )
        self.memory_card.pack(side="left", padx=10)
        
        self.disk_card = AphroditeStatusCard(
            status_frame,
            title="Disk Space",
            value="0%",
            icon="💾",
            status="normal"
        )
        self.disk_card.pack(side="left", padx=10)
        
        # Update system status
        self._update_system_status()
    
    def _create_scan_page(self):
        """Create the scan page."""
        self.scan_page = tk.Frame(self.content_frame, bg="transparent")
        
        # Title
        title_label = tk.Label(
            self.scan_page,
            text="🔍 System Scanner",
            **self.theme.styles['label_title']
        )
        title_label.pack(pady=(0, 20))
        
        # Scan options card
        options_card = AphroditeCard(self.scan_page, title="Scan Options")
        options_card.pack(fill="x", padx=20, pady=10)
        
        # Scan type options
        self.quick_scan_var = tk.BooleanVar(value=True)
        self.detailed_scan_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_card,
            text="Quick Scan (Fast)",
            variable=self.quick_scan_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            options_card,
            text="Detailed Scan (Thorough)",
            variable=self.detailed_scan_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        # Scan button
        self.scan_button = AphroditeButton(
            self.scan_page,
            text="🔍 Start Scan",
            command=self._start_scan,
            style="primary"
        )
        self.scan_button.pack(pady=20)
        
        # Progress bar
        self.scan_progress = AphroditeProgressBar(self.scan_page)
        self.scan_progress.pack(fill="x", padx=20, pady=10)
        
        # Results card
        self.scan_results_card = AphroditeCard(self.scan_page, title="Scan Results")
        self.scan_results_card.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Results text
        self.scan_results_text = tk.Text(
            self.scan_results_card,
            height=10,
            bg=self.theme.colors.bg_secondary,
            fg=self.theme.colors.text_primary,
            font=self.theme.fonts['body_small'],
            relief="flat",
            borderwidth=0
        )
        self.scan_results_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_clean_page(self):
        """Create the clean page."""
        self.clean_page = tk.Frame(self.content_frame, bg="transparent")
        
        # Title
        title_label = tk.Label(
            self.clean_page,
            text="🧹 System Cleaner",
            **self.theme.styles['label_title']
        )
        title_label.pack(pady=(0, 20))
        
        # Clean options card
        options_card = AphroditeCard(self.clean_page, title="Cleaning Options")
        options_card.pack(fill="x", padx=20, pady=10)
        
        # Clean type options
        self.clean_caches_var = tk.BooleanVar(value=True)
        self.clean_logs_var = tk.BooleanVar(value=True)
        self.clean_temp_var = tk.BooleanVar(value=True)
        self.safe_mode_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            options_card,
            text="🗂️ Application Caches",
            variable=self.clean_caches_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            options_card,
            text="📝 System Logs",
            variable=self.clean_logs_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            options_card,
            text="🗑️ Temporary Files",
            variable=self.clean_temp_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            options_card,
            text="🛡️ Safe Mode (Preview Only)",
            variable=self.safe_mode_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        # Clean button
        self.clean_button = AphroditeButton(
            self.clean_page,
            text="🧹 Start Cleaning",
            command=self._start_cleaning,
            style="primary"
        )
        self.clean_button.pack(pady=20)
        
        # Progress bar
        self.clean_progress = AphroditeProgressBar(self.clean_page)
        self.clean_progress.pack(fill="x", padx=20, pady=10)
        
        # Results card
        self.clean_results_card = AphroditeCard(self.clean_page, title="Cleaning Results")
        self.clean_results_card.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Results text
        self.clean_results_text = tk.Text(
            self.clean_results_card,
            height=10,
            bg=self.theme.colors.bg_secondary,
            fg=self.theme.colors.text_primary,
            font=self.theme.fonts['body_small'],
            relief="flat",
            borderwidth=0
        )
        self.clean_results_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_optimize_page(self):
        """Create the optimize page."""
        self.optimize_page = tk.Frame(self.content_frame, bg="transparent")
        
        # Title
        title_label = tk.Label(
            self.optimize_page,
            text="⚡ Performance Optimizer",
            **self.theme.styles['label_title']
        )
        title_label.pack(pady=(0, 20))
        
        # Optimization options card
        options_card = AphroditeCard(self.optimize_page, title="Optimization Options")
        options_card.pack(fill="x", padx=20, pady=10)
        
        # Optimization type options
        self.opt_startup_var = tk.BooleanVar(value=True)
        self.opt_memory_var = tk.BooleanVar(value=True)
        self.opt_disk_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            options_card,
            text="🚀 Startup Optimization",
            variable=self.opt_startup_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            options_card,
            text="🧠 Memory Optimization",
            variable=self.opt_memory_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            options_card,
            text="💾 Disk Optimization",
            variable=self.opt_disk_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        # Optimize button
        self.optimize_button = AphroditeButton(
            self.optimize_page,
            text="⚡ Start Optimization",
            command=self._start_optimization,
            style="primary"
        )
        self.optimize_button.pack(pady=20)
        
        # Progress bar
        self.optimize_progress = AphroditeProgressBar(self.optimize_page)
        self.optimize_progress.pack(fill="x", padx=20, pady=10)
        
        # Results card
        self.optimize_results_card = AphroditeCard(self.optimize_page, title="Optimization Results")
        self.optimize_results_card.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Results text
        self.optimize_results_text = tk.Text(
            self.optimize_results_card,
            height=10,
            bg=self.theme.colors.bg_secondary,
            fg=self.theme.colors.text_primary,
            font=self.theme.fonts['body_small'],
            relief="flat",
            borderwidth=0
        )
        self.optimize_results_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_reports_page(self):
        """Create the reports page."""
        self.reports_page = tk.Frame(self.content_frame, bg="transparent")
        
        # Title
        title_label = tk.Label(
            self.reports_page,
            text="📊 System Reports",
            **self.theme.styles['label_title']
        )
        title_label.pack(pady=(0, 20))
        
        # Report options
        button_frame = tk.Frame(self.reports_page, bg="transparent")
        button_frame.pack(pady=20)
        
        AphroditeButton(
            button_frame,
            text="📈 Generate Report",
            command=self._generate_report,
            style="primary"
        ).pack(side="left", padx=10)
        
        AphroditeButton(
            button_frame,
            text="💾 Save Report",
            command=self._save_report,
            style="secondary"
        ).pack(side="left", padx=10)
        
        # Report content
        self.report_text = tk.Text(
            self.reports_page,
            height=20,
            bg=self.theme.colors.bg_secondary,
            fg=self.theme.colors.text_primary,
            font=self.theme.fonts['body_small'],
            relief="flat",
            borderwidth=0
        )
        self.report_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def _create_settings_page(self):
        """Create the settings page."""
        self.settings_page = tk.Frame(self.content_frame, bg="transparent")
        
        # Title
        title_label = tk.Label(
            self.settings_page,
            text="⚙️ Settings",
            **self.theme.styles['label_title']
        )
        title_label.pack(pady=(0, 20))
        
        # Settings card
        settings_card = AphroditeCard(self.settings_page, title="Application Settings")
        settings_card.pack(fill="x", padx=20, pady=10)
        
        # Settings options
        self.auto_backup_var = tk.BooleanVar(value=True)
        self.safe_mode_var = tk.BooleanVar(value=True)
        self.verbose_logging_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            settings_card,
            text="💾 Auto Backup",
            variable=self.auto_backup_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            settings_card,
            text="🛡️ Safe Mode",
            variable=self.safe_mode_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Checkbutton(
            settings_card,
            text="📝 Verbose Logging",
            variable=self.verbose_logging_var,
            bg="transparent",
            fg=self.theme.colors.text_primary,
            selectcolor=self.theme.colors.bg_secondary
        ).pack(anchor="w", padx=10, pady=5)
        
        # Save button
        AphroditeButton(
            self.settings_page,
            text="💾 Save Settings",
            command=self._save_settings,
            style="primary"
        ).pack(pady=20)
    
    def _start_background_animations(self):
        """Start background animations."""
        self.background_canvas.start_water_flow()
    
    def _update_system_status(self):
        """Update system status display."""
        def update():
            try:
                status = asyncio.run(self.engine.get_system_status())
                
                if 'error' not in status:
                    # Update CPU
                    cpu_percent = status.get('cpu_usage_percent', 0)
                    self.cpu_card.update_value(f"{cpu_percent:.1f}%")
                    self.cpu_card.update_status('normal' if cpu_percent < 80 else 'warning')
                    
                    # Update Memory
                    memory_percent = status.get('memory_percent_used', 0)
                    self.memory_card.update_value(f"{memory_percent:.1f}%")
                    self.memory_card.update_status('normal' if memory_percent < 80 else 'warning')
                    
                    # Update Disk
                    disk_percent = status.get('disk_percent_used', 0)
                    self.disk_card.update_value(f"{disk_percent:.1f}%")
                    self.disk_card.update_status('normal' if disk_percent < 90 else 'warning')
                
            except Exception as e:
                print(f"Error updating system status: {e}")
        
        # Update every 5 seconds
        self.root.after(5000, self._update_system_status)
        update()
    
    def _show_page(self, page_name: str):
        """Show a specific page."""
        # Hide all pages
        for page in [self.home_page, self.scan_page, self.clean_page, 
                    self.optimize_page, self.reports_page, self.settings_page]:
            page.pack_forget()
        
        # Show selected page
        if page_name == "home":
            self.home_page.pack(fill="both", expand=True)
        elif page_name == "scan":
            self.scan_page.pack(fill="both", expand=True)
        elif page_name == "clean":
            self.clean_page.pack(fill="both", expand=True)
        elif page_name == "optimize":
            self.optimize_page.pack(fill="both", expand=True)
        elif page_name == "reports":
            self.reports_page.pack(fill="both", expand=True)
        elif page_name == "settings":
            self.settings_page.pack(fill="both", expand=True)
        
        self.current_page = page_name
    
    def _show_home_page(self):
        self._show_page("home")
    
    def _show_scan_page(self):
        self._show_page("scan")
    
    def _show_clean_page(self):
        self._show_page("clean")
    
    def _show_optimize_page(self):
        self._show_page("optimize")
    
    def _show_reports_page(self):
        self._show_page("reports")
    
    def _show_settings_page(self):
        self._show_page("settings")
    
    def _quick_scan(self):
        """Perform a quick scan."""
        self._show_scan_page()
        self._start_scan()
    
    def _safe_clean(self):
        """Perform safe cleaning."""
        self._show_clean_page()
        self._start_cleaning()
    
    def _quick_optimize(self):
        """Perform quick optimization."""
        self._show_optimize_page()
        self._start_optimization()
    
    def _start_scan(self):
        """Start system scan."""
        if self.scan_running:
            return
        
        self.scan_running = True
        self.scan_button.configure(state="disabled", text="🔍 Scanning...")
        self.scan_progress.set_progress(0)
        
        def scan_thread():
            try:
                # Determine scan mode
                quick_mode = self.quick_scan_var.get()
                detailed_mode = self.detailed_scan_var.get()
                
                # Run scan
                scan_result = asyncio.run(self.engine.scan_system(
                    quick_mode=quick_mode,
                    detailed_mode=detailed_mode
                ))
                
                # Update UI
                self.root.after(0, lambda: self._scan_completed(scan_result))
                
            except Exception as e:
                self.root.after(0, lambda: self._scan_error(str(e)))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def _scan_completed(self, scan_result):
        """Handle scan completion."""
        self.scan_running = False
        self.scan_button.configure(state="normal", text="🔍 Start Scan")
        self.scan_progress.set_progress(1.0)
        
        # Display results
        results_text = f"""
Scan Completed Successfully!

📊 Scan Results:
• Files Scanned: {scan_result.total_files_scanned}
• Cache Files: {scan_result.cache_files_found}
• Temp Files: {scan_result.temp_files_found}
• Log Files: {scan_result.log_files_found}
• Large Files: {scan_result.large_files_found}
• Potential Savings: {self._format_bytes(scan_result.potential_space_savings)}
• Scan Duration: {scan_result.scan_duration:.2f}s

🔍 Scan Errors: {len(scan_result.scan_errors)}
"""
        
        self.scan_results_text.delete(1.0, tk.END)
        self.scan_results_text.insert(1.0, results_text)
        
        self.status_label.configure(text="Scan completed successfully! ✨")
    
    def _scan_error(self, error: str):
        """Handle scan error."""
        self.scan_running = False
        self.scan_button.configure(state="normal", text="🔍 Start Scan")
        self.scan_progress.set_progress(0)
        
        messagebox.showerror("Scan Error", f"Scan failed: {error}")
        self.status_label.configure(text="Scan failed ❌")
    
    def _start_cleaning(self):
        """Start system cleaning."""
        if self.clean_running:
            return
        
        self.clean_running = True
        self.clean_button.configure(state="disabled", text="🧹 Cleaning...")
        self.clean_progress.set_progress(0)
        
        def clean_thread():
            try:
                # Determine cleaning options
                clean_options = {
                    "caches": self.clean_caches_var.get(),
                    "logs": self.clean_logs_var.get(),
                    "temp_files": self.clean_temp_var.get(),
                }
                
                safe_mode = self.safe_mode_var.get()
                
                # Run cleaning
                clean_result = asyncio.run(self.engine.clean_system(
                    clean_options=clean_options,
                    safe_mode=safe_mode,
                    create_backup=True
                ))
                
                # Update UI
                self.root.after(0, lambda: self._clean_completed(clean_result))
                
            except Exception as e:
                self.root.after(0, lambda: self._clean_error(str(e)))
        
        threading.Thread(target=clean_thread, daemon=True).start()
    
    def _clean_completed(self, clean_result):
        """Handle cleaning completion."""
        self.clean_running = False
        self.clean_button.configure(state="normal", text="🧹 Start Cleaning")
        self.clean_progress.set_progress(1.0)
        
        # Display results
        results_text = f"""
Cleaning Completed Successfully!

🧹 Cleaning Results:
• Files Cleaned: {clean_result.files_cleaned}
• Space Freed: {self._format_bytes(clean_result.space_freed)}
• Clean Duration: {clean_result.clean_duration:.2f}s
• Backup Created: {'Yes' if clean_result.backup_created else 'No'}

🔍 Clean Errors: {len(clean_result.clean_errors)}
"""
        
        self.clean_results_text.delete(1.0, tk.END)
        self.clean_results_text.insert(1.0, results_text)
        
        self.status_label.configure(text="Cleaning completed successfully! ✨")
    
    def _clean_error(self, error: str):
        """Handle cleaning error."""
        self.clean_running = False
        self.clean_button.configure(state="normal", text="🧹 Start Cleaning")
        self.clean_progress.set_progress(0)
        
        messagebox.showerror("Cleaning Error", f"Cleaning failed: {error}")
        self.status_label.configure(text="Cleaning failed ❌")
    
    def _start_optimization(self):
        """Start system optimization."""
        if self.optimize_running:
            return
        
        self.optimize_running = True
        self.optimize_button.configure(state="disabled", text="⚡ Optimizing...")
        self.optimize_progress.set_progress(0)
        
        def optimize_thread():
            try:
                # Determine optimization options
                opt_options = {
                    "startup": self.opt_startup_var.get(),
                    "memory": self.opt_memory_var.get(),
                    "disk": self.opt_disk_var.get(),
                }
                
                # Run optimization
                opt_result = asyncio.run(self.engine.optimize_system(
                    optimization_options=opt_options,
                    safe_mode=True
                ))
                
                # Update UI
                self.root.after(0, lambda: self._optimize_completed(opt_result))
                
            except Exception as e:
                self.root.after(0, lambda: self._optimize_error(str(e)))
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    def _optimize_completed(self, opt_result):
        """Handle optimization completion."""
        self.optimize_running = False
        self.optimize_button.configure(state="normal", text="⚡ Start Optimization")
        self.optimize_progress.set_progress(1.0)
        
        # Display results
        results_text = f"""
Optimization Completed Successfully!

⚡ Optimization Results:
• Optimizations Applied: {opt_result.optimizations_applied}
• Performance Improvement: {opt_result.performance_improvement:.1f}%
• Optimization Duration: {opt_result.optimization_duration:.2f}s
• Startup Items Optimized: {opt_result.startup_items_optimized}
• Memory Optimized: {'Yes' if opt_result.memory_optimized else 'No'}
• Disk Optimized: {'Yes' if opt_result.disk_optimized else 'No'}

🔍 Optimization Errors: {len(opt_result.optimization_errors)}
"""
        
        self.optimize_results_text.delete(1.0, tk.END)
        self.optimize_results_text.insert(1.0, results_text)
        
        self.status_label.configure(text="Optimization completed successfully! ✨")
    
    def _optimize_error(self, error: str):
        """Handle optimization error."""
        self.optimize_running = False
        self.optimize_button.configure(state="normal", text="⚡ Start Optimization")
        self.optimize_progress.set_progress(0)
        
        messagebox.showerror("Optimization Error", f"Optimization failed: {error}")
        self.status_label.configure(text="Optimization failed ❌")
    
    def _generate_report(self):
        """Generate system report."""
        try:
            report_data = asyncio.run(self.engine.generate_report(detailed=True))
            
            if 'error' not in report_data:
                report_text = f"""
System Optimization Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

📊 System Overview:
{report_data.get('system_overview', 'No data available')}

🔍 Recent Scans:
{report_data.get('recent_scans', 'No scans available')}

🧹 Recent Cleanings:
{report_data.get('recent_cleanings', 'No cleanings available')}

⚡ Recent Optimizations:
{report_data.get('recent_optimizations', 'No optimizations available')}

🤖 AI Insights:
{report_data.get('ai_insights', 'No insights available')}
"""
                
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(1.0, report_text)
                
                self.status_label.configure(text="Report generated successfully! 📊")
            else:
                messagebox.showerror("Report Error", f"Failed to generate report: {report_data['error']}")
                
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {e}")
    
    def _save_report(self):
        """Save report to file."""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.report_text.get(1.0, tk.END))
                
                messagebox.showinfo("Success", f"Report saved to {filename}")
                self.status_label.configure(text="Report saved successfully! 💾")
                
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save report: {e}")
    
    def _save_settings(self):
        """Save application settings."""
        try:
            # Update config
            self.config.general.auto_backup = self.auto_backup_var.get()
            self.config.general.safe_mode = self.safe_mode_var.get()
            
            # Save config
            self.config.save()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.status_label.configure(text="Settings saved successfully! ⚙️")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save settings: {e}")
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()

def launch_gui():
    """Launch the Purrify GUI application."""
    app = PurrifyGUI()
    app.run() 