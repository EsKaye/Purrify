"""
Purrify Core Engine

This module contains the main PurrifyEngine class that orchestrates
all system optimization operations including scanning, cleaning,
and performance optimization.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from loguru import logger

from .config import Config
from ..scanners.system_scanner import SystemScanner
from ..cleaners.cache_cleaner import CacheCleaner
from ..optimizers.performance_optimizer import PerformanceOptimizer
from ..ai.intelligence_engine import IntelligenceEngine
from ..utils.platform import detect_platform
from ..utils.reporting import ReportGenerator


@dataclass
class ScanResult:
    """Results from system scanning operation."""
    total_files_scanned: int = 0
    cache_files_found: int = 0
    temp_files_found: int = 0
    log_files_found: int = 0
    large_files_found: int = 0
    potential_space_savings: int = 0  # in bytes
    scan_duration: float = 0.0
    scan_errors: List[str] = field(default_factory=list)
    file_details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CleanResult:
    """Results from system cleaning operation."""
    files_cleaned: int = 0
    space_freed: int = 0  # in bytes
    clean_duration: float = 0.0
    clean_errors: List[str] = field(default_factory=list)
    backup_created: bool = False
    backup_path: Optional[str] = None


@dataclass
class OptimizationResult:
    """Results from system optimization operation."""
    optimizations_applied: int = 0
    performance_improvement: float = 0.0  # percentage
    optimization_duration: float = 0.0
    optimization_errors: List[str] = field(default_factory=list)
    startup_items_optimized: int = 0
    memory_optimized: bool = False
    disk_optimized: bool = False


class PurrifyEngine:
    """
    Main engine for Purrify system optimization utility.
    
    This class orchestrates all system optimization operations including
    scanning, cleaning, and performance optimization with AI-powered
    intelligence for safe and effective system maintenance.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the Purrify engine.
        
        Args:
            config: Configuration object containing all settings
        """
        self.config = config
        self.platform = detect_platform()
        
        # Initialize core components
        self.scanner = SystemScanner(config)
        self.cleaner = CacheCleaner(config)
        self.optimizer = PerformanceOptimizer(config)
        self.ai_engine = IntelligenceEngine(config)
        self.report_generator = ReportGenerator(config)
        
        # Performance tracking
        self.operation_history: List[Dict[str, Any]] = []
        self.last_scan_result: Optional[ScanResult] = None
        self.last_clean_result: Optional[CleanResult] = None
        self.last_optimization_result: Optional[OptimizationResult] = None
        
        logger.info("PurrifyEngine initialized successfully")
    
    async def scan_system(
        self,
        quick_mode: bool = False,
        detailed_mode: bool = False,
        include_duplicates: bool = True,
        include_photos: bool = True,
        include_large_files: bool = True
    ) -> ScanResult:
        """
        Perform comprehensive system scan for optimization opportunities.
        
        Args:
            quick_mode: Enable quick scan mode for faster results
            detailed_mode: Enable detailed scan with file analysis
            include_duplicates: Scan for duplicate files
            include_photos: Analyze photos for optimization
            include_large_files: Identify large files
            
        Returns:
            ScanResult object containing scan findings
        """
        logger.info("Starting enhanced system scan...")
        start_time = time.time()
        
        try:
            # Perform enhanced system scan
            scan_data = await self.scanner.scan_system(
                quick_mode=quick_mode,
                detailed_mode=detailed_mode,
                include_duplicates=include_duplicates,
                include_photos=include_photos,
                include_large_files=include_large_files
            )
            
            # Convert enhanced dictionary result to ScanResult object
            scan_result = ScanResult(
                total_files_scanned=scan_data.get("total_files", 0),
                cache_files_found=sum(
                    cat_data.get("count", 0) 
                    for cat, cat_data in scan_data.get("categories", {}).items() 
                    if "cache" in cat
                ),
                temp_files_found=scan_data.get("categories", {}).get("temp", {}).get("count", 0),
                log_files_found=scan_data.get("categories", {}).get("log", {}).get("count", 0),
                large_files_found=scan_data.get("large_files", {}).get("count", 0),
                potential_space_savings=scan_data.get("potential_savings", 0),
                scan_duration=scan_data.get("scan_duration", 0.0),
                scan_errors=scan_data.get("errors", []),
                file_details=scan_data.get("categories", {})
            )
            
            # Add enhanced data to file_details
            scan_result.file_details.update({
                "duplicates": scan_data.get("duplicates", {}),
                "photos": scan_data.get("photos", {}),
                "large_files": scan_data.get("large_files", {}),
                "old_files": scan_data.get("old_files", {})
            })
            
            # Apply AI analysis if enabled
            if self.config.ai.enable_ml_analysis:
                scan_result = await self.ai_engine.analyze_scan_results(scan_result)
            
            # Update tracking
            scan_result.scan_duration = time.time() - start_time
            self.last_scan_result = scan_result
            
            # Log enhanced results
            logger.info(f"Enhanced system scan completed in {scan_result.scan_duration:.2f}s")
            logger.info(f"Found {scan_result.total_files_scanned} files")
            logger.info(f"Found {scan_data.get('duplicates', {}).get('groups', 0)} duplicate groups")
            logger.info(f"Analyzed {scan_data.get('photos', {}).get('count', 0)} photos")
            logger.info(f"Potential space savings: {self._format_bytes(scan_result.potential_space_savings)}")
            
            return scan_result
            
        except Exception as e:
            logger.error(f"Enhanced system scan failed: {e}")
            error_result = ScanResult(
                scan_errors=[str(e)],
                scan_duration=time.time() - start_time
            )
            return error_result
    
    async def clean_system(
        self,
        clean_options: Dict[str, bool],
        safe_mode: bool = True,
        create_backup: bool = True
    ) -> CleanResult:
        """
        Clean system caches and temporary files.
        
        Args:
            clean_options: Dictionary specifying what to clean
            safe_mode: Enable safe mode (preview only)
            create_backup: Create backup before cleaning
            
        Returns:
            CleanResult object containing cleaning results
        """
        logger.info("Starting system cleaning...")
        start_time = time.time()
        
        try:
            # Create backup if requested
            backup_path = None
            if create_backup and self.config.general.auto_backup:
                backup_path = await self._create_backup()
            
            # Perform cleaning operations
            clean_result = await self.cleaner.clean_system(
                clean_options=clean_options,
                safe_mode=safe_mode,
                backup_path=backup_path
            )
            
            # Apply AI safety checks
            if self.config.ai.enable_ml_analysis:
                clean_result = await self.ai_engine.validate_clean_operation(clean_result)
            
            # Update tracking
            clean_result.clean_duration = time.time() - start_time
            clean_result.backup_created = backup_path is not None
            clean_result.backup_path = backup_path
            self.last_clean_result = clean_result
            
            # Log results
            logger.info(f"System cleaning completed in {clean_result.clean_duration:.2f}s")
            logger.info(f"Cleaned {clean_result.files_cleaned} files")
            logger.info(f"Freed {self._format_bytes(clean_result.space_freed)}")
            
            return clean_result
            
        except Exception as e:
            logger.error(f"System cleaning failed: {e}")
            error_result = CleanResult(
                clean_errors=[str(e)],
                clean_duration=time.time() - start_time
            )
            return error_result
    
    async def optimize_system(
        self,
        optimization_options: Dict[str, bool],
        safe_mode: bool = True
    ) -> OptimizationResult:
        """
        Optimize system performance.
        
        Args:
            optimization_options: Dictionary specifying optimization types
            safe_mode: Enable safe mode (preview only)
            
        Returns:
            OptimizationResult object containing optimization results
        """
        logger.info("Starting system optimization...")
        start_time = time.time()
        
        try:
            # Perform optimization operations
            opt_result = await self.optimizer.optimize_system(
                optimization_options=optimization_options,
                safe_mode=safe_mode
            )
            
            # Apply AI optimization recommendations
            if self.config.ai.enable_ml_analysis:
                opt_result = await self.ai_engine.optimize_performance(opt_result)
            
            # Update tracking
            opt_result.optimization_duration = time.time() - start_time
            self.last_optimization_result = opt_result
            
            # Log results
            logger.info(f"System optimization completed in {opt_result.optimization_duration:.2f}s")
            logger.info(f"Applied {opt_result.optimizations_applied} optimizations")
            logger.info(f"Performance improvement: {opt_result.performance_improvement:.1f}%")
            
            return opt_result
            
        except Exception as e:
            logger.error(f"System optimization failed: {e}")
            error_result = OptimizationResult(
                optimization_errors=[str(e)],
                optimization_duration=time.time() - start_time
            )
            return error_result
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and metrics.
        
        Returns:
            Dictionary containing system status information
        """
        logger.info("Getting system status...")
        
        try:
            status_info = await self.scanner.get_system_status()
            
            # Add AI insights if enabled
            if self.config.ai.enable_ml_analysis:
                ai_insights = await self.ai_engine.get_system_insights(status_info)
                status_info['ai_insights'] = ai_insights
            
            return status_info
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}
    
    async def generate_report(self, detailed: bool = False) -> Dict[str, Any]:
        """
        Generate comprehensive system optimization report.
        
        Args:
            detailed: Include detailed information in report
            
        Returns:
            Dictionary containing report data
        """
        logger.info("Generating system report...")
        
        try:
            report_data = await self.report_generator.generate_report(
                scan_result=self.last_scan_result,
                clean_result=self.last_clean_result,
                optimization_result=self.last_optimization_result,
                detailed=detailed
            )
            
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {"error": str(e)}
    
    async def _create_backup(self) -> Optional[str]:
        """
        Create backup of critical files before cleaning.
        
        Returns:
            Path to backup directory if created, None otherwise
        """
        try:
            backup_dir = Path("backups") / f"purrify_backup_{int(time.time())}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Create backup of important files
            await self.cleaner.create_backup(backup_dir)
            
            logger.info(f"Backup created at: {backup_dir}")
            return str(backup_dir)
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def display_scan_results(self, scan_result: ScanResult, output_file: Optional[str] = None):
        """Display enhanced scan results in a user-friendly format."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        # Create main results table
        table = Table(title="🔍 Enhanced System Scan Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Files Scanned", f"{scan_result.total_files_scanned:,}")
        table.add_row("Cache Files", f"{scan_result.cache_files_found:,}")
        table.add_row("Temp Files", f"{scan_result.temp_files_found:,}")
        table.add_row("Log Files", f"{scan_result.log_files_found:,}")
        table.add_row("Large Files", f"{scan_result.large_files_found:,}")
        table.add_row("Potential Savings", self._format_bytes(scan_result.potential_space_savings))
        table.add_row("Scan Duration", f"{scan_result.scan_duration:.2f}s")
        
        console.print(table)
        
        # Display enhanced results if available
        if hasattr(scan_result, 'file_details') and scan_result.file_details:
            # Duplicates section
            duplicates = scan_result.file_details.get("duplicates", {})
            if duplicates.get("groups", 0) > 0:
                dup_table = Table(title="🔄 Duplicate Files Found")
                dup_table.add_column("Metric", style="cyan")
                dup_table.add_column("Value", style="green")
                
                dup_table.add_row("Duplicate Groups", f"{duplicates.get('groups', 0)}")
                dup_table.add_row("Total Duplicate Size", self._format_bytes(duplicates.get('total_size', 0)))
                dup_table.add_row("Potential Savings", self._format_bytes(duplicates.get('potential_savings', 0)))
                
                console.print(dup_table)
                
                # Show some duplicate groups
                if duplicates.get('groups_detail'):
                    console.print(Panel(
                        f"Found {len(duplicates['groups_detail'])} duplicate groups\n"
                        f"Largest group: {duplicates['groups_detail'][0].get('count', 0)} files "
                        f"({self._format_bytes(duplicates['groups_detail'][0].get('total_size', 0))})",
                        title="📋 Duplicate Summary",
                        border_style="yellow"
                    ))
            
            # Photos section
            photos = scan_result.file_details.get("photos", {})
            if photos.get("count", 0) > 0:
                photo_table = Table(title="📸 Photo Analysis")
                photo_table.add_column("Metric", style="cyan")
                photo_table.add_column("Value", style="green")
                
                photo_table.add_row("Photos Found", f"{photos.get('count', 0)}")
                photo_table.add_row("Total Photo Size", self._format_bytes(photos.get('total_size', 0)))
                photo_table.add_row("Potential Savings", self._format_bytes(photos.get('potential_savings', 0)))
                
                console.print(photo_table)
                
                # Show photo optimization opportunities
                if photos.get('photos_detail'):
                    console.print(Panel(
                        f"Analyzed {len(photos['photos_detail'])} photos for optimization\n"
                        f"Average compression potential: {photos.get('potential_savings', 0) / max(photos.get('count', 1), 1) / 1024 / 1024:.1f} MB per photo",
                        title="🎨 Photo Optimization",
                        border_style="magenta"
                    ))
            
            # Large files section
            large_files = scan_result.file_details.get("large_files", {})
            if large_files.get("count", 0) > 0:
                large_table = Table(title="📁 Large Files")
                large_table.add_column("Metric", style="cyan")
                large_table.add_column("Value", style="green")
                
                large_table.add_row("Large Files Found", f"{large_files.get('count', 0)}")
                large_table.add_row("Total Large File Size", self._format_bytes(large_files.get('total_size', 0)))
                
                console.print(large_table)
                
                # Show some large files
                if large_files.get('files'):
                    console.print(Panel(
                        f"Largest file: {self._format_bytes(large_files['files'][0].get('size', 0))}\n"
                        f"File type: {large_files['files'][0].get('file_type', 'Unknown')}",
                        title="📋 Large File Summary",
                        border_style="red"
                    ))
            
            # Old files section
            old_files = scan_result.file_details.get("old_files", {})
            if old_files.get("count", 0) > 0:
                old_table = Table(title="📅 Old Files")
                old_table.add_column("Metric", style="cyan")
                old_table.add_column("Value", style="green")
                
                old_table.add_row("Old Files Found", f"{old_files.get('count', 0)}")
                old_table.add_row("Total Old File Size", self._format_bytes(old_files.get('total_size', 0)))
                
                console.print(old_table)
        
        # Display errors if any
        if scan_result.scan_errors:
            error_panel = Panel(
                "\n".join(scan_result.scan_errors),
                title="⚠️ Scan Errors",
                border_style="red"
            )
            console.print(error_panel)
        
        # Save to file if requested
        if output_file:
            self._save_results_to_file(scan_result, output_file)
    
    def display_clean_results(self, clean_result: CleanResult):
        """Display cleaning results in a user-friendly format."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        # Create results table
        table = Table(title="🧹 System Cleaning Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Files Cleaned", f"{clean_result.files_cleaned:,}")
        table.add_row("Space Freed", self._format_bytes(clean_result.space_freed))
        table.add_row("Clean Duration", f"{clean_result.clean_duration:.2f}s")
        table.add_row("Backup Created", "✅" if clean_result.backup_created else "❌")
        
        if clean_result.backup_path:
            table.add_row("Backup Location", clean_result.backup_path)
        
        console.print(table)
        
        # Display errors if any
        if clean_result.clean_errors:
            error_panel = Panel(
                "\n".join(clean_result.clean_errors),
                title="⚠️ Cleaning Errors",
                border_style="red"
            )
            console.print(error_panel)
    
    def display_optimization_results(self, opt_result: OptimizationResult):
        """Display optimization results in a user-friendly format."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        # Create results table
        table = Table(title="⚡ System Optimization Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Optimizations Applied", f"{opt_result.optimizations_applied}")
        table.add_row("Performance Improvement", f"{opt_result.performance_improvement:.1f}%")
        table.add_row("Optimization Duration", f"{opt_result.optimization_duration:.2f}s")
        table.add_row("Startup Items Optimized", f"{opt_result.startup_items_optimized}")
        table.add_row("Memory Optimized", "✅" if opt_result.memory_optimized else "❌")
        table.add_row("Disk Optimized", "✅" if opt_result.disk_optimized else "❌")
        
        console.print(table)
        
        # Display errors if any
        if opt_result.optimization_errors:
            error_panel = Panel(
                "\n".join(opt_result.optimization_errors),
                title="⚠️ Optimization Errors",
                border_style="red"
            )
            console.print(error_panel)
    
    def display_system_status(self, status_info: Dict[str, Any]):
        """Display system status in a user-friendly format."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        # Create status table
        table = Table(title="📈 System Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in status_info.items():
            if key != "ai_insights":
                if isinstance(value, (int, float)):
                    if "bytes" in key.lower() or "size" in key.lower():
                        table.add_row(key.replace("_", " ").title(), self._format_bytes(value))
                    else:
                        table.add_row(key.replace("_", " ").title(), f"{value:,}")
                else:
                    table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(table)
        
        # Display AI insights if available
        if "ai_insights" in status_info:
            insights_panel = Panel(
                status_info["ai_insights"],
                title="🤖 AI Insights",
                border_style="blue"
            )
            console.print(insights_panel)
    
    def display_report(self, report_data: Dict[str, Any], output_file: Optional[str] = None):
        """Display comprehensive system report."""
        from rich.console import Console
        from rich.panel import Panel
        from rich.markdown import Markdown
        
        console = Console()
        
        # Display report content
        if "markdown" in report_data:
            md = Markdown(report_data["markdown"])
            console.print(md)
        else:
            console.print(Panel(str(report_data), title="📊 System Report"))
        
        # Save to file if requested
        if output_file:
            self._save_report_to_file(report_data, output_file)
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human-readable string."""
        if bytes_value == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while bytes_value >= 1024 and i < len(size_names) - 1:
            bytes_value /= 1024.0
            i += 1
        
        return f"{bytes_value:.1f} {size_names[i]}"
    
    def _save_results_to_file(self, results: Any, output_file: str):
        """Save results to file."""
        try:
            import json
            with open(output_file, 'w') as f:
                json.dump(results.__dict__, f, indent=2, default=str)
            logger.info(f"Results saved to: {output_file}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    
    def _save_report_to_file(self, report_data: Dict[str, Any], output_file: str):
        """Save report to file."""
        try:
            if output_file.endswith('.md'):
                with open(output_file, 'w') as f:
                    f.write(report_data.get('markdown', str(report_data)))
            else:
                import json
                with open(output_file, 'w') as f:
                    json.dump(report_data, f, indent=2, default=str)
            logger.info(f"Report saved to: {output_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}") 