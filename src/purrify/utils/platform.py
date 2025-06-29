"""
Purrify Platform Utilities

This module provides platform detection and utility functions for
cross-platform compatibility between macOS and Windows.
"""

import os
import sys
import platform
import subprocess
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from loguru import logger


def detect_platform() -> Dict[str, Any]:
    """
    Detect the current platform and return detailed information.
    
    Returns:
        Dictionary containing platform information
    """
    system = platform.system().lower()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    
    platform_info = {
        "system": system,
        "release": release,
        "version": version,
        "machine": machine,
        "processor": processor,
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "architecture": platform.architecture()[0],
        "is_64bit": platform.architecture()[0] == "64bit"
    }
    
    # Platform-specific information
    if system == "darwin":  # macOS
        platform_info.update(_get_macos_info())
    elif system == "windows":
        platform_info.update(_get_windows_info())
    else:
        platform_info["supported"] = False
        logger.warning(f"Unsupported platform: {system}")
    
    platform_info["supported"] = system in ["darwin", "windows"]
    
    return platform_info


def _get_macos_info() -> Dict[str, Any]:
    """Get macOS-specific system information."""
    info = {
        "platform_type": "macOS",
        "supported": True
    }
    
    try:
        # Get macOS version
        result = subprocess.run(
            ["sw_vers", "-productVersion"],
            capture_output=True,
            text=True,
            check=True
        )
        info["macos_version"] = result.stdout.strip()
        
        # Get macOS build version
        result = subprocess.run(
            ["sw_vers", "-buildVersion"],
            capture_output=True,
            text=True,
            check=True
        )
        info["macos_build"] = result.stdout.strip()
        
        # Get macOS name
        result = subprocess.run(
            ["sw_vers", "-productName"],
            capture_output=True,
            text=True,
            check=True
        )
        info["macos_name"] = result.stdout.strip()
        
        # Check if running on Apple Silicon
        result = subprocess.run(
            ["uname", "-m"],
            capture_output=True,
            text=True,
            check=True
        )
        info["is_apple_silicon"] = result.stdout.strip() == "arm64"
        
        # Get system memory info
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"],
            capture_output=True,
            text=True,
            check=True
        )
        info["total_memory"] = int(result.stdout.strip())
        
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to get macOS info: {e}")
    
    return info


def _get_windows_info() -> Dict[str, Any]:
    """Get Windows-specific system information."""
    info = {
        "platform_type": "Windows",
        "supported": True
    }
    
    try:
        # Get Windows version
        result = subprocess.run(
            ["ver"],
            capture_output=True,
            text=True,
            check=True
        )
        info["windows_version"] = result.stdout.strip()
        
        # Get Windows build number
        result = subprocess.run(
            ["cmd", "/c", "echo %OSVERSION%"],
            capture_output=True,
            text=True,
            check=True
        )
        info["windows_build"] = result.stdout.strip()
        
        # Get system memory info
        import psutil
        info["total_memory"] = psutil.virtual_memory().total
        
    except (subprocess.CalledProcessError, ImportError) as e:
        logger.warning(f"Failed to get Windows info: {e}")
    
    return info


def get_system_paths() -> Dict[str, List[str]]:
    """
    Get platform-specific system paths for scanning and cleaning.
    
    Returns:
        Dictionary containing different types of system paths
    """
    system = platform.system().lower()
    
    if system == "darwin":
        return _get_macos_paths()
    elif system == "windows":
        return _get_windows_paths()
    else:
        return {"error": f"Unsupported platform: {system}"}


def _get_macos_paths() -> Dict[str, List[str]]:
    """Get macOS-specific system paths."""
    home = os.path.expanduser("~")
    
    return {
        "system_caches": [
            "/System/Library/Caches",
            "/Library/Caches",
            "/private/var/folders",
            "/private/var/cache",
            "/private/var/tmp"
        ],
        "user_caches": [
            f"{home}/Library/Caches",
            f"{home}/Library/Application Support",
            f"{home}/Library/Logs",
            f"{home}/Library/Saved Application State",
            f"{home}/Library/WebKit",
            f"{home}/.Trash"
        ],
        "application_caches": [
            f"{home}/Library/Caches/com.apple.Safari",
            f"{home}/Library/Caches/com.google.Chrome",
            f"{home}/Library/Caches/com.mozilla.firefox",
            f"{home}/Library/Caches/com.microsoft.VSCode",
            f"{home}/Library/Caches/com.jetbrains.intellij",
            f"{home}/Library/Caches/com.adobe.Photoshop",
            f"{home}/Library/Caches/com.adobe.Premiere Pro"
        ],
        "system_logs": [
            "/var/log",
            "/private/var/log",
            f"{home}/Library/Logs"
        ],
        "temp_files": [
            "/tmp",
            "/var/tmp",
            f"{home}/Library/Caches/TemporaryItems"
        ],
        "downloads": [
            f"{home}/Downloads",
            f"{home}/Desktop"
        ],
        "startup_items": [
            f"{home}/Library/LaunchAgents",
            "/Library/LaunchAgents",
            "/Library/LaunchDaemons",
            "/System/Library/LaunchAgents",
            "/System/Library/LaunchDaemons"
        ]
    }


def _get_windows_paths() -> Dict[str, List[str]]:
    """Get Windows-specific system paths."""
    home = os.path.expanduser("~")
    appdata = os.environ.get("APPDATA", f"{home}/AppData/Roaming")
    local_appdata = os.environ.get("LOCALAPPDATA", f"{home}/AppData/Local")
    temp = os.environ.get("TEMP", "C:/Windows/Temp")
    
    return {
        "system_caches": [
            "C:/Windows/Temp",
            "C:/Windows/Prefetch",
            "C:/Windows/SoftwareDistribution/Download",
            "C:/ProgramData/Microsoft/Windows/WER"
        ],
        "user_caches": [
            f"{local_appdata}/Temp",
            f"{local_appdata}/Microsoft/Windows/INetCache",
            f"{local_appdata}/Microsoft/Windows/WebCache",
            f"{appdata}/Microsoft/Windows/Recent",
            f"{appdata}/Microsoft/Windows/Recent/AutomaticDestinations"
        ],
        "application_caches": [
            f"{local_appdata}/Google/Chrome/User Data/Default/Cache",
            f"{local_appdata}/Mozilla/Firefox/Profiles",
            f"{local_appdata}/Microsoft/Edge/User Data/Default/Cache",
            f"{local_appdata}/Microsoft/Teams/current/Cache",
            f"{local_appdata}/Discord/Cache",
            f"{local_appdata}/Slack/Cache"
        ],
        "system_logs": [
            "C:/Windows/System32/winevt/Logs",
            "C:/Windows/Logs",
            "C:/ProgramData/Microsoft/Windows/WindowsUpdate/Log"
        ],
        "temp_files": [
            temp,
            f"{local_appdata}/Temp",
            f"{home}/AppData/Local/Temp"
        ],
        "downloads": [
            f"{home}/Downloads",
            f"{home}/Desktop"
        ],
        "startup_items": [
            "C:/Users/All Users/Microsoft/Windows/Start Menu/Programs/Startup",
            f"{home}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup",
            "C:/Windows/System32/config/systemprofile/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        ]
    }


def get_browser_paths() -> Dict[str, List[str]]:
    """
    Get browser-specific cache and data paths.
    
    Returns:
        Dictionary containing browser paths by browser name
    """
    system = platform.system().lower()
    home = os.path.expanduser("~")
    
    if system == "darwin":
        return {
            "safari": [
                f"{home}/Library/Safari",
                f"{home}/Library/Caches/com.apple.Safari",
                f"{home}/Library/WebKit"
            ],
            "chrome": [
                f"{home}/Library/Application Support/Google/Chrome/Default",
                f"{home}/Library/Caches/Google/Chrome",
                f"{home}/Library/Application Support/Google/Chrome/Default/Cache"
            ],
            "firefox": [
                f"{home}/Library/Application Support/Firefox/Profiles",
                f"{home}/Library/Caches/Firefox"
            ],
            "edge": [
                f"{home}/Library/Application Support/Microsoft Edge/Default",
                f"{home}/Library/Caches/Microsoft Edge"
            ]
        }
    elif system == "windows":
        appdata = os.environ.get("APPDATA", f"{home}/AppData/Roaming")
        local_appdata = os.environ.get("LOCALAPPDATA", f"{home}/AppData/Local")
        
        return {
            "chrome": [
                f"{local_appdata}/Google/Chrome/User Data/Default",
                f"{local_appdata}/Google/Chrome/User Data/Default/Cache",
                f"{local_appdata}/Google/Chrome/User Data/Default/Storage"
            ],
            "firefox": [
                f"{appdata}/Mozilla/Firefox/Profiles",
                f"{local_appdata}/Mozilla/Firefox/Profiles"
            ],
            "edge": [
                f"{local_appdata}/Microsoft/Edge/User Data/Default",
                f"{local_appdata}/Microsoft/Edge/User Data/Default/Cache"
            ],
            "ie": [
                f"{local_appdata}/Microsoft/Windows/INetCache",
                f"{local_appdata}/Microsoft/Windows/WebCache"
            ]
        }
    else:
        return {}


def check_permissions(path: str) -> Dict[str, Any]:
    """
    Check file system permissions for a given path.
    
    Args:
        path: Path to check permissions for
        
    Returns:
        Dictionary containing permission information
    """
    try:
        path_obj = Path(path)
        
        permissions = {
            "path": str(path),
            "exists": path_obj.exists(),
            "is_file": path_obj.is_file(),
            "is_dir": path_obj.is_dir(),
            "readable": os.access(path, os.R_OK),
            "writable": os.access(path, os.W_OK),
            "executable": os.access(path, os.X_OK)
        }
        
        if path_obj.exists():
            try:
                stat_info = path_obj.stat()
                permissions.update({
                    "size": stat_info.st_size,
                    "modified": stat_info.st_mtime,
                    "owner": stat_info.st_uid if hasattr(stat_info, 'st_uid') else None,
                    "group": stat_info.st_gid if hasattr(stat_info, 'st_gid') else None
                })
            except OSError as e:
                permissions["error"] = str(e)
        
        return permissions
        
    except Exception as e:
        return {
            "path": path,
            "error": str(e),
            "exists": False
        }


def get_disk_usage(path: str = "/") -> Dict[str, Any]:
    """
    Get disk usage information for a given path.
    
    Args:
        path: Path to check disk usage for
        
    Returns:
        Dictionary containing disk usage information
    """
    try:
        import psutil
        
        disk_usage = psutil.disk_usage(path)
        
        return {
            "path": path,
            "total": disk_usage.total,
            "used": disk_usage.used,
            "free": disk_usage.free,
            "percent_used": disk_usage.percent,
            "percent_free": 100 - disk_usage.percent
        }
        
    except ImportError:
        logger.warning("psutil not available, cannot get disk usage")
        return {"error": "psutil not available"}
    except Exception as e:
        return {"error": str(e)}


def get_memory_info() -> Dict[str, Any]:
    """
    Get system memory information.
    
    Returns:
        Dictionary containing memory information
    """
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        
        return {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "free": memory.free,
            "percent_used": memory.percent,
            "percent_free": 100 - memory.percent
        }
        
    except ImportError:
        logger.warning("psutil not available, cannot get memory info")
        return {"error": "psutil not available"}
    except Exception as e:
        return {"error": str(e)}


def is_admin() -> bool:
    """
    Check if the current process has administrative privileges.
    
    Returns:
        True if running with admin privileges, False otherwise
    """
    try:
        if platform.system().lower() == "windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def require_admin(func):
    """
    Decorator to require administrative privileges for a function.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        if not is_admin():
            raise PermissionError(
                "This operation requires administrative privileges. "
                "Please run the application as administrator/sudo."
            )
        return func(*args, **kwargs)
    
    return wrapper


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string
    """
    if bytes_value == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_value >= 1024 and i < len(size_names) - 1:
        bytes_value /= 1024.0
        i += 1
    
    return f"{bytes_value:.1f} {size_names[i]}"


def get_system_info() -> Dict[str, Any]:
    """
    Get comprehensive system information.
    
    Returns:
        Dictionary containing system information
    """
    info = detect_platform()
    
    # Add disk usage
    info["disk_usage"] = get_disk_usage()
    
    # Add memory info
    info["memory_info"] = get_memory_info()
    
    # Add system paths
    info["system_paths"] = get_system_paths()
    
    # Add browser paths
    info["browser_paths"] = get_browser_paths()
    
    # Add admin status
    info["is_admin"] = is_admin()
    
    return info 