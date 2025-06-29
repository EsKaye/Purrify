"""
Purrify System Scanner

This module provides comprehensive system scanning capabilities for
detecting cache files, temporary files, and optimization opportunities.
"""

import asyncio
import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from loguru import logger

from ..core.config import Config
from ..utils.platform import get_system_paths, get_browser_paths, format_bytes
from ..core.logger import log_async_function_call


@dataclass
class FileInfo:
    """Information about a file found during scanning."""
    path: str
    size: int
    modified: float
    file_type: str
    category: str
    safe_to_delete: bool = True
    risk_level: str = "low"


class SystemScanner:
    """
    System scanner for detecting optimization opportunities.
    
    This class provides comprehensive scanning capabilities to identify
    cache files, temporary files, logs, and other items that can be
    safely cleaned or optimized.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the system scanner.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.platform = config.platform
        self.system_paths = get_system_paths()
        self.browser_paths = get_browser_paths()
        
        # Track scanned files
        self.scanned_files: List[FileInfo] = []
        self.scan_errors: List[str] = []
        
        logger.info("SystemScanner initialized")
    
    @log_async_function_call
    async def scan_system(
        self,
        quick_mode: bool = False,
        detailed_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Perform comprehensive system scan.
        
        Args:
            quick_mode: Enable quick scan mode
            detailed_mode: Enable detailed scan with file analysis
            
        Returns:
            Dictionary containing scan results
        """
        logger.info(f"Starting system scan (quick: {quick_mode}, detailed: {detailed_mode})")
        
        # Reset tracking
        self.scanned_files.clear()
        self.scan_errors.clear()
        
        # Update config with scan mode
        self.config.scanning.quick_mode = quick_mode
        
        scan_start = time.time()
        
        try:
            # Scan different categories
            scan_tasks = []
            
            if self.config.scanning.include_system_caches:
                scan_tasks.append(self._scan_system_caches())
            
            if self.config.scanning.include_user_caches:
                scan_tasks.append(self._scan_user_caches())
            
            if self.config.scanning.include_application_caches:
                scan_tasks.append(self._scan_application_caches())
            
            if self.config.scanning.include_browser_caches:
                scan_tasks.append(self._scan_browser_caches())
            
            if self.config.scanning.include_logs:
                scan_tasks.append(self._scan_logs())
            
            if self.config.scanning.include_temp_files:
                scan_tasks.append(self._scan_temp_files())
            
            # Run scans concurrently
            await asyncio.gather(*scan_tasks, return_exceptions=True)
            
            # Calculate results
            scan_duration = time.time() - scan_start
            results = self._calculate_scan_results(scan_duration)
            
            logger.info(f"System scan completed in {scan_duration:.2f}s")
            logger.info(f"Found {len(self.scanned_files)} files")
            
            return results
            
        except Exception as e:
            logger.error(f"System scan failed: {e}")
            self.scan_errors.append(str(e))
            return self._create_error_result(str(e), time.time() - scan_start)
    
    async def _scan_system_caches(self):
        """Scan system cache directories."""
        logger.debug("Scanning system caches...")
        
        system_cache_paths = self.system_paths.get("system_caches", [])
        
        for path in system_cache_paths:
            try:
                await self._scan_directory(
                    path=path,
                    category="system_cache",
                    max_depth=3 if not self.config.scanning.quick_mode else 1
                )
            except Exception as e:
                error_msg = f"Failed to scan system cache {path}: {e}"
                logger.warning(error_msg)
                self.scan_errors.append(error_msg)
    
    async def _scan_user_caches(self):
        """Scan user cache directories."""
        logger.debug("Scanning user caches...")
        
        user_cache_paths = self.system_paths.get("user_caches", [])
        
        for path in user_cache_paths:
            try:
                await self._scan_directory(
                    path=path,
                    category="user_cache",
                    max_depth=5 if not self.config.scanning.quick_mode else 2
                )
            except Exception as e:
                error_msg = f"Failed to scan user cache {path}: {e}"
                logger.warning(error_msg)
                self.scan_errors.append(error_msg)
    
    async def _scan_application_caches(self):
        """Scan application cache directories."""
        logger.debug("Scanning application caches...")
        
        app_cache_paths = self.system_paths.get("application_caches", [])
        
        for path in app_cache_paths:
            try:
                await self._scan_directory(
                    path=path,
                    category="application_cache",
                    max_depth=4 if not self.config.scanning.quick_mode else 2
                )
            except Exception as e:
                error_msg = f"Failed to scan application cache {path}: {e}"
                logger.warning(error_msg)
                self.scan_errors.append(error_msg)
    
    async def _scan_browser_caches(self):
        """Scan browser cache directories."""
        logger.debug("Scanning browser caches...")
        
        for browser, paths in self.browser_paths.items():
            for path in paths:
                try:
                    await self._scan_directory(
                        path=path,
                        category=f"browser_cache_{browser}",
                        max_depth=3 if not self.config.scanning.quick_mode else 1
                    )
                except Exception as e:
                    error_msg = f"Failed to scan browser cache {browser} {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)
    
    async def _scan_logs(self):
        """Scan log directories."""
        logger.debug("Scanning log files...")
        
        log_paths = self.system_paths.get("system_logs", [])
        
        for path in log_paths:
            try:
                await self._scan_directory(
                    path=path,
                    category="log",
                    max_depth=3 if not self.config.scanning.quick_mode else 1,
                    file_patterns=["*.log", "*.log.*"]
                )
            except Exception as e:
                error_msg = f"Failed to scan logs {path}: {e}"
                logger.warning(error_msg)
                self.scan_errors.append(error_msg)
    
    async def _scan_temp_files(self):
        """Scan temporary file directories."""
        logger.debug("Scanning temporary files...")
        
        temp_paths = self.system_paths.get("temp_files", [])
        
        for path in temp_paths:
            try:
                await self._scan_directory(
                    path=path,
                    category="temp",
                    max_depth=2 if not self.config.scanning.quick_mode else 1
                )
            except Exception as e:
                error_msg = f"Failed to scan temp files {path}: {e}"
                logger.warning(error_msg)
                self.scan_errors.append(error_msg)
    
    async def _scan_directory(
        self,
        path: str,
        category: str,
        max_depth: int = 3,
        file_patterns: Optional[List[str]] = None
    ):
        """
        Scan a directory for files matching criteria.
        
        Args:
            path: Directory path to scan
            category: Category of files being scanned
            max_depth: Maximum directory depth to scan
            file_patterns: Optional file patterns to match
        """
        try:
            path_obj = Path(path)
            
            if not path_obj.exists():
                return
            
            # Check if path is excluded
            if self._is_path_excluded(str(path_obj)):
                return
            
            # Scan directory
            for file_path in path_obj.rglob("*"):
                try:
                    # Check depth
                    if len(file_path.parts) - len(path_obj.parts) > max_depth:
                        continue
                    
                    # Skip if not a file
                    if not file_path.is_file():
                        continue
                    
                    # Check file patterns if specified
                    if file_patterns and not any(
                        file_path.match(pattern) for pattern in file_patterns
                    ):
                        continue
                    
                    # Get file info
                    file_info = await self._get_file_info(file_path, category)
                    
                    if file_info:
                        self.scanned_files.append(file_info)
                        
                except (PermissionError, OSError) as e:
                    # Skip files we can't access
                    continue
                    
        except Exception as e:
            logger.debug(f"Error scanning directory {path}: {e}")
    
    async def _get_file_info(self, file_path: Path, category: str) -> Optional[FileInfo]:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            category: Category of the file
            
        Returns:
            FileInfo object if file should be included, None otherwise
        """
        try:
            # Get file stats
            stat_info = file_path.stat()
            
            # Check file age
            file_age_hours = (time.time() - stat_info.st_mtime) / 3600
            if file_age_hours < self.config.cleaning.min_file_age_hours:
                return None
            
            # Check file size
            file_size = stat_info.st_size
            if file_size == 0:
                return None
            
            # Determine file type
            file_type = self._get_file_type(file_path)
            
            # Check if safe to delete
            safe_to_delete = self._is_safe_to_delete(file_path, category)
            
            # Determine risk level
            risk_level = self._get_risk_level(file_path, category)
            
            return FileInfo(
                path=str(file_path),
                size=file_size,
                modified=stat_info.st_mtime,
                file_type=file_type,
                category=category,
                safe_to_delete=safe_to_delete,
                risk_level=risk_level
            )
            
        except (PermissionError, OSError):
            return None
    
    def _get_file_type(self, file_path: Path) -> str:
        """Get the type of a file based on its extension."""
        extension = file_path.suffix.lower()
        
        if extension in ['.log', '.log.1', '.log.2']:
            return "log"
        elif extension in ['.cache', '.tmp', '.temp']:
            return "cache"
        elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return "image"
        elif extension in ['.mp4', '.avi', '.mov', '.mkv']:
            return "video"
        elif extension in ['.mp3', '.wav', '.flac']:
            return "audio"
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "archive"
        else:
            return "other"
    
    def _is_safe_to_delete(self, file_path: Path, category: str) -> bool:
        """Check if a file is safe to delete."""
        file_path_str = str(file_path)
        
        # Check whitelist
        for whitelist_path in self.config.security.whitelist_paths:
            if whitelist_path in file_path_str:
                return False
        
        # Check blacklist
        for blacklist_path in self.config.security.blacklist_paths:
            if blacklist_path in file_path_str:
                return False
        
        # Check exclusion patterns
        for pattern in self.config.scanning.exclude_patterns:
            if file_path.match(pattern):
                return False
        
        # Category-specific checks
        if category == "system_cache":
            # Be more careful with system caches
            return file_path_str.count("/") > 2  # Only deep system caches
        
        return True
    
    def _get_risk_level(self, file_path: Path, category: str) -> str:
        """Determine the risk level of deleting a file."""
        file_path_str = str(file_path)
        
        # High risk patterns
        high_risk_patterns = [
            "system", "library", "bin", "sbin", "usr/bin", "usr/sbin",
            "windows", "system32", "syswow64", "program files"
        ]
        
        for pattern in high_risk_patterns:
            if pattern in file_path_str.lower():
                return "high"
        
        # Medium risk patterns
        medium_risk_patterns = [
            "application support", "preferences", "settings",
            "appdata", "local", "roaming"
        ]
        
        for pattern in medium_risk_patterns:
            if pattern in file_path_str.lower():
                return "medium"
        
        return "low"
    
    def _is_path_excluded(self, path: str) -> bool:
        """Check if a path should be excluded from scanning."""
        for pattern in self.config.scanning.exclude_patterns:
            if pattern in path:
                return True
        return False
    
    def _calculate_scan_results(self, scan_duration: float) -> Dict[str, Any]:
        """Calculate scan results from collected file information."""
        if not self.scanned_files:
            return {
                "total_files_scanned": 0,
                "cache_files_found": 0,
                "temp_files_found": 0,
                "log_files_found": 0,
                "large_files_found": 0,
                "potential_space_savings": 0,
                "scan_duration": scan_duration,
                "scan_errors": self.scan_errors,
                "file_details": []
            }
        
        # Categorize files
        cache_files = [f for f in self.scanned_files if "cache" in f.category]
        temp_files = [f for f in self.scanned_files if f.category == "temp"]
        log_files = [f for f in self.scanned_files if f.category == "log"]
        large_files = [f for f in self.scanned_files if f.size > 100 * 1024 * 1024]  # > 100MB
        
        # Calculate space savings
        potential_space_savings = sum(f.size for f in self.scanned_files if f.safe_to_delete)
        
        # Prepare file details (limit to first 1000 for performance)
        file_details = []
        for file_info in self.scanned_files[:1000]:
            file_details.append({
                "path": file_info.path,
                "size": file_info.size,
                "modified": file_info.modified,
                "category": file_info.category,
                "file_type": file_info.file_type,
                "safe_to_delete": file_info.safe_to_delete,
                "risk_level": file_info.risk_level
            })
        
        return {
            "total_files_scanned": len(self.scanned_files),
            "cache_files_found": len(cache_files),
            "temp_files_found": len(temp_files),
            "log_files_found": len(log_files),
            "large_files_found": len(large_files),
            "potential_space_savings": potential_space_savings,
            "scan_duration": scan_duration,
            "scan_errors": self.scan_errors,
            "file_details": file_details
        }
    
    def _create_error_result(self, error: str, scan_duration: float) -> Dict[str, Any]:
        """Create error result when scan fails."""
        return {
            "total_files_scanned": 0,
            "cache_files_found": 0,
            "temp_files_found": 0,
            "log_files_found": 0,
            "large_files_found": 0,
            "potential_space_savings": 0,
            "scan_duration": scan_duration,
            "scan_errors": [error],
            "file_details": []
        }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status information.
        
        Returns:
            Dictionary containing system status
        """
        logger.debug("Getting system status...")
        
        try:
            import psutil
            
            # Get system information
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get process information
            processes = len(psutil.pids())
            
            # Get network information
            network = psutil.net_io_counters()
            
            status = {
                "cpu_usage_percent": cpu_percent,
                "memory_total_bytes": memory.total,
                "memory_used_bytes": memory.used,
                "memory_available_bytes": memory.available,
                "memory_percent_used": memory.percent,
                "disk_total_bytes": disk.total,
                "disk_used_bytes": disk.used,
                "disk_free_bytes": disk.free,
                "disk_percent_used": disk.percent,
                "process_count": processes,
                "network_bytes_sent": network.bytes_sent,
                "network_bytes_recv": network.bytes_recv,
                "timestamp": time.time()
            }
            
            return status
            
        except ImportError:
            logger.warning("psutil not available, returning basic status")
            return {
                "error": "psutil not available",
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {
                "error": str(e),
                "timestamp": time.time()
            } 