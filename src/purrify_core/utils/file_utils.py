"""
File Utilities

This module provides cross-platform file operations for the Purrify system.
"""

import os
import shutil
import stat
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta


class FileUtils:
    """Cross-platform file utility functions."""
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get comprehensive file information."""
        try:
            path = Path(file_path)
            if not path.exists():
                return {}
            
            stat_info = path.stat()
            
            return {
                "path": str(path),
                "name": path.name,
                "size": stat_info.st_size,
                "modified": stat_info.st_mtime,
                "created": stat_info.st_ctime,
                "accessed": stat_info.st_atime,
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "is_symlink": path.is_symlink(),
                "extension": path.suffix.lower(),
                "parent": str(path.parent),
                "exists": True
            }
        except (OSError, PermissionError):
            return {"path": file_path, "exists": False}
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except (OSError, PermissionError):
            return 0
    
    @staticmethod
    def get_file_modified_time(file_path: str) -> float:
        """Get file modification time."""
        try:
            return Path(file_path).stat().st_mtime
        except (OSError, PermissionError):
            return 0.0
    
    @staticmethod
    def is_file_old(file_path: str, days: int = 30) -> bool:
        """Check if file is older than specified days."""
        try:
            modified_time = FileUtils.get_file_modified_time(file_path)
            cutoff_time = datetime.now() - timedelta(days=days)
            return datetime.fromtimestamp(modified_time) < cutoff_time
        except (OSError, PermissionError):
            return False
    
    @staticmethod
    def is_file_large(file_path: str, size_mb: int = 100) -> bool:
        """Check if file is larger than specified size in MB."""
        try:
            size_bytes = FileUtils.get_file_size(file_path)
            return size_bytes > (size_mb * 1024 * 1024)
        except (OSError, PermissionError):
            return False
    
    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Get file type based on extension."""
        extension = Path(file_path).suffix.lower()
        
        # Image files
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif']:
            return "image"
        
        # Video files
        elif extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v']:
            return "video"
        
        # Audio files
        elif extension in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
            return "audio"
        
        # Document files
        elif extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf']:
            return "document"
        
        # Archive files
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']:
            return "archive"
        
        # Log files
        elif extension in ['.log', '.log.1', '.log.2']:
            return "log"
        
        # Cache files
        elif extension in ['.cache', '.tmp', '.temp']:
            return "cache"
        
        else:
            return "other"
    
    @staticmethod
    def safe_delete_file(file_path: str, backup_dir: Optional[str] = None) -> bool:
        """Safely delete a file with optional backup."""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            # Create backup if requested
            if backup_dir:
                backup_path = Path(backup_dir) / path.name
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, backup_path)
            
            # Delete the file
            path.unlink()
            return True
            
        except (OSError, PermissionError):
            return False
    
    @staticmethod
    def safe_delete_directory(dir_path: str, backup_dir: Optional[str] = None) -> bool:
        """Safely delete a directory with optional backup."""
        try:
            path = Path(dir_path)
            if not path.exists():
                return False
            
            # Create backup if requested
            if backup_dir:
                backup_path = Path(backup_dir) / path.name
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(path, backup_path)
            
            # Delete the directory
            shutil.rmtree(path)
            return True
            
        except (OSError, PermissionError):
            return False
    
    @staticmethod
    def get_directory_size(dir_path: str) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        try:
            for path in Path(dir_path).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except (OSError, PermissionError):
            pass
        return total_size
    
    @staticmethod
    def get_directory_file_count(dir_path: str) -> int:
        """Get total number of files in directory."""
        file_count = 0
        try:
            for path in Path(dir_path).rglob('*'):
                if path.is_file():
                    file_count += 1
        except (OSError, PermissionError):
            pass
        return file_count
    
    @staticmethod
    def is_safe_to_delete(file_path: str, whitelist: List[str] = None, blacklist: List[str] = None) -> bool:
        """Check if file is safe to delete based on whitelist/blacklist."""
        if whitelist is None:
            whitelist = []
        if blacklist is None:
            blacklist = []
        
        file_path_str = str(file_path).lower()
        
        # Check blacklist first
        for blacklisted in blacklist:
            if blacklisted.lower() in file_path_str:
                return False
        
        # Check whitelist
        for whitelisted in whitelist:
            if whitelisted.lower() in file_path_str:
                return True
        
        # If no whitelist specified, allow deletion
        return len(whitelist) == 0
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def get_relative_path(file_path: str, base_path: str) -> str:
        """Get relative path from base path."""
        try:
            return str(Path(file_path).relative_to(Path(base_path)))
        except ValueError:
            return file_path 