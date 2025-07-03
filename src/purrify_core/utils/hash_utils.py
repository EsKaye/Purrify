"""
Hash Utilities

This module provides file hashing utilities for the Purrify system.
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Optional


class HashUtils:
    """File hashing utility functions."""
    
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm: str = "md5", chunk_size: int = 8192) -> Optional[str]:
        """Calculate hash of a file using specified algorithm."""
        try:
            hash_obj = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except (OSError, PermissionError):
            return None
    
    @staticmethod
    def calculate_string_hash(text: str, algorithm: str = "md5") -> str:
        """Calculate hash of a string using specified algorithm."""
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def find_duplicate_files(file_paths: List[str], algorithm: str = "md5") -> Dict[str, List[str]]:
        """Find duplicate files based on hash."""
        hash_groups: Dict[str, List[str]] = {}
        
        for file_path in file_paths:
            file_hash = HashUtils.calculate_file_hash(file_path, algorithm)
            if file_hash:
                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []
                hash_groups[file_hash].append(file_path)
        
        # Return only groups with more than one file
        return {hash_val: files for hash_val, files in hash_groups.items() if len(files) > 1}
    
    @staticmethod
    def find_duplicates_by_size_and_hash(file_paths: List[str], algorithm: str = "md5") -> Dict[str, List[str]]:
        """Find duplicate files by first grouping by size, then by hash."""
        # Group files by size first
        size_groups: Dict[int, List[str]] = {}
        
        for file_path in file_paths:
            try:
                size = Path(file_path).stat().st_size
                if size not in size_groups:
                    size_groups[size] = []
                size_groups[size].append(file_path)
            except (OSError, PermissionError):
                continue
        
        # Find duplicates within each size group
        all_duplicates: Dict[str, List[str]] = {}
        
        for size, files in size_groups.items():
            if len(files) > 1:  # Only process groups with multiple files
                duplicates = HashUtils.find_duplicate_files(files, algorithm)
                all_duplicates.update(duplicates)
        
        return all_duplicates
    
    @staticmethod
    def verify_file_integrity(file_path: str, expected_hash: str, algorithm: str = "md5") -> bool:
        """Verify file integrity by comparing with expected hash."""
        actual_hash = HashUtils.calculate_file_hash(file_path, algorithm)
        return actual_hash == expected_hash if actual_hash else False
    
    @staticmethod
    def get_supported_algorithms() -> List[str]:
        """Get list of supported hash algorithms."""
        return [
            "md5",
            "sha1", 
            "sha256",
            "sha512",
            "blake2b",
            "blake2s"
        ]
    
    @staticmethod
    def is_hash_valid(hash_string: str, algorithm: str = "md5") -> bool:
        """Check if a hash string is valid for the given algorithm."""
        try:
            # Check if the hash length matches the expected length for the algorithm
            expected_lengths = {
                "md5": 32,
                "sha1": 40,
                "sha256": 64,
                "sha512": 128,
                "blake2b": 128,
                "blake2s": 64
            }
            
            expected_length = expected_lengths.get(algorithm, 32)
            return len(hash_string) == expected_length and all(c in '0123456789abcdef' for c in hash_string.lower())
        except (TypeError, AttributeError):
            return False 