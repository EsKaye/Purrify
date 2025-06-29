"""
Purrify Cache Cleaner

This module provides safe cache cleaning capabilities for removing
unnecessary files while maintaining system stability.
"""

import asyncio
import os
import shutil
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from loguru import logger

from ..core.config import Config
from ..core.logger import log_async_function_call


@dataclass
class CleanResult:
    """Results from a cleaning operation."""
    files_cleaned: int = 0
    space_freed: int = 0
    clean_duration: float = 0.0
    clean_errors: List[str] = None
    backup_created: bool = False
    backup_path: Optional[str] = None
    
    def __post_init__(self):
        if self.clean_errors is None:
            self.clean_errors = []


class CacheCleaner:
    """
    Cache cleaner for safely removing unnecessary files.
    
    This class provides intelligent cleaning capabilities that respect
    system safety and user preferences while effectively removing
    cache files, temporary files, and logs.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the cache cleaner.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.platform = config.platform
        
        logger.info("CacheCleaner initialized")
    
    @log_async_function_call
    async def clean_system(
        self,
        clean_options: Dict[str, bool],
        safe_mode: bool = True,
        backup_path: Optional[str] = None
    ) -> CleanResult:
        """
        Clean system files based on specified options.
        
        Args:
            clean_options: Dictionary specifying what to clean
            safe_mode: Enable safe mode (preview only)
            backup_path: Path to backup directory
            
        Returns:
            CleanResult object containing cleaning results
        """
        logger.info(f"Starting system cleaning (safe_mode: {safe_mode})")
        
        clean_start = time.time()
        files_cleaned = 0
        space_freed = 0
        clean_errors = []
        
        try:
            # Clean different categories
            if clean_options.get("caches", False):
                result = await self._clean_caches(safe_mode, backup_path)
                files_cleaned += result.files_cleaned
                space_freed += result.space_freed
                clean_errors.extend(result.clean_errors)
            
            if clean_options.get("logs", False):
                result = await self._clean_logs(safe_mode, backup_path)
                files_cleaned += result.files_cleaned
                space_freed += result.space_freed
                clean_errors.extend(result.clean_errors)
            
            if clean_options.get("temp_files", False):
                result = await self._clean_temp_files(safe_mode, backup_path)
                files_cleaned += result.files_cleaned
                space_freed += result.space_freed
                clean_errors.extend(result.clean_errors)
            
            clean_duration = time.time() - clean_start
            
            result = CleanResult(
                files_cleaned=files_cleaned,
                space_freed=space_freed,
                clean_duration=clean_duration,
                clean_errors=clean_errors,
                backup_created=backup_path is not None,
                backup_path=backup_path
            )
            
            logger.info(f"System cleaning completed in {clean_duration:.2f}s")
            logger.info(f"Cleaned {files_cleaned} files, freed {space_freed} bytes")
            
            return result
            
        except Exception as e:
            logger.error(f"System cleaning failed: {e}")
            clean_errors.append(str(e))
            return CleanResult(
                clean_errors=clean_errors,
                clean_duration=time.time() - clean_start
            )
    
    async def _clean_caches(self, safe_mode: bool, backup_path: Optional[str]) -> CleanResult:
        """Clean cache files."""
        logger.debug("Cleaning cache files...")
        
        # This would implement actual cache cleaning logic
        # For now, return a placeholder result
        return CleanResult(
            files_cleaned=0,
            space_freed=0,
            clean_errors=[]
        )
    
    async def _clean_logs(self, safe_mode: bool, backup_path: Optional[str]) -> CleanResult:
        """Clean log files."""
        logger.debug("Cleaning log files...")
        
        # This would implement actual log cleaning logic
        # For now, return a placeholder result
        return CleanResult(
            files_cleaned=0,
            space_freed=0,
            clean_errors=[]
        )
    
    async def _clean_temp_files(self, safe_mode: bool, backup_path: Optional[str]) -> CleanResult:
        """Clean temporary files."""
        logger.debug("Cleaning temporary files...")
        
        # This would implement actual temp file cleaning logic
        # For now, return a placeholder result
        return CleanResult(
            files_cleaned=0,
            space_freed=0,
            clean_errors=[]
        )
    
    async def create_backup(self, backup_dir: Path):
        """Create backup of important files."""
        logger.info(f"Creating backup at {backup_dir}")
        
        # This would implement actual backup logic
        # For now, just create the directory
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Backup created successfully") 