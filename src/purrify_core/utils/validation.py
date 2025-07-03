"""
Validation Utilities

This module provides input validation utilities for the Purrify system.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Union


class ValidationUtils:
    """Input validation utility functions."""
    
    @staticmethod
    def is_valid_path(path: str) -> bool:
        """Check if a path is valid."""
        try:
            Path(path)
            return True
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def is_valid_file_path(path: str) -> bool:
        """Check if a file path is valid and exists."""
        try:
            path_obj = Path(path)
            return path_obj.exists() and path_obj.is_file()
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def is_valid_directory_path(path: str) -> bool:
        """Check if a directory path is valid and exists."""
        try:
            path_obj = Path(path)
            return path_obj.exists() and path_obj.is_dir()
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def is_safe_path(path: str, allowed_dirs: List[str] = None) -> bool:
        """Check if a path is safe to operate on."""
        if allowed_dirs is None:
            allowed_dirs = []
        
        try:
            path_obj = Path(path).resolve()
            
            # Check if path is within allowed directories
            if allowed_dirs:
                for allowed_dir in allowed_dirs:
                    allowed_path = Path(allowed_dir).resolve()
                    try:
                        path_obj.relative_to(allowed_path)
                        return True
                    except ValueError:
                        continue
                return False
            
            return True
        except (OSError, ValueError):
            return False
    
    @staticmethod
    def is_valid_file_size(size_bytes: Union[int, str]) -> bool:
        """Check if file size is valid."""
        try:
            size = int(size_bytes)
            return 0 <= size <= (1024 ** 4)  # Max 1TB
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_percentage(value: Union[float, str]) -> bool:
        """Check if percentage value is valid."""
        try:
            percentage = float(value)
            return 0.0 <= percentage <= 100.0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_duration(seconds: Union[float, str]) -> bool:
        """Check if duration is valid."""
        try:
            duration = float(seconds)
            return 0.0 <= duration <= (24 * 3600)  # Max 24 hours
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_hash(hash_string: str, algorithm: str = "md5") -> bool:
        """Check if hash string is valid for the given algorithm."""
        if not isinstance(hash_string, str):
            return False
        
        # Check hash length
        expected_lengths = {
            "md5": 32,
            "sha1": 40,
            "sha256": 64,
            "sha512": 128,
            "blake2b": 128,
            "blake2s": 64
        }
        
        expected_length = expected_lengths.get(algorithm, 32)
        if len(hash_string) != expected_length:
            return False
        
        # Check if it's a valid hexadecimal string
        return bool(re.match(r'^[0-9a-fA-F]+$', hash_string))
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if email address is valid."""
        if not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid."""
        if not isinstance(url, str):
            return False
        
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """Check if filename is valid."""
        if not isinstance(filename, str):
            return False
        
        # Check for invalid characters
        invalid_chars = '<>:"/\\|?*'
        return not any(char in filename for char in invalid_chars)
    
    @staticmethod
    def is_valid_config_key(key: str) -> bool:
        """Check if configuration key is valid."""
        if not isinstance(key, str):
            return False
        
        # Check for valid characters (alphanumeric, underscore, dot)
        pattern = r'^[a-zA-Z0-9_.]+$'
        return bool(re.match(pattern, key))
    
    @staticmethod
    def validate_scan_options(options: Dict[str, Any]) -> Dict[str, Any]:
        """Validate scan options and return cleaned options."""
        validated = {}
        
        # Validate quick_mode
        if 'quick_mode' in options:
            validated['quick_mode'] = bool(options['quick_mode'])
        
        # Validate max_depth
        if 'max_depth' in options:
            try:
                max_depth = int(options['max_depth'])
                validated['max_depth'] = max(1, min(max_depth, 20))
            except (ValueError, TypeError):
                validated['max_depth'] = 10
        
        # Validate timeout
        if 'timeout' in options:
            try:
                timeout = float(options['timeout'])
                validated['timeout'] = max(30, min(timeout, 3600))
            except (ValueError, TypeError):
                validated['timeout'] = 300
        
        # Validate include_patterns
        if 'include_patterns' in options:
            if isinstance(options['include_patterns'], list):
                validated['include_patterns'] = [
                    str(pattern) for pattern in options['include_patterns']
                    if isinstance(pattern, str)
                ]
        
        # Validate exclude_patterns
        if 'exclude_patterns' in options:
            if isinstance(options['exclude_patterns'], list):
                validated['exclude_patterns'] = [
                    str(pattern) for pattern in options['exclude_patterns']
                    if isinstance(pattern, str)
                ]
        
        return validated
    
    @staticmethod
    def validate_clean_options(options: Dict[str, Any]) -> Dict[str, Any]:
        """Validate clean options and return cleaned options."""
        validated = {}
        
        # Validate safe_mode
        if 'safe_mode' in options:
            validated['safe_mode'] = bool(options['safe_mode'])
        
        # Validate backup
        if 'backup' in options:
            validated['backup'] = bool(options['backup'])
        
        # Validate backup_path
        if 'backup_path' in options and options['backup_path']:
            if ValidationUtils.is_valid_path(options['backup_path']):
                validated['backup_path'] = str(options['backup_path'])
        
        # Validate min_age_hours
        if 'min_age_hours' in options:
            try:
                min_age = int(options['min_age_hours'])
                validated['min_age_hours'] = max(0, min(min_age, 8760))  # Max 1 year
            except (ValueError, TypeError):
                validated['min_age_hours'] = 24
        
        return validated
    
    @staticmethod
    def validate_optimization_options(options: Dict[str, Any]) -> Dict[str, Any]:
        """Validate optimization options and return cleaned options."""
        validated = {}
        
        # Validate optimization types
        optimization_types = ['startup', 'memory', 'disk', 'registry', 'services']
        for opt_type in optimization_types:
            if opt_type in options:
                validated[opt_type] = bool(options[opt_type])
        
        # Validate safe_mode
        if 'safe_mode' in options:
            validated['safe_mode'] = bool(options['safe_mode'])
        
        return validated
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing invalid characters."""
        if not isinstance(filename, str):
            return ""
        
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        sanitized = filename
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        
        return sanitized or "unnamed"
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """Validate that required fields are present and return missing fields."""
        missing_fields = []
        
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        
        return missing_fields 