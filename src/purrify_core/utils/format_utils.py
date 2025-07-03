"""
Format Utilities

This module provides data formatting utilities for the Purrify system.
"""

import json
import yaml
from datetime import datetime, timedelta
from typing import Dict, Any, List, Union


class FormatUtils:
    """Data formatting utility functions."""
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes into human-readable format."""
        if bytes_value == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
        i = 0
        while bytes_value >= 1024 and i < len(size_names) - 1:
            bytes_value /= 1024.0
            i += 1
        
        return f"{bytes_value:.1f} {size_names[i]}"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in seconds to human-readable format."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def format_percentage(value: float, total: float) -> str:
        """Format percentage value."""
        if total == 0:
            return "0.0%"
        percentage = (value / total) * 100
        return f"{percentage:.1f}%"
    
    @staticmethod
    def format_timestamp(timestamp: Union[float, datetime]) -> str:
        """Format timestamp to readable string."""
        if isinstance(timestamp, float):
            dt = datetime.fromtimestamp(timestamp)
        else:
            dt = timestamp
        
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"
    
    @staticmethod
    def format_file_path(file_path: str, max_length: int = 50) -> str:
        """Format file path for display, truncating if too long."""
        if len(file_path) <= max_length:
            return file_path
        
        # Try to keep the filename and truncate the path
        path_parts = file_path.split('/')
        if len(path_parts) > 1:
            filename = path_parts[-1]
            path_part = '/'.join(path_parts[:-1])
            
            # Calculate how much space we have for the path
            available_space = max_length - len(filename) - 3  # 3 for "..."
            
            if available_space > 0:
                return f"...{path_part[-available_space:]}/{filename}"
            else:
                return f"...{filename[-max_length+3:]}"
        else:
            return f"...{file_path[-max_length+3:]}"
    
    @staticmethod
    def format_list(items: List[Any], max_items: int = 5) -> str:
        """Format a list for display, truncating if too long."""
        if len(items) <= max_items:
            return ", ".join(str(item) for item in items)
        else:
            displayed = items[:max_items]
            return f"{', '.join(str(item) for item in displayed)}... (+{len(items) - max_items} more)"
    
    @staticmethod
    def to_json(data: Any, indent: int = 2) -> str:
        """Convert data to JSON string."""
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def from_json(json_string: str) -> Any:
        """Parse JSON string to data."""
        return json.loads(json_string)
    
    @staticmethod
    def to_yaml(data: Any) -> str:
        """Convert data to YAML string."""
        return yaml.dump(data, default_flow_style=False, indent=2)
    
    @staticmethod
    def from_yaml(yaml_string: str) -> Any:
        """Parse YAML string to data."""
        return yaml.safe_load(yaml_string)
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List[Any]], max_width: int = 80) -> str:
        """Format data as a table."""
        if not headers or not rows:
            return ""
        
        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width_col = len(str(header))
            for row in rows:
                if i < len(row):
                    max_width_col = max(max_width_col, len(str(row[i])))
            col_widths.append(min(max_width_col, max_width // len(headers)))
        
        # Build table
        table_lines = []
        
        # Header
        header_line = " | ".join(str(header)[:width].ljust(width) for header, width in zip(headers, col_widths))
        table_lines.append(header_line)
        table_lines.append("-" * len(header_line))
        
        # Rows
        for row in rows:
            row_line = " | ".join(str(cell)[:width].ljust(width) for cell, width in zip(row, col_widths))
            table_lines.append(row_line)
        
        return "\n".join(table_lines)
    
    @staticmethod
    def format_progress_bar(current: int, total: int, width: int = 50) -> str:
        """Format a progress bar."""
        if total == 0:
            return "[" + " " * width + "] 0%"
        
        percentage = (current / total) * 100
        filled_width = int((current / total) * width)
        
        bar = "█" * filled_width + "░" * (width - filled_width)
        return f"[{bar}] {percentage:.1f}%"
    
    @staticmethod
    def format_elapsed_time(start_time: datetime, end_time: datetime = None) -> str:
        """Format elapsed time between two timestamps."""
        if end_time is None:
            end_time = datetime.now()
        
        elapsed = end_time - start_time
        total_seconds = elapsed.total_seconds()
        
        if total_seconds < 60:
            return f"{total_seconds:.1f} seconds"
        elif total_seconds < 3600:
            minutes = total_seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = total_seconds / 3600
            return f"{hours:.1f} hours"
    
    @staticmethod
    def format_speed(bytes_per_second: float) -> str:
        """Format speed in bytes per second."""
        return f"{FormatUtils.format_bytes(int(bytes_per_second))}/s"
    
    @staticmethod
    def format_eta(remaining_bytes: int, bytes_per_second: float) -> str:
        """Format estimated time to completion."""
        if bytes_per_second <= 0:
            return "Unknown"
        
        remaining_seconds = remaining_bytes / bytes_per_second
        return FormatUtils.format_duration(remaining_seconds) 