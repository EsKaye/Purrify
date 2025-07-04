"""
Purrify Core Engine

This module contains the main PurrifyEngine class that orchestrates
all system optimization operations including scanning, cleaning,
and performance optimization.

The engine provides:
- Comprehensive system scanning with AI-powered analysis
- Safe system cleaning with backup creation
- Performance optimization with real-time monitoring
- Cross-platform compatibility and safety measures
- Detailed reporting and result visualization

Classes:
    ScanResult: Results from system scanning operations
    CleanResult: Results from system cleaning operations  
    OptimizationResult: Results from optimization operations
    PurrifyEngine: Main orchestration engine

Author: Purrify Team
Version: 2.0.0
License: MIT
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
    """
    Results from system scanning operation.
    
    This dataclass contains comprehensive information about files found
    during system scanning, including categorization, potential savings,
    and detailed analysis results.
    
    Attributes:
        total_files_scanned: Total number of files processed
        cache_files_found: Number of cache files identified
        temp_files_found: Number of temporary files found
        log_files_found: Number of log files discovered
        large_files_found: Number of large files (>10MB) identified
        potential_space_savings: Total potential space savings in bytes
        scan_duration: Time taken for scan operation in seconds
        scan_errors: List of errors encountered during scanning
        file_details: Detailed breakdown of files by category
    """
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
    """
    Results from system cleaning operation.
    
    This dataclass contains information about files cleaned, space freed,
    and backup operations performed during system cleaning.
    
    Attributes:
        files_cleaned: Number of files successfully cleaned
        space_freed: Total space freed in bytes
        clean_duration: Time taken for cleaning operation in seconds
        clean_errors: List of errors encountered during cleaning
        backup_created: Whether a backup was created before cleaning
        backup_path: Path to the created backup (if any)
    """
    files_cleaned: int = 0
    space_freed: int = 0  # in bytes
    clean_duration: float = 0.0
    clean_errors: List[str] = field(default_factory=list)
    backup_created: bool = False
    backup_path: Optional[str] = None


@dataclass
class OptimizationResult:
    """
    Results from system optimization operation.
    
    This dataclass contains information about optimizations applied,
    performance improvements achieved, and system enhancements made.
    
    Attributes:
        optimizations_applied: Number of optimizations successfully applied
        performance_improvement: Overall performance improvement percentage
        optimization_duration: Time taken for optimization in seconds
        optimization_errors: List of errors encountered during optimization
        startup_items_optimized: Number of startup items optimized
        memory_optimized: Whether memory optimization was performed
        disk_optimized: Whether disk optimization was performed
    """
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
    
    The engine provides a unified interface for:
    - Comprehensive system scanning with enhanced capabilities
    - Safe system cleaning with automatic backup creation
    - Performance optimization with real-time monitoring
    - AI-powered analysis and recommendations
    - Detailed reporting and result visualization
    
    Attributes:
        config: Configuration object containing all settings
        platform: Platform information and capabilities
        scanner: System scanner for file discovery and analysis
        cleaner: Cache cleaner for safe file removal
        optimizer: Performance optimizer for system enhancement
        ai_engine: AI intelligence engine for analysis
        report_generator: Report generator for detailed output
        operation_history: History of all operations performed
        last_scan_result: Results from the most recent scan
        last_clean_result: Results from the most recent cleaning
        last_optimization_result: Results from the most recent optimization
    """
    
    def __init__(self, config: Config) -> None:
        """
        Initialize the Purrify engine with configuration.
        
        Sets up all core components including scanner, cleaner, optimizer,
        AI engine, and report generator. Initializes platform detection
        and operation tracking.
        
        Args:
            config: Configuration object containing all system settings,
                   scanning preferences, and optimization parameters
                   
        Raises:
            ValueError: If configuration is invalid or missing required settings
            RuntimeError: If platform detection fails or components can't be initialized
        """
        if not config:
            raise ValueError("Configuration object is required")
            
        self.config = config
        self.platform = detect_platform()
        
        # Initialize core components with error handling
        try:
            self.scanner = SystemScanner(config)
            self.cleaner = CacheCleaner(config)
            self.optimizer = PerformanceOptimizer(config)
            self.ai_engine = IntelligenceEngine(config)
            self.report_generator = ReportGenerator(config)
        except Exception as e:
            logger.error(f"Failed to initialize engine components: {e}")
            raise RuntimeError(f"Engine initialization failed: {e}")
        
        # Performance tracking and history
        self.operation_history: List[Dict[str, Any]] = []
        self.last_scan_result: Optional[ScanResult] = None
        self.last_clean_result: Optional[CleanResult] = None
        self.last_optimization_result: Optional[OptimizationResult] = None
        
        logger.info("PurrifyEngine initialized successfully")
        logger.info(f"Platform detected: {self.platform.get('platform_type', 'Unknown')}")
    
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
        
        This method orchestrates a complete system scan using the enhanced
        scanner with AI-powered analysis. It can operate in different modes
        for speed vs. thoroughness trade-offs.
        
        The scan includes:
        - System caches and temporary files
        - Browser caches and application data
        - Duplicate file detection (optional)
        - Photo analysis for compression opportunities (optional)
        - Large file identification (optional)
        - AI-powered risk assessment and recommendations
        
        Args:
            quick_mode: Enable quick scan mode for faster results (skips detailed analysis)
            detailed_mode: Enable detailed scan with comprehensive file analysis
            include_duplicates: Scan for duplicate files using MD5 hashing
            include_photos: Analyze photos for compression and optimization opportunities
            include_large_files: Identify large files (>10MB) for potential optimization
            
        Returns:
            ScanResult object containing comprehensive scan findings including
            file counts, potential savings, and detailed categorization
            
        Raises:
            RuntimeError: If scanning fails due to system errors or permissions
            ValueError: If scan parameters are invalid
            
        Example:
            >>> engine = PurrifyEngine(config)
            >>> result = await engine.scan_system(quick_mode=True)
            >>> print(f"Found {result.total_files_scanned} files")
            >>> print(f"Potential savings: {result.potential_space_savings} bytes")
        """
        logger.info("Starting enhanced system scan...")
        logger.info(f"Scan mode: quick={quick_mode}, detailed={detailed_mode}")
        logger.info(f"Features: duplicates={include_duplicates}, photos={include_photos}, large_files={include_large_files}")
        
        start_time = time.time()
        
        try:
            # Validate scan parameters
            self._validate_scan_parameters(quick_mode, detailed_mode, include_duplicates, include_photos, include_large_files)
            
            # Perform enhanced system scan
            scan_data = await self.scanner.scan_system(
                quick_mode=quick_mode,
                detailed_mode=detailed_mode,
                include_duplicates=include_duplicates,
                include_photos=include_photos,
                include_large_files=include_large_files
            )
            
            # Convert enhanced dictionary result to ScanResult object
            scan_result = self._create_scan_result_from_data(scan_data, start_time)
            
            # Apply AI analysis if enabled
            if self.config.ai.enable_ml_analysis:
                scan_result = await self._apply_ai_analysis(scan_result)
            
            # Update tracking and history
            self._update_scan_tracking(scan_result, start_time)
            
            # Log comprehensive results
            self._log_scan_results(scan_result, scan_data)
            
            return scan_result
            
        except Exception as e:
            logger.error(f"Enhanced system scan failed: {e}")
            error_result = self._create_error_scan_result(str(e), start_time)
            return error_result
    
    async def clean_system(
        self,
        clean_options: Dict[str, bool],
        safe_mode: bool = True,
        create_backup: bool = True
    ) -> CleanResult:
        """
        Clean system caches and temporary files safely.
        
        This method performs safe system cleaning with automatic backup creation
        and comprehensive error handling. It can clean various types of files
        based on the provided options.
        
        Cleaning operations include:
        - System cache files and temporary data
        - Browser caches and application data
        - Log files and temporary downloads
        - Duplicate files (if identified)
        - Old files based on age criteria
        
        Args:
            clean_options: Dictionary specifying what to clean with boolean flags:
                - 'system_caches': Clean system cache directories
                - 'user_caches': Clean user-specific cache files
                - 'browser_caches': Clean browser cache and data
                - 'temp_files': Clean temporary files
                - 'log_files': Clean log files
                - 'duplicates': Clean duplicate files (if found)
                - 'old_files': Clean files older than specified age
            safe_mode: Enable safe mode (preview only, no actual deletion)
            create_backup: Create backup before cleaning operations
            
        Returns:
            CleanResult object containing cleaning results, space freed,
            and backup information
            
        Raises:
            ValueError: If clean options are invalid
            RuntimeError: If cleaning fails due to system errors
            PermissionError: If insufficient permissions for cleaning
            
        Example:
            >>> clean_opts = {'system_caches': True, 'temp_files': True}
            >>> result = await engine.clean_system(clean_opts, safe_mode=True)
            >>> print(f"Freed {result.space_freed} bytes")
        """
        logger.info("Starting system cleaning...")
        logger.info(f"Clean options: {clean_options}")
        logger.info(f"Safe mode: {safe_mode}, Backup: {create_backup}")
        
        start_time = time.time()
        
        try:
            # Validate cleaning parameters
            self._validate_clean_parameters(clean_options, safe_mode, create_backup)
            
            # Create backup if requested
            backup_path = None
            if create_backup and not safe_mode:
                backup_path = await self._create_backup()
            
            # Perform cleaning operations
            clean_result = await self.cleaner.clean_system(
                clean_options=clean_options,
                safe_mode=safe_mode,
                backup_path=backup_path
            )
            
            # Update tracking and history
            clean_result.clean_duration = time.time() - start_time
            self.last_clean_result = clean_result
            self._add_to_operation_history('clean', clean_result)
            
            # Log results
            logger.info(f"System cleaning completed in {clean_result.clean_duration:.2f}s")
            logger.info(f"Files cleaned: {clean_result.files_cleaned}")
            logger.info(f"Space freed: {self._format_bytes(clean_result.space_freed)}")
            
            return clean_result
            
        except Exception as e:
            logger.error(f"System cleaning failed: {e}")
            error_result = self._create_error_clean_result(str(e), start_time)
            return error_result
    
    async def optimize_system(
        self,
        optimization_options: Dict[str, bool],
        safe_mode: bool = True
    ) -> OptimizationResult:
        """
        Optimize system performance and startup.
        
        This method applies various system optimizations to improve
        performance, reduce startup time, and enhance overall system
        efficiency.
        
        Optimization operations include:
        - Startup item management and optimization
        - Memory optimization and cleanup
        - Disk optimization and defragmentation
        - Service optimization and management
        - Registry cleanup (Windows)
        - System preference optimization (macOS)
        
        Args:
            optimization_options: Dictionary specifying optimizations to apply:
                - 'startup_items': Optimize startup programs and services
                - 'memory': Perform memory optimization and cleanup
                - 'disk': Optimize disk performance and cleanup
                - 'services': Optimize system services
                - 'registry': Clean registry (Windows only)
                - 'preferences': Optimize system preferences (macOS only)
            safe_mode: Enable safe mode (preview only, no actual changes)
            
        Returns:
            OptimizationResult object containing optimization results,
            performance improvements, and applied optimizations
            
        Raises:
            ValueError: If optimization options are invalid
            RuntimeError: If optimization fails due to system errors
            PermissionError: If insufficient permissions for optimization
            
        Example:
            >>> opt_opts = {'startup_items': True, 'memory': True}
            >>> result = await engine.optimize_system(opt_opts, safe_mode=True)
            >>> print(f"Performance improvement: {result.performance_improvement}%")
        """
        logger.info("Starting system optimization...")
        logger.info(f"Optimization options: {optimization_options}")
        logger.info(f"Safe mode: {safe_mode}")
        
        start_time = time.time()
        
        try:
            # Validate optimization parameters
            self._validate_optimization_parameters(optimization_options, safe_mode)
            
            # Perform optimization operations
            opt_result = await self.optimizer.optimize_system(
                optimization_options=optimization_options,
                safe_mode=safe_mode
            )
            
            # Update tracking and history
            opt_result.optimization_duration = time.time() - start_time
            self.last_optimization_result = opt_result
            self._add_to_operation_history('optimize', opt_result)
            
            # Log results
            logger.info(f"System optimization completed in {opt_result.optimization_duration:.2f}s")
            logger.info(f"Optimizations applied: {opt_result.optimizations_applied}")
            logger.info(f"Performance improvement: {opt_result.performance_improvement:.2f}%")
            
            return opt_result
            
        except Exception as e:
            logger.error(f"System optimization failed: {e}")
            error_result = self._create_error_optimization_result(str(e), start_time)
            return error_result
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status and health information.
        
        This method provides detailed information about the current
        system state, including disk usage, memory status, performance
        metrics, and optimization opportunities.
        
        Returns:
            Dictionary containing comprehensive system status including:
            - Platform information and capabilities
            - Disk usage and space availability
            - Memory usage and performance
            - System health indicators
            - Recent operation history
            - Optimization recommendations
            
        Example:
            >>> status = await engine.get_system_status()
            >>> print(f"Disk usage: {status['disk_usage']['percent']}%")
            >>> print(f"Memory usage: {status['memory_usage']['percent']}%")
        """
        logger.info("Getting system status...")
        
        try:
            # Get basic system information
            status_info = await self.scanner.get_system_status()
            
            # Add engine-specific information
            status_info.update({
                'engine_info': {
                    'version': '2.0.0',
                    'platform': self.platform,
                    'last_scan': self.last_scan_result.scan_duration if self.last_scan_result else None,
                    'last_clean': self.last_clean_result.clean_duration if self.last_clean_result else None,
                    'last_optimization': self.last_optimization_result.optimization_duration if self.last_optimization_result else None
                },
                'operation_history': self.operation_history[-10:],  # Last 10 operations
                'ai_enabled': self.config.ai.enable_ml_analysis
            })
            
            logger.info("System status retrieved successfully")
            return status_info
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {'error': str(e)}
    
    async def generate_report(self, detailed: bool = False) -> Dict[str, Any]:
        """
        Generate comprehensive system optimization report.
        
        This method creates a detailed report of all system operations,
        including scan results, cleaning operations, optimizations applied,
        and recommendations for future maintenance.
        
        Args:
            detailed: Include detailed file-level information in report
            
        Returns:
            Dictionary containing comprehensive report data including:
            - Executive summary of all operations
            - Detailed scan results and findings
            - Cleaning operations and space freed
            - Optimization results and improvements
            - System health assessment
            - Recommendations for future maintenance
            
        Example:
            >>> report = await engine.generate_report(detailed=True)
            >>> print(f"Total space freed: {report['summary']['total_space_freed']}")
        """
        logger.info(f"Generating {'detailed' if detailed else 'summary'} report...")
        
        try:
            report_data = await self.report_generator.generate_report(
                scan_result=self.last_scan_result,
                clean_result=self.last_clean_result,
                optimization_result=self.last_optimization_result,
                detailed=detailed
            )
            
            logger.info("Report generated successfully")
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {'error': str(e)}
    
    # Private helper methods for improved modularity
    
    def _validate_scan_parameters(
        self,
        quick_mode: bool,
        detailed_mode: bool,
        include_duplicates: bool,
        include_photos: bool,
        include_large_files: bool
    ) -> None:
        """Validate scan parameters for consistency and correctness."""
        if quick_mode and detailed_mode:
            raise ValueError("Cannot enable both quick_mode and detailed_mode")
        
        if quick_mode and (include_duplicates or include_photos):
            logger.warning("Quick mode enabled - detailed analysis features will be skipped")
    
    def _validate_clean_parameters(
        self,
        clean_options: Dict[str, bool],
        safe_mode: bool,
        create_backup: bool
    ) -> None:
        """Validate cleaning parameters for safety and correctness."""
        if not clean_options:
            raise ValueError("Clean options cannot be empty")
        
        if not safe_mode and not create_backup:
            logger.warning("Safe mode disabled without backup - this may be risky")
    
    def _validate_optimization_parameters(
        self,
        optimization_options: Dict[str, bool],
        safe_mode: bool
    ) -> None:
        """Validate optimization parameters for safety and correctness."""
        if not optimization_options:
            raise ValueError("Optimization options cannot be empty")
        
        if not safe_mode:
            logger.warning("Safe mode disabled for optimization - changes will be applied")
    
    def _create_scan_result_from_data(self, scan_data: Dict[str, Any], start_time: float) -> ScanResult:
        """Create ScanResult object from scanner data."""
        return ScanResult(
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
            scan_duration=time.time() - start_time,
            scan_errors=scan_data.get("errors", []),
            file_details=scan_data.get("categories", {})
        )
    
    async def _apply_ai_analysis(self, scan_result: ScanResult) -> ScanResult:
        """Apply AI analysis to scan results if enabled."""
        try:
            return await self.ai_engine.analyze_scan_results(scan_result)
        except Exception as e:
            logger.warning(f"AI analysis failed: {e}")
            return scan_result
    
    def _update_scan_tracking(self, scan_result: ScanResult, start_time: float) -> None:
        """Update scan tracking and history."""
        scan_result.scan_duration = time.time() - start_time
        self.last_scan_result = scan_result
        self._add_to_operation_history('scan', scan_result)
    
    def _log_scan_results(self, scan_result: ScanResult, scan_data: Dict[str, Any]) -> None:
        """Log comprehensive scan results."""
        logger.info(f"Enhanced system scan completed in {scan_result.scan_duration:.2f}s")
        logger.info(f"Found {scan_result.total_files_scanned} files")
        logger.info(f"Found {scan_data.get('duplicates', {}).get('groups', 0)} duplicate groups")
        logger.info(f"Analyzed {scan_data.get('photos', {}).get('count', 0)} photos")
        logger.info(f"Potential space savings: {self._format_bytes(scan_result.potential_space_savings)}")
    
    def _create_error_scan_result(self, error: str, start_time: float) -> ScanResult:
        """Create error scan result with failure information."""
        return ScanResult(
            scan_errors=[error],
            scan_duration=time.time() - start_time
        )
    
    def _create_error_clean_result(self, error: str, start_time: float) -> CleanResult:
        """Create error clean result with failure information."""
        return CleanResult(
            clean_errors=[error],
            clean_duration=time.time() - start_time
        )
    
    def _create_error_optimization_result(self, error: str, start_time: float) -> OptimizationResult:
        """Create error optimization result with failure information."""
        return OptimizationResult(
            optimization_errors=[error],
            optimization_duration=time.time() - start_time
        )
    
    def _add_to_operation_history(self, operation_type: str, result: Any) -> None:
        """Add operation to history for tracking and reporting."""
        history_entry = {
            'timestamp': time.time(),
            'operation': operation_type,
            'duration': getattr(result, f'{operation_type}_duration', 0.0),
            'success': len(getattr(result, f'{operation_type}_errors', [])) == 0
        }
        self.operation_history.append(history_entry)
    
    async def _create_backup(self) -> Optional[str]:
        """Create backup before cleaning operations."""
        try:
            backup_path = await self.cleaner.create_backup(Path("backups"))
            logger.info(f"Backup created at: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

    # Display and formatting methods
    
    def display_scan_results(self, scan_result: ScanResult, output_file: Optional[str] = None) -> None:
        """
        Display scan results in a formatted, user-friendly manner.
        
        This method provides comprehensive visualization of scan results
        including file counts, potential savings, and detailed breakdowns
        by category.
        
        Args:
            scan_result: ScanResult object containing scan findings
            output_file: Optional file path to save results
            
        Example:
            >>> engine.display_scan_results(scan_result)
            >>> engine.display_scan_results(scan_result, "scan_results.txt")
        """
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            from rich.text import Text
            
            console = Console()
            
            # Display main results
            console.print(Panel(
                f"🔍 System Scan Results\n"
                f"Duration: {scan_result.scan_duration:.2f}s\n"
                f"Files Scanned: {scan_result.total_files_scanned:,}\n"
                f"Potential Savings: {self._format_bytes(scan_result.potential_space_savings)}",
                title="📊 Scan Summary",
                border_style="blue"
            ))
            
            # Display file categories
            if scan_result.file_details:
                categories_table = Table(title="📁 File Categories")
                categories_table.add_column("Category", style="cyan")
                categories_table.add_column("Count", style="green")
                categories_table.add_column("Size", style="yellow")
                
                for category, data in scan_result.file_details.items():
                    if isinstance(data, dict) and 'count' in data:
                        categories_table.add_row(
                            category.replace('_', ' ').title(),
                            f"{data.get('count', 0):,}",
                            self._format_bytes(data.get('total_size', 0))
                        )
                
                console.print(categories_table)
            
            # Display enhanced results if available
            if isinstance(scan_result.file_details, dict):
                # Duplicates section
                duplicates = scan_result.file_details.get("duplicates", {})
                if duplicates.get("count", 0) > 0:
                    dup_table = Table(title="🔄 Duplicate Files")
                    dup_table.add_column("Metric", style="cyan")
                    dup_table.add_column("Value", style="green")
                    
                    dup_table.add_row("Duplicate Groups", f"{duplicates.get('groups', 0)}")
                    dup_table.add_row("Total Duplicate Size", self._format_bytes(duplicates.get('total_size', 0)))
                    dup_table.add_row("Potential Savings", self._format_bytes(duplicates.get('potential_savings', 0)))
                    
                    console.print(dup_table)
                
                # Photos section
                photos = scan_result.file_details.get("photos", {})
                if photos.get("count", 0) > 0:
                    photo_table = Table(title="📸 Photo Analysis")
                    photo_table.add_column("Metric", style="cyan")
                    photo_table.add_column("Value", style="green")
                    
                    photo_table.add_row("Photos Analyzed", f"{photos.get('count', 0)}")
                    photo_table.add_row("Total Photo Size", self._format_bytes(photos.get('total_size', 0)))
                    photo_table.add_row("Compression Potential", self._format_bytes(photos.get('compression_potential', 0)))
                    
                    console.print(photo_table)
                
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
                console.print(f"📄 Results saved to: {output_file}")
                
        except ImportError:
            # Fallback to simple text output if rich is not available
            print(f"Scan Results:")
            print(f"Duration: {scan_result.scan_duration:.2f}s")
            print(f"Files Scanned: {scan_result.total_files_scanned:,}")
            print(f"Potential Savings: {self._format_bytes(scan_result.potential_space_savings)}")
            
            if scan_result.scan_errors:
                print(f"Errors: {scan_result.scan_errors}")
    
    def display_clean_results(self, clean_result: CleanResult) -> None:
        """
        Display cleaning results in a formatted, user-friendly manner.
        
        Args:
            clean_result: CleanResult object containing cleaning results
        """
        try:
            from rich.console import Console
            from rich.panel import Panel
            
            console = Console()
            
            console.print(Panel(
                f"🧹 System Cleaning Results\n"
                f"Duration: {clean_result.clean_duration:.2f}s\n"
                f"Files Cleaned: {clean_result.files_cleaned:,}\n"
                f"Space Freed: {self._format_bytes(clean_result.space_freed)}\n"
                f"Backup Created: {'✅' if clean_result.backup_created else '❌'}",
                title="📊 Cleaning Summary",
                border_style="green"
            ))
            
            if clean_result.clean_errors:
                error_panel = Panel(
                    "\n".join(clean_result.clean_errors),
                    title="⚠️ Cleaning Errors",
                    border_style="red"
                )
                console.print(error_panel)
                
        except ImportError:
            print(f"Cleaning Results:")
            print(f"Duration: {clean_result.clean_duration:.2f}s")
            print(f"Files Cleaned: {clean_result.files_cleaned:,}")
            print(f"Space Freed: {self._format_bytes(clean_result.space_freed)}")
    
    def display_optimization_results(self, opt_result: OptimizationResult) -> None:
        """
        Display optimization results in a formatted, user-friendly manner.
        
        Args:
            opt_result: OptimizationResult object containing optimization results
        """
        try:
            from rich.console import Console
            from rich.panel import Panel
            
            console = Console()
            
            console.print(Panel(
                f"⚡ System Optimization Results\n"
                f"Duration: {opt_result.optimization_duration:.2f}s\n"
                f"Optimizations Applied: {opt_result.optimizations_applied}\n"
                f"Performance Improvement: {opt_result.performance_improvement:.2f}%\n"
                f"Startup Items Optimized: {opt_result.startup_items_optimized}",
                title="📊 Optimization Summary",
                border_style="yellow"
            ))
            
            if opt_result.optimization_errors:
                error_panel = Panel(
                    "\n".join(opt_result.optimization_errors),
                    title="⚠️ Optimization Errors",
                    border_style="red"
                )
                console.print(error_panel)
                
        except ImportError:
            print(f"Optimization Results:")
            print(f"Duration: {opt_result.optimization_duration:.2f}s")
            print(f"Optimizations Applied: {opt_result.optimizations_applied}")
            print(f"Performance Improvement: {opt_result.performance_improvement:.2f}%")
    
    def display_system_status(self, status_info: Dict[str, Any]) -> None:
        """
        Display system status in a formatted, user-friendly manner.
        
        Args:
            status_info: Dictionary containing system status information
        """
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            
            console = Console()
            
            # System overview
            console.print(Panel(
                f"🖥️ System Status\n"
                f"Platform: {status_info.get('platform', {}).get('platform_type', 'Unknown')}\n"
                f"Architecture: {status_info.get('platform', {}).get('architecture', 'Unknown')}\n"
                f"Python Version: {status_info.get('platform', {}).get('python_version', 'Unknown')}",
                title="📊 System Overview",
                border_style="blue"
            ))
            
            # Disk usage
            if 'disk_usage' in status_info:
                disk_table = Table(title="💾 Disk Usage")
                disk_table.add_column("Metric", style="cyan")
                disk_table.add_column("Value", style="green")
                
                disk_usage = status_info['disk_usage']
                disk_table.add_row("Total Space", self._format_bytes(disk_usage.get('total', 0)))
                disk_table.add_row("Used Space", self._format_bytes(disk_usage.get('used', 0)))
                disk_table.add_row("Free Space", self._format_bytes(disk_usage.get('free', 0)))
                disk_table.add_row("Usage Percentage", f"{disk_usage.get('percent', 0):.1f}%")
                
                console.print(disk_table)
            
            # Memory usage
            if 'memory_usage' in status_info:
                mem_table = Table(title="🧠 Memory Usage")
                mem_table.add_column("Metric", style="cyan")
                mem_table.add_column("Value", style="green")
                
                mem_usage = status_info['memory_usage']
                mem_table.add_row("Total Memory", self._format_bytes(mem_usage.get('total', 0)))
                mem_table.add_row("Used Memory", self._format_bytes(mem_usage.get('used', 0)))
                mem_table.add_row("Free Memory", self._format_bytes(mem_usage.get('free', 0)))
                mem_table.add_row("Usage Percentage", f"{mem_usage.get('percent', 0):.1f}%")
                
                console.print(mem_table)
                
        except ImportError:
            print(f"System Status:")
            print(f"Platform: {status_info.get('platform', {}).get('platform_type', 'Unknown')}")
            if 'disk_usage' in status_info:
                disk = status_info['disk_usage']
                print(f"Disk Usage: {disk.get('percent', 0):.1f}%")
            if 'memory_usage' in status_info:
                mem = status_info['memory_usage']
                print(f"Memory Usage: {mem.get('percent', 0):.1f}%")
    
    def display_report(self, report_data: Dict[str, Any], output_file: Optional[str] = None) -> None:
        """
        Display comprehensive system report in a formatted manner.
        
        Args:
            report_data: Dictionary containing report data
            output_file: Optional file path to save report
        """
        try:
            from rich.console import Console
            from rich.panel import Panel
            
            console = Console()
            
            # Display report summary
            if 'summary' in report_data:
                summary = report_data['summary']
                console.print(Panel(
                    f"📋 System Optimization Report\n"
                    f"Generated: {summary.get('timestamp', 'Unknown')}\n"
                    f"Total Operations: {summary.get('total_operations', 0)}\n"
                    f"Space Freed: {self._format_bytes(summary.get('total_space_freed', 0))}\n"
                    f"Performance Improvement: {summary.get('overall_performance_improvement', 0):.2f}%",
                    title="📊 Report Summary",
                    border_style="blue"
                ))
            
            # Save to file if requested
            if output_file:
                self._save_report_to_file(report_data, output_file)
                console.print(f"📄 Report saved to: {output_file}")
                
        except ImportError:
            print("System Optimization Report")
            if 'summary' in report_data:
                summary = report_data['summary']
                print(f"Total Operations: {summary.get('total_operations', 0)}")
                print(f"Space Freed: {self._format_bytes(summary.get('total_space_freed', 0))}")
    
    def _format_bytes(self, bytes_value: int) -> str:
        """
        Format bytes into human-readable string.
        
        Args:
            bytes_value: Number of bytes to format
            
        Returns:
            Formatted string with appropriate unit (B, KB, MB, GB, TB)
        """
        if bytes_value == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        
        while bytes_value >= 1024 and unit_index < len(units) - 1:
            bytes_value /= 1024
            unit_index += 1
        
        return f"{bytes_value:.2f} {units[unit_index]}"
    
    def _save_results_to_file(self, results: Any, output_file: str) -> None:
        """Save results to file in a readable format."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Purrify Scan Results\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Duration: {results.scan_duration:.2f}s\n")
                f.write(f"Files Scanned: {results.total_files_scanned:,}\n")
                f.write(f"Potential Savings: {self._format_bytes(results.potential_space_savings)}\n")
                
                if results.scan_errors:
                    f.write(f"\nErrors:\n")
                    for error in results.scan_errors:
                        f.write(f"- {error}\n")
        except Exception as e:
            logger.error(f"Failed to save results to file: {e}")
    
    def _save_report_to_file(self, report_data: Dict[str, Any], output_file: str) -> None:
        """Save report to file in a readable format."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Purrify System Optimization Report\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if 'summary' in report_data:
                    summary = report_data['summary']
                    f.write(f"Summary:\n")
                    f.write(f"- Total Operations: {summary.get('total_operations', 0)}\n")
                    f.write(f"- Space Freed: {self._format_bytes(summary.get('total_space_freed', 0))}\n")
                    f.write(f"- Performance Improvement: {summary.get('overall_performance_improvement', 0):.2f}%\n")
        except Exception as e:
            logger.error(f"Failed to save report to file: {e}")
    
    def run(self) -> None:
        """
        Run the Purrify engine in interactive mode.
        
        This method provides an interactive interface for running
        system optimization operations with user input and real-time
        feedback.
        """
        logger.info("Starting Purrify engine in interactive mode")
        # Interactive mode implementation would go here
        # For now, this is a placeholder for future enhancement
        logger.info("Interactive mode not yet implemented")
    
    @staticmethod
    def launch_gui() -> None:
        """
        Launch the Purrify GUI interface.
        
        This static method provides a convenient way to launch
        the graphical user interface for Purrify.
        """
        try:
            from ..gui import PurrifyGUI
            app = PurrifyGUI()
            app.run()
        except ImportError as e:
            logger.error(f"Failed to import GUI components: {e}")
            print("GUI not available. Please install GUI dependencies.")
        except Exception as e:
            logger.error(f"Failed to launch GUI: {e}")
            print(f"GUI launch failed: {e}") 