"""
Purrify System Scanner

This module provides comprehensive system scanning capabilities for
detecting cache files, temporary files, duplicates, photos, and optimization opportunities.
"""

import asyncio
import os
import time
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict
from loguru import logger
import json

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
    hash: Optional[str] = None
    duplicate_group: Optional[str] = None
    photo_metadata: Optional[Dict] = None
    compression_potential: Optional[float] = None


@dataclass
class DuplicateGroup:
    """Group of duplicate files."""
    hash: str
    files: List[FileInfo]
    total_size: int
    potential_savings: int
    file_type: str


@dataclass
class PhotoAnalysis:
    """Photo analysis results."""
    path: str
    size: int
    resolution: Optional[Tuple[int, int]]
    format: str
    compression_ratio: Optional[float]
    quality_score: Optional[float]
    duplicate_of: Optional[str] = None


class SystemScanner:
    """
    Enhanced system scanner for detecting optimization opportunities.
    
    This class provides comprehensive scanning capabilities to identify
    cache files, temporary files, logs, duplicates, photos, and other items
    that can be safely cleaned or optimized.
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
        
        # Enhanced tracking
        self.duplicate_groups: List[DuplicateGroup] = []
        self.photo_analysis: List[PhotoAnalysis] = []
        self.large_files: List[FileInfo] = []
        self.old_files: List[FileInfo] = []
        
        # File type patterns
        self.photo_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif'}
        self.video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v'}
        self.document_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf'}
        
        logger.info("Enhanced SystemScanner initialized")
    
    @log_async_function_call
    async def scan_system(
        self,
        quick_mode: bool = False,
        detailed_mode: bool = False,
        include_duplicates: bool = True,
        include_photos: bool = True,
        include_large_files: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive system scan with enhanced capabilities.
        
        Args:
            quick_mode: Enable quick scan mode
            detailed_mode: Enable detailed scan with file analysis
            include_duplicates: Scan for duplicate files
            include_photos: Analyze photos for optimization
            include_large_files: Identify large files
            
        Returns:
            Dictionary containing scan results
        """
        logger.info(f"Starting enhanced system scan (quick: {quick_mode}, detailed: {detailed_mode})")
        
        # Reset tracking
        self.scanned_files.clear()
        self.scan_errors.clear()
        self.duplicate_groups.clear()
        self.photo_analysis.clear()
        self.large_files.clear()
        self.old_files.clear()
        
        # Update config with scan mode
        self.config.scanning.quick_mode = quick_mode
        
        scan_start = time.time()
        
        try:
            # Basic scans
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
            
            # Enhanced scans
            if include_duplicates and not quick_mode:
                scan_tasks.append(self._scan_for_duplicates())
            
            if include_photos and not quick_mode:
                scan_tasks.append(self._scan_photos())
            
            if include_large_files:
                scan_tasks.append(self._scan_large_files())
            
            if not quick_mode:
                scan_tasks.append(self._scan_old_files())
            
            # Run scans concurrently
            await asyncio.gather(*scan_tasks, return_exceptions=True)
            
            # Post-process results
            if include_duplicates and not quick_mode:
                await self._analyze_duplicates()
            
            if include_photos and not quick_mode:
                await self._analyze_photos()
            
            # Calculate results
            scan_duration = time.time() - scan_start
            results = self._calculate_enhanced_scan_results(scan_duration)
            
            logger.info(f"Enhanced system scan completed in {scan_duration:.2f}s")
            logger.info(f"Found {len(self.scanned_files)} files")
            logger.info(f"Found {len(self.duplicate_groups)} duplicate groups")
            logger.info(f"Analyzed {len(self.photo_analysis)} photos")
            
            return results
            
        except Exception as e:
            logger.error(f"Enhanced system scan failed: {e}")
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
        
        # Windows 11 specific cache scanning
        if self.platform.get("is_windows_11", False):
            await self._scan_windows_11_caches()
    
    async def _scan_windows_11_caches(self):
        """Scan Windows 11 specific cache directories."""
        logger.debug("Scanning Windows 11 specific caches...")
        
        # WSL caches
        wsl_paths = self.system_paths.get("wsl_caches", [])
        for path in wsl_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory(
                        path=path,
                        category="wsl_cache",
                        max_depth=4 if not self.config.scanning.quick_mode else 2
                    )
                except Exception as e:
                    error_msg = f"Failed to scan WSL cache {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)
        
        # Microsoft Store caches
        store_paths = self.system_paths.get("microsoft_store_caches", [])
        for path in store_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory(
                        path=path,
                        category="microsoft_store_cache",
                        max_depth=3 if not self.config.scanning.quick_mode else 1
                    )
                except Exception as e:
                    error_msg = f"Failed to scan Microsoft Store cache {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)
        
        # Windows Security caches
        security_paths = self.system_paths.get("windows_security_caches", [])
        for path in security_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory(
                        path=path,
                        category="windows_security_cache",
                        max_depth=3 if not self.config.scanning.quick_mode else 1
                    )
                except Exception as e:
                    error_msg = f"Failed to scan Windows Security cache {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)
        
        # Windows Search caches
        search_paths = self.system_paths.get("windows_search_caches", [])
        for path in search_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory(
                        path=path,
                        category="windows_search_cache",
                        max_depth=3 if not self.config.scanning.quick_mode else 1
                    )
                except Exception as e:
                    error_msg = f"Failed to scan Windows Search cache {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)
        
        # Cloud integration caches
        cloud_paths = self.system_paths.get("cloud_integration_caches", [])
        for path in cloud_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory(
                        path=path,
                        category="cloud_integration_cache",
                        max_depth=4 if not self.config.scanning.quick_mode else 2
                    )
                except Exception as e:
                    error_msg = f"Failed to scan cloud integration cache {path}: {e}"
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
        
        log_paths = self.system_paths.get("logs", [])
        
        for path in log_paths:
            try:
                await self._scan_directory(
                    path=path,
                    category="log",
                    max_depth=4 if not self.config.scanning.quick_mode else 2,
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
                    max_depth=3 if not self.config.scanning.quick_mode else 1
                )
            except Exception as e:
                error_msg = f"Failed to scan temp files {path}: {e}"
                logger.warning(error_msg)
                self.scan_errors.append(error_msg)
    
    async def _scan_for_duplicates(self):
        """Scan for duplicate files across the system."""
        logger.debug("Scanning for duplicate files...")
        
        # Common directories to scan for duplicates
        duplicate_paths = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Music"),
            os.path.expanduser("~/Videos")
        ]
        
        for path in duplicate_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory_for_duplicates(path, max_depth=5)
                except Exception as e:
                    error_msg = f"Failed to scan for duplicates in {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)

    async def _scan_directory_for_duplicates(self, path: str, max_depth: int = 3):
        """Scan directory for potential duplicate files."""
        try:
            for root, dirs, files in os.walk(path):
                depth = root[len(path):].count(os.sep)
                if depth > max_depth:
                    continue
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_info = await self._get_enhanced_file_info(file_path, "potential_duplicate")
                        if file_info and file_info.size > 1024:  # Only files > 1KB
                            self.scanned_files.append(file_info)
                    except Exception as e:
                        logger.debug(f"Error processing file {file_path}: {e}")
                        
        except Exception as e:
            logger.warning(f"Error scanning directory {path}: {e}")

    async def _scan_photos(self):
        """Scan for photos and analyze them."""
        logger.debug("Scanning for photos...")
        
        photo_paths = [
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents")
        ]
        
        for path in photo_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory_for_photos(path, max_depth=6)
                except Exception as e:
                    error_msg = f"Failed to scan for photos in {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)

    async def _scan_directory_for_photos(self, path: str, max_depth: int = 4):
        """Scan directory for photos."""
        try:
            for root, dirs, files in os.walk(path):
                depth = root[len(path):].count(os.sep)
                if depth > max_depth:
                    continue
                
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = Path(file).suffix.lower()
                    
                    if file_ext in self.photo_extensions:
                        try:
                            file_info = await self._get_enhanced_file_info(file_path, "photo")
                            if file_info:
                                self.scanned_files.append(file_info)
                        except Exception as e:
                            logger.debug(f"Error processing photo {file_path}: {e}")
                            
        except Exception as e:
            logger.warning(f"Error scanning photos in {path}: {e}")

    async def _scan_large_files(self):
        """Scan for large files that could be optimized."""
        logger.debug("Scanning for large files...")
        
        large_file_paths = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Videos"),
            os.path.expanduser("~/Music")
        ]
        
        for path in large_file_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory_for_large_files(path, max_depth=4)
                except Exception as e:
                    error_msg = f"Failed to scan for large files in {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)

    async def _scan_directory_for_large_files(self, path: str, max_depth: int = 3):
        """Scan directory for large files."""
        try:
            for root, dirs, files in os.walk(path):
                depth = root[len(path):].count(os.sep)
                if depth > max_depth:
                    continue
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        if stat.st_size > 10 * 1024 * 1024:  # Files > 10MB
                            file_info = await self._get_enhanced_file_info(file_path, "large_file")
                            if file_info:
                                self.large_files.append(file_info)
                                self.scanned_files.append(file_info)
                    except Exception as e:
                        logger.debug(f"Error processing large file {file_path}: {e}")
                        
        except Exception as e:
            logger.warning(f"Error scanning large files in {path}: {e}")

    async def _scan_old_files(self):
        """Scan for old files that might be candidates for cleanup."""
        logger.debug("Scanning for old files...")
        
        old_file_paths = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents")
        ]
        
        import time
        current_time = time.time()
        cutoff_time = current_time - (90 * 24 * 3600)  # 90 days ago
        
        for path in old_file_paths:
            if os.path.exists(path):
                try:
                    await self._scan_directory_for_old_files(path, cutoff_time, max_depth=3)
                except Exception as e:
                    error_msg = f"Failed to scan for old files in {path}: {e}"
                    logger.warning(error_msg)
                    self.scan_errors.append(error_msg)

    async def _scan_directory_for_old_files(self, path: str, cutoff_time: float, max_depth: int = 3):
        """Scan directory for old files."""
        try:
            for root, dirs, files in os.walk(path):
                depth = root[len(path):].count(os.sep)
                if depth > max_depth:
                    continue
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        if stat.st_mtime < cutoff_time:
                            file_info = await self._get_enhanced_file_info(file_path, "old_file")
                            if file_info:
                                self.old_files.append(file_info)
                                self.scanned_files.append(file_info)
                    except Exception as e:
                        logger.debug(f"Error processing old file {file_path}: {e}")
                        
        except Exception as e:
            logger.warning(f"Error scanning old files in {path}: {e}")

    async def _analyze_duplicates(self):
        """Analyze scanned files for duplicates."""
        logger.debug("Analyzing duplicates...")
        
        # Group files by size first (quick filter)
        size_groups = defaultdict(list)
        for file_info in self.scanned_files:
            if file_info.size > 1024:  # Only files > 1KB
                size_groups[file_info.size].append(file_info)
        
        # For files with same size, calculate hash
        for size, files in size_groups.items():
            if len(files) > 1:
                await self._calculate_file_hashes(files)
        
        # Group by hash
        hash_groups = defaultdict(list)
        for file_info in self.scanned_files:
            if file_info.hash:
                hash_groups[file_info.hash].append(file_info)
        
        # Create duplicate groups
        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                total_size = sum(f.size for f in files)
                potential_savings = total_size - min(f.size for f in files)  # Keep one copy
                
                duplicate_group = DuplicateGroup(
                    hash=file_hash,
                    files=files,
                    total_size=total_size,
                    potential_savings=potential_savings,
                    file_type=files[0].file_type
                )
                
                self.duplicate_groups.append(duplicate_group)
                
                # Mark files as duplicates
                for i, file_info in enumerate(files):
                    file_info.duplicate_group = file_hash
                    if i > 0:  # Mark all but the first as safe to delete
                        file_info.safe_to_delete = True
                        file_info.risk_level = "low"

    async def _calculate_file_hashes(self, files: List[FileInfo]):
        """Calculate MD5 hashes for files."""
        for file_info in files:
            try:
                file_info.hash = await self._calculate_file_hash(file_info.path)
            except Exception as e:
                logger.debug(f"Error calculating hash for {file_info.path}: {e}")

    async def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.debug(f"Error calculating hash for {file_path}: {e}")
            return ""

    async def _analyze_photos(self):
        """Analyze photos for optimization opportunities."""
        logger.debug("Analyzing photos...")
        
        for file_info in self.scanned_files:
            if file_info.category == "photo":
                try:
                    photo_analysis = await self._analyze_single_photo(file_info)
                    if photo_analysis:
                        self.photo_analysis.append(photo_analysis)
                except Exception as e:
                    logger.debug(f"Error analyzing photo {file_info.path}: {e}")

    async def _analyze_single_photo(self, file_info: FileInfo) -> Optional[PhotoAnalysis]:
        """Analyze a single photo for optimization opportunities."""
        try:
            file_path = Path(file_info.path)
            file_ext = file_path.suffix.lower()
            
            # Basic analysis without external dependencies
            resolution = None
            compression_ratio = None
            quality_score = None
            
            # Try to get basic image info
            try:
                # Simple file analysis
                if file_ext in {'.jpg', '.jpeg'}:
                    compression_ratio = 0.8  # Estimated compression potential
                    quality_score = 0.7
                elif file_ext in {'.png'}:
                    compression_ratio = 0.6
                    quality_score = 0.9
                elif file_ext in {'.gif'}:
                    compression_ratio = 0.5
                    quality_score = 0.6
                else:
                    compression_ratio = 0.7
                    quality_score = 0.8
                    
            except Exception as e:
                logger.debug(f"Error analyzing photo metadata for {file_info.path}: {e}")
            
            return PhotoAnalysis(
                path=file_info.path,
                size=file_info.size,
                resolution=resolution,
                format=file_ext,
                compression_ratio=compression_ratio,
                quality_score=quality_score
            )
            
        except Exception as e:
            logger.debug(f"Error in photo analysis for {file_info.path}: {e}")
            return None

    async def _get_enhanced_file_info(self, file_path: str, category: str) -> Optional[FileInfo]:
        """Get enhanced file information including hash and metadata."""
        try:
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists() or not file_path_obj.is_file():
                return None
            
            stat = file_path_obj.stat()
            
            file_info = FileInfo(
                path=str(file_path_obj),
                size=stat.st_size,
                modified=stat.st_mtime,
                file_type=self._get_file_type(file_path_obj),
                category=category,
                safe_to_delete=self._is_safe_to_delete(file_path_obj, category),
                risk_level=self._get_risk_level(file_path_obj, category)
            )
            
            return file_info
            
        except Exception as e:
            logger.debug(f"Error getting file info for {file_path}: {e}")
            return None

    def _calculate_enhanced_scan_results(self, scan_duration: float) -> Dict[str, Any]:
        """Calculate enhanced scan results with duplicate and photo analysis."""
        total_files = len(self.scanned_files)
        total_size = sum(f.size for f in self.scanned_files)
        
        # Categorize files
        categories = defaultdict(list)
        for file_info in self.scanned_files:
            categories[file_info.category].append(file_info)
        
        # Calculate potential savings
        cache_savings = sum(f.size for f in self.scanned_files if "cache" in f.category)
        duplicate_savings = sum(group.potential_savings for group in self.duplicate_groups)
        photo_savings = sum(
            int(photo.size * (1 - (photo.compression_ratio or 0.7)))
            for photo in self.photo_analysis
        )
        
        total_potential_savings = cache_savings + duplicate_savings + photo_savings
        
        return {
            "success": True,
            "scan_duration": scan_duration,
            "total_files": total_files,
            "total_size": total_size,
            "potential_savings": total_potential_savings,
            "categories": {
                category: {
                    "count": len(files),
                    "size": sum(f.size for f in files),
                    "files": [f.path for f in files[:10]]  # First 10 files
                }
                for category, files in categories.items()
            },
            "duplicates": {
                "groups": len(self.duplicate_groups),
                "total_size": sum(group.total_size for group in self.duplicate_groups),
                "potential_savings": duplicate_savings,
                "groups_detail": [
                    {
                        "hash": group.hash,
                        "file_type": group.file_type,
                        "count": len(group.files),
                        "total_size": group.total_size,
                        "potential_savings": group.potential_savings,
                        "files": [f.path for f in group.files]
                    }
                    for group in self.duplicate_groups[:10]  # First 10 groups
                ]
            },
            "photos": {
                "count": len(self.photo_analysis),
                "total_size": sum(photo.size for photo in self.photo_analysis),
                "potential_savings": photo_savings,
                "photos_detail": [
                    {
                        "path": photo.path,
                        "size": photo.size,
                        "format": photo.format,
                        "compression_ratio": photo.compression_ratio,
                        "quality_score": photo.quality_score
                    }
                    for photo in self.photo_analysis[:10]  # First 10 photos
                ]
            },
            "large_files": {
                "count": len(self.large_files),
                "total_size": sum(f.size for f in self.large_files),
                "files": [
                    {
                        "path": f.path,
                        "size": f.size,
                        "file_type": f.file_type
                    }
                    for f in self.large_files[:10]  # First 10 large files
                ]
            },
            "old_files": {
                "count": len(self.old_files),
                "total_size": sum(f.size for f in self.old_files),
                "files": [
                    {
                        "path": f.path,
                        "size": f.size,
                        "modified": f.modified
                    }
                    for f in self.old_files[:10]  # First 10 old files
                ]
            },
            "errors": self.scan_errors
        }

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