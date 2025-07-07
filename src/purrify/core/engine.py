"""
Purrify Core Engine

This module provides the main engine for system scanning, optimization,
and cleaning operations with comprehensive Windows 11 support.
"""

import asyncio
import os
import time
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger

from .config import Config
from .logger import setup_logger
from ..scanners.system_scanner import SystemScanner
from ..optimizers.performance_optimizer import PerformanceOptimizer
from ..cleaners.cache_cleaner import CacheCleaner
from ..utils.platform import detect_platform, get_system_paths, format_bytes
from ..optimizers.script_generator import ScriptGenerator


class PurrifyEngine:
    """
    Main engine for Purrify system optimization operations.
    
    This class coordinates scanning, optimization, and cleaning operations
    with comprehensive Windows 11 support and LilithOS detection.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the Purrify engine.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.platform = detect_platform()
        self.scanner = SystemScanner(config)
        self.optimizer = PerformanceOptimizer(config)
        self.cleaner = CacheCleaner(config)
        
        # Setup logging
        setup_logger(verbose=config.logging.verbose)
        
        logger.info("PurrifyEngine initialized")
        logger.info(f"Platform: {self.platform.get('platform_type', 'Unknown')}")
        
        # Check for LilithOS references
        self.lilithos_paths = self._detect_lilithos_references()
    
    def _detect_lilithos_references(self) -> List[str]:
        """Detect LilithOS references in the system."""
        lilithos_paths = []
        
        # Common LilithOS paths to check
        potential_paths = [
            "C:/LilithOS",
            "C:/Program Files/LilithOS",
            "C:/ProgramData/LilithOS",
            os.path.expanduser("~/LilithOS"),
            os.path.expanduser("~/AppData/Local/LilithOS"),
            os.path.expanduser("~/AppData/Roaming/LilithOS"),
        ]
        
        for path in potential_paths:
            if os.path.exists(path):
                lilithos_paths.append(path)
                logger.info(f"Found LilithOS reference: {path}")
        
        return lilithos_paths
    
    async def scan_system(
        self,
        quick_mode: bool = False,
        detailed_mode: bool = False,
        include_duplicates: bool = True,
        include_photos: bool = True,
        include_large_files: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive system scan with LilithOS detection.
        
        Args:
            quick_mode: Enable quick scan mode
            detailed_mode: Enable detailed scan with file analysis
            include_duplicates: Scan for duplicate files
            include_photos: Analyze photos for optimization
            include_large_files: Identify large files
            
        Returns:
            Dictionary containing scan results
        """
        logger.info("Starting comprehensive system scan...")
        
        # Perform standard system scan
        scan_results = await self.scanner.scan_system(
            quick_mode=quick_mode,
            detailed_mode=detailed_mode,
            include_duplicates=include_duplicates,
            include_photos=include_photos,
            include_large_files=include_large_files
        )
        
        # Add LilithOS specific scanning
        lilithos_results = await self._scan_lilithos_references()
        scan_results["lilithos_references"] = lilithos_results
        
        # Add redundant folder detection
        redundant_results = await self._scan_redundant_folders()
        scan_results["redundant_folders"] = redundant_results
        
        return scan_results
    
    async def _scan_lilithos_references(self) -> Dict[str, Any]:
        """Scan for LilithOS references and redundant files."""
        logger.info("Scanning for LilithOS references...")
        
        lilithos_data = {
            "paths_found": self.lilithos_paths,
            "total_size": 0,
            "files_count": 0,
            "redundant_files": [],
            "safe_to_clean": []
        }
        
        for path in self.lilithos_paths:
            try:
                path_obj = Path(path)
                if path_obj.exists():
                    # Calculate size and file count
                    total_size = 0
                    file_count = 0
                    
                    for file_path in path_obj.rglob("*"):
                        if file_path.is_file():
                            file_size = file_path.stat().st_size
                            total_size += file_size
                            file_count += 1
                            
                            # Check if file is redundant
                            if self._is_redundant_file(file_path):
                                lilithos_data["redundant_files"].append({
                                    "path": str(file_path),
                                    "size": file_size,
                                    "type": "redundant"
                                })
                    
                    lilithos_data["total_size"] += total_size
                    lilithos_data["files_count"] += file_count
                    
                    # Mark as safe to clean if it's a cache or temp directory
                    if any(keyword in path.lower() for keyword in ["cache", "temp", "tmp", "log"]):
                        lilithos_data["safe_to_clean"].append(path)
                        
            except Exception as e:
                logger.warning(f"Error scanning LilithOS path {path}: {e}")
        
        return lilithos_data
    
    async def _scan_redundant_folders(self) -> Dict[str, Any]:
        """Scan for redundant folders in C: drive."""
        logger.info("Scanning for redundant folders in C: drive...")
        
        redundant_data = {
            "folders_found": [],
            "total_size": 0,
            "potential_savings": 0
        }
        
        # Common redundant folder patterns
        redundant_patterns = [
            "*.tmp",
            "*.temp",
            "*.cache",
            "*.log",
            "*.bak",
            "*.old",
            "*.backup",
            "Thumbs.db",
            ".DS_Store",
            "desktop.ini"
        ]
        
        # Scan C: drive for redundant folders
        c_drive = Path("C:/")
        
        try:
            for root, dirs, files in os.walk(c_drive, topdown=True):
                # Skip system directories
                dirs[:] = [d for d in dirs if not self._is_system_directory(d)]
                
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    
                    # Check if directory is redundant
                    if self._is_redundant_directory(dir_path):
                        try:
                            dir_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                            redundant_data["folders_found"].append({
                                "path": str(dir_path),
                                "size": dir_size,
                                "type": "redundant_folder"
                            })
                            redundant_data["total_size"] += dir_size
                        except Exception as e:
                            logger.warning(f"Error calculating size for {dir_path}: {e}")
                            
        except Exception as e:
            logger.warning(f"Error scanning C: drive: {e}")
        
        redundant_data["potential_savings"] = redundant_data["total_size"]
        return redundant_data
    
    def _is_redundant_file(self, file_path: Path) -> bool:
        """Check if a file is redundant."""
        redundant_extensions = {'.tmp', '.temp', '.cache', '.log', '.bak', '.old', '.backup'}
        redundant_names = {'thumbs.db', '.ds_store', 'desktop.ini'}
        
        return (file_path.suffix.lower() in redundant_extensions or 
                file_path.name.lower() in redundant_names)
    
    def _is_redundant_directory(self, dir_path: Path) -> bool:
        """Check if a directory is redundant."""
        redundant_names = {
            'temp', 'tmp', 'cache', 'logs', 'backup', 'old', 'bak',
            'recycler', '$recycle.bin', 'system volume information'
        }
        
        return dir_path.name.lower() in redundant_names
    
    def _is_system_directory(self, dir_name: str) -> bool:
        """Check if a directory is a system directory."""
        system_dirs = {
            'windows', 'program files', 'programdata', 'system32',
            'syswow64', 'winsxs', '$recycle.bin', 'system volume information'
        }
        
        return dir_name.lower() in system_dirs
    
    async def clean_system(
        self,
        clean_options: Dict[str, bool],
        safe_mode: bool = True,
        create_backup: bool = False
    ) -> Dict[str, Any]:
        """
        Clean system files with LilithOS awareness.
        
        Args:
            clean_options: Dictionary specifying what to clean
            safe_mode: Enable safe mode (preview only)
            create_backup: Create backup before cleaning
            
        Returns:
            Dictionary containing cleaning results
        """
        logger.info("Starting system cleaning...")
        
        # Perform standard cleaning
        clean_results = await self.cleaner.clean_system(
            clean_options=clean_options,
            safe_mode=safe_mode
        )
        
        # Add LilithOS specific cleaning
        if not safe_mode:
            lilithos_clean_results = await self._clean_lilithos_references()
            # Convert CleanResult to dict and add LilithOS results
            clean_dict = {
                "files_cleaned": clean_results.files_cleaned,
                "space_freed": clean_results.space_freed,
                "clean_duration": clean_results.clean_duration,
                "clean_errors": clean_results.clean_errors,
                "backup_created": clean_results.backup_created,
                "backup_path": clean_results.backup_path,
                "lilithos_cleaned": lilithos_clean_results
            }
            return clean_dict
        
        return clean_results
    
    async def _clean_lilithos_references(self) -> Dict[str, Any]:
        """Clean LilithOS references safely."""
        logger.info("Cleaning LilithOS references...")
        
        clean_results = {
            "paths_cleaned": [],
            "files_removed": 0,
            "space_freed": 0,
            "errors": []
        }
        
        for path in self.lilithos_paths:
            try:
                path_obj = Path(path)
                if path_obj.exists():
                    # Only clean cache and temp directories
                    if any(keyword in path.lower() for keyword in ["cache", "temp", "tmp", "log"]):
                        if path_obj.is_dir():
                            # Calculate size before removal
                            total_size = sum(f.stat().st_size for f in path_obj.rglob('*') if f.is_file())
                            file_count = sum(1 for f in path_obj.rglob('*') if f.is_file())
                            
                            # Remove directory
                            shutil.rmtree(path)
                            
                            clean_results["paths_cleaned"].append(path)
                            clean_results["files_removed"] += file_count
                            clean_results["space_freed"] += total_size
                            
                            logger.info(f"Cleaned LilithOS path: {path} ({format_bytes(total_size)})")
                            
            except Exception as e:
                error_msg = f"Error cleaning LilithOS path {path}: {e}"
                clean_results["errors"].append(error_msg)
                logger.warning(error_msg)
        
        return clean_results
    
    async def optimize_system(
        self,
        optimization_options: Dict[str, bool],
        safe_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize system performance with Windows 11 support.
        
        Args:
            optimization_options: Dictionary specifying optimization types
            safe_mode: Enable safe mode (preview only)
            
        Returns:
            Dictionary containing optimization results
        """
        logger.info("Starting system optimization...")
        
        # Perform standard optimization
        opt_results = await self.optimizer.optimize_system(
            optimization_options=optimization_options,
            safe_mode=safe_mode
        )
        
        return opt_results
    
    async def generate_report(self, detailed: bool = False) -> Dict[str, Any]:
        """Generate comprehensive system report."""
        logger.info("Generating system report...")
        
        # Get system status
        system_status = await self.scanner.get_system_status()
        
        # Get platform info
        platform_info = detect_platform()
        
        # Get LilithOS info
        lilithos_info = {
            "paths_found": self.lilithos_paths,
            "total_paths": len(self.lilithos_paths)
        }
        
        report = {
            "timestamp": time.time(),
            "platform": platform_info,
            "system_status": system_status,
            "lilithos_info": lilithos_info,
            "detailed": detailed
        }
        
        return report
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return await self.scanner.get_system_status()
    
    def display_scan_results(self, scan_results: Dict[str, Any], output_file: Optional[str] = None):
        """Display scan results in a formatted way."""
        print("\n" + "="*60)
        print("🔍 PURRIFY SYSTEM SCAN RESULTS")
        print("="*60)
        
        # Display standard scan results
        if "total_files" in scan_results:
            print(f"📁 Files Scanned: {scan_results['total_files']:,}")
            print(f"💾 Total Size: {format_bytes(scan_results.get('total_size', 0))}")
            print(f"⏱️  Scan Duration: {scan_results.get('scan_duration', 0):.2f}s")
        elif "total_files_scanned" in scan_results:
            print(f"📁 Files Scanned: {scan_results['total_files_scanned']:,}")
            print(f"💾 Total Size: {format_bytes(scan_results.get('total_size', 0))}")
            print(f"⏱️  Scan Duration: {scan_results.get('scan_duration', 0):.2f}s")
        else:
            print("📁 Files Scanned: 0")
            print("💾 Total Size: 0 B")
            print("⏱️  Scan Duration: 0.00s")
        
        # Display duplicate results
        if "duplicates" in scan_results:
            duplicates = scan_results["duplicates"]
            print(f"\n🔄 Duplicate Files: {duplicates['groups']} groups")
            print(f"💾 Potential Savings: {format_bytes(duplicates['potential_savings'])}")
        elif "duplicate_groups" in scan_results:
            print(f"\n🔄 Duplicate Files: {len(scan_results['duplicate_groups'])} groups")
            print(f"💾 Potential Savings: {format_bytes(scan_results.get('duplicate_savings', 0))}")
        
        # Display photo analysis
        if "photos" in scan_results:
            photos = scan_results["photos"]
            print(f"\n📸 Photos Analyzed: {photos['count']}")
            print(f"💾 Compression Potential: {format_bytes(photos['potential_savings'])}")
        elif "photo_analysis" in scan_results:
            print(f"\n📸 Photos Analyzed: {len(scan_results['photo_analysis'])}")
            print(f"💾 Compression Potential: {format_bytes(scan_results.get('photo_savings', 0))}")
        
        # Display large files
        if "large_files" in scan_results:
            large_files = scan_results["large_files"]
            print(f"\n📦 Large Files: {large_files['count']}")
            print(f"💾 Total Size: {format_bytes(large_files['total_size'])}")
        
        # Display LilithOS results
        if "lilithos_references" in scan_results:
            lilithos = scan_results["lilithos_references"]
            print(f"\n🖤 LilithOS References: {len(lilithos['paths_found'])} paths")
            print(f"💾 Total Size: {format_bytes(lilithos['total_size'])}")
            print(f"📁 Files: {lilithos['files_count']:,}")
            if lilithos['paths_found']:
                print("📍 Paths found:")
                for path in lilithos['paths_found']:
                    print(f"   - {path}")
        
        # Display redundant folders
        if "redundant_folders" in scan_results:
            redundant = scan_results["redundant_folders"]
            print(f"\n🗂️  Redundant Folders: {len(redundant['folders_found'])}")
            print(f"💾 Potential Savings: {format_bytes(redundant['potential_savings'])}")
        
        # Display enhanced scanning results
        if "login_patterns" in scan_results:
            login = scan_results["login_patterns"]
            print(f"\n🔐 Login Patterns: {login['count']} files")
            print(f"💾 Size: {format_bytes(login['size'])}")
        
        if "most_used_files" in scan_results:
            most_used = scan_results["most_used_files"]
            print(f"\n📁 Most Used Files: {most_used['count']} files")
            print(f"💾 Size: {format_bytes(most_used['size'])}")
        
        if "user_directories" in scan_results:
            user_dirs = scan_results["user_directories"]
            print(f"\n👤 User Directories: {user_dirs['count']} files")
            print(f"💾 Size: {format_bytes(user_dirs['size'])}")
        
        if "program_installations" in scan_results:
            programs = scan_results["program_installations"]
            print(f"\n🖥️  Program Installations: {programs['count']} files")
            print(f"💾 Size: {format_bytes(programs['size'])}")
        
        if "critical_machine_files" in scan_results:
            critical = scan_results["critical_machine_files"]
            print(f"\n⚙️  Critical Machine Files: {critical['count']} files")
            print(f"💾 Size: {format_bytes(critical['size'])}")
        
        if "startup_and_services" in scan_results:
            startup = scan_results["startup_and_services"]
            print(f"\n🚀 Startup & Services: {startup['count']} files")
            print(f"💾 Size: {format_bytes(startup['size'])}")
        
        print("\n" + "="*60)
        
        # Save to file if requested
        if output_file:
            self._save_results_to_file(scan_results, output_file)
    
    def display_clean_results(self, clean_results: Dict[str, Any]):
        """Display cleaning results."""
        print("\n" + "="*60)
        print("🧹 PURRIFY CLEANING RESULTS")
        print("="*60)
        
        if "files_removed" in clean_results:
            print(f"🗑️  Files Removed: {clean_results['files_removed']:,}")
            print(f"💾 Space Freed: {format_bytes(clean_results['space_freed'])}")
            print(f"⏱️  Duration: {clean_results.get('duration', 0):.2f}s")
        
        if "lilithos_cleaned" in clean_results:
            lilithos = clean_results["lilithos_cleaned"]
            print(f"\n🖤 LilithOS Cleaned: {len(lilithos['paths_cleaned'])} paths")
            print(f"💾 Space Freed: {format_bytes(lilithos['space_freed'])}")
            print(f"📁 Files Removed: {lilithos['files_removed']:,}")
        
        print("\n" + "="*60)
    
    def display_optimization_results(self, opt_results):
        """Display optimization results."""
        print("\n" + "="*60)
        print("⚡ PURRIFY OPTIMIZATION RESULTS")
        print("="*60)
        
        try:
            # Handle both dict and OptimizationResult objects
            if hasattr(opt_results, 'optimizations_applied'):
                # OptimizationResult object
                print(f"🔧 Optimizations Applied: {opt_results.optimizations_applied}")
                print(f"📈 Performance Improvement: {opt_results.performance_improvement:.1f}%")
                print(f"⏱️  Optimization Duration: {opt_results.optimization_duration:.2f}s")
                
                if opt_results.startup_items_optimized > 0:
                    print(f"🚀 Startup Items Optimized: {opt_results.startup_items_optimized}")
                
                if opt_results.memory_optimized:
                    print("🧠 Memory Optimization: Applied")
                
                if opt_results.disk_optimized:
                    print("💾 Disk Optimization: Applied")
                
                if opt_results.optimization_errors:
                    print(f"\n⚠️  Optimization Errors: {len(opt_results.optimization_errors)}")
                    for error in opt_results.optimization_errors[:5]:  # Show first 5 errors
                        print(f"   - {error}")
            elif isinstance(opt_results, dict) and "optimizations_applied" in opt_results:
                # Dictionary format
                print(f"🔧 Optimizations Applied: {opt_results['optimizations_applied']}")
                print(f"📈 Performance Improvement: {opt_results.get('performance_improvement', 0):.1f}%")
                print(f"⏱️  Optimization Duration: {opt_results.get('optimization_duration', 0):.2f}s")
                
                if opt_results.get('startup_items_optimized', 0) > 0:
                    print(f"🚀 Startup Items Optimized: {opt_results['startup_items_optimized']}")
                
                if opt_results.get('memory_optimized', False):
                    print("🧠 Memory Optimization: Applied")
                
                if opt_results.get('disk_optimized', False):
                    print("💾 Disk Optimization: Applied")
                
                if opt_results.get('optimization_errors'):
                    print(f"\n⚠️  Optimization Errors: {len(opt_results['optimization_errors'])}")
                    for error in opt_results['optimization_errors'][:5]:  # Show first 5 errors
                        print(f"   - {error}")
            else:
                print("❌ No optimization results available")
                
        except Exception as e:
            print(f"❌ Error displaying optimization results: {e}")
        
        print("="*60)
    
    def display_report(self, report_data: Dict[str, Any], output_file: Optional[str] = None):
        """Display system report."""
        print("\n" + "="*60)
        print("📊 PURRIFY SYSTEM REPORT")
        print("="*60)
        
        platform = report_data.get("platform", {})
        print(f"🖥️  Platform: {platform.get('platform_type', 'Unknown')}")
        print(f"🪟 Windows 11: {platform.get('is_windows_11', False)}")
        
        lilithos = report_data.get("lilithos_info", {})
        print(f"🖤 LilithOS Paths: {lilithos.get('total_paths', 0)}")
        
        print("\n" + "="*60)
    
    def display_system_status(self, status_info: Dict[str, Any]):
        """Display system status."""
        print("\n" + "="*60)
        print("📈 PURRIFY SYSTEM STATUS")
        print("="*60)
        
        print(f"💾 Disk Usage: {status_info.get('disk_usage', 'Unknown')}")
        print(f"🧠 Memory Usage: {status_info.get('memory_usage', 'Unknown')}")
        print(f"⚡ CPU Usage: {status_info.get('cpu_usage', 'Unknown')}")
        
        print("\n" + "="*60)
    
    def _save_results_to_file(self, results: Dict[str, Any], file_path: str):
        """Save results to a file."""
        try:
            import json
            with open(file_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"📄 Results saved to: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save results to {file_path}: {e}")
    
    async def generate_optimization_script(self, scan_results: Dict[str, Any]) -> str:
        """Generate a machine-specific optimization script after scan."""
        generator = ScriptGenerator(scan_results)
        script_path = generator.generate()
        logger.info(f"Machine-specific optimization script generated: {script_path}")
        return script_path
