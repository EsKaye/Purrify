"""
Purrify Platform Utilities

This module provides platform detection and utility functions for
cross-platform compatibility between macOS and Windows.

The platform utilities provide:
- Comprehensive platform detection and information gathering
- Cross-platform path mapping and system directory discovery
- Browser cache and data path detection
- System permission and access validation
- Disk usage and memory information gathering
- Platform-specific optimization and safety features

Functions:
    detect_platform: Detect current platform with detailed information
    get_system_paths: Get platform-specific system paths for scanning
    get_browser_paths: Get browser cache and data paths
    check_permissions: Check file system permissions for paths
    get_disk_usage: Get disk usage information
    get_memory_info: Get memory usage information
    is_admin: Check if running with administrative privileges

Author: Purrify Team
Version: 2.0.0
License: MIT
"""

import os
import sys
import platform
import subprocess
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from loguru import logger


def detect_platform() -> Dict[str, Any]:
    """
    Detect the current platform and return detailed information.
    
    This function provides comprehensive platform detection including
    system type, version, architecture, and platform-specific features.
    It supports macOS and Windows with detailed version information
    and feature detection.
    
    Returns:
        Dictionary containing comprehensive platform information:
        - system: Operating system name (darwin, windows, linux)
        - platform_type: Human-readable platform name
        - release: OS release version
        - version: OS version string
        - machine: Machine architecture
        - processor: Processor information
        - python_version: Python version string
        - architecture: System architecture (32bit, 64bit)
        - is_64bit: Whether system is 64-bit
        - supported: Whether platform is supported
        - Platform-specific fields (macos_version, windows_11_build, etc.)
        
    Raises:
        RuntimeError: If platform detection fails completely
        
    Example:
        >>> platform_info = detect_platform()
        >>> print(f"Platform: {platform_info['platform_type']}")
        >>> print(f"Architecture: {platform_info['architecture']}")
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
    """
    Get Windows-specific system information.
    
    This function provides comprehensive Windows system information
    using platform detection and file system checks rather than
    external commands that may not be available.
    """
    info = {
        "platform_type": "Windows",
        "supported": True
    }
    
    try:
        # Use platform module for basic version info
        info["windows_version"] = platform.version()
        info["windows_build"] = platform.release()
        
        # Detect Windows 11 using platform version
        # Windows 11 typically has build number >= 22000
        try:
            build_number = int(platform.release())
            info["is_windows_11"] = build_number >= 22000
            if info["is_windows_11"]:
                info["windows_11_build"] = str(build_number)
                info["is_latest_windows_11"] = build_number >= 22000
            else:
                info["is_windows_11"] = False
                info["windows_11_build"] = None
                info["is_latest_windows_11"] = False
        except (ValueError, TypeError):
            # Fallback: check for Windows 11 specific features
            info["is_windows_11"] = os.path.exists("C:\\Windows\\System32\\wsl.exe")
            info["windows_11_build"] = None
            info["is_latest_windows_11"] = False
        
        # Get system memory info
        try:
            import psutil
            info["total_memory"] = psutil.virtual_memory().total
        except ImportError:
            info["total_memory"] = 0
            logger.warning("psutil not available, memory info unavailable")
        
        # Check for Windows 11 specific features
        info["has_wsl"] = os.path.exists("C:\\Windows\\System32\\wsl.exe")
        info["has_windows_terminal"] = os.path.exists(os.path.expanduser("~\\AppData\\Local\\Microsoft\\WindowsTerminal"))
        info["has_microsoft_store"] = os.path.exists("C:\\Program Files\\WindowsApps")
        
        logger.info(f"Windows platform info gathered successfully")
        
    except Exception as e:
        logger.warning(f"Failed to get Windows info: {e}")
        # Provide fallback information
        info.update({
            "windows_version": "Unknown",
            "windows_build": "Unknown",
            "is_windows_11": False,
            "windows_11_build": None,
            "is_latest_windows_11": False,
            "total_memory": 0,
            "has_wsl": False,
            "has_windows_terminal": False,
            "has_microsoft_store": False
        })
    
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
    
    # Base Windows paths
    base_paths = {
        "system_caches": [
            "C:/Windows/Temp",
            "C:/Windows/Prefetch",
            "C:/Windows/SoftwareDistribution/Download",
            "C:/ProgramData/Microsoft/Windows/WER",
            "C:/Windows/WinSxS/Temp",  # Windows 11 component store temp
            "C:/Windows/System32/config/systemprofile/AppData/Local/Temp"  # System temp
        ],
        "user_caches": [
            f"{local_appdata}/Temp",
            f"{local_appdata}/Microsoft/Windows/INetCache",
            f"{local_appdata}/Microsoft/Windows/WebCache",
            f"{local_appdata}/Microsoft/Windows/History",
            f"{local_appdata}/Microsoft/Windows/Temporary Internet Files",
            f"{local_appdata}/Microsoft/Windows/Explorer",
            f"{local_appdata}/Microsoft/Windows/Shell",
            f"{appdata}/Microsoft/Windows/Recent",
            f"{appdata}/Microsoft/Windows/Recent/AutomaticDestinations",
            f"{local_appdata}/Microsoft/Windows/WER"  # User error reporting
        ],
        "application_caches": [
            f"{local_appdata}/Google/Chrome/User Data/Default/Cache",
            f"{local_appdata}/Google/Chrome/User Data/Default/Storage",
            f"{local_appdata}/Mozilla/Firefox/Profiles",
            f"{local_appdata}/Microsoft/Edge/User Data/Default/Cache",
            f"{local_appdata}/Microsoft/Edge/User Data/Default/Storage",
            f"{local_appdata}/Microsoft/Teams/current/Cache",
            f"{local_appdata}/Discord/Cache",
            f"{local_appdata}/Slack/Cache",
            f"{local_appdata}/Microsoft/WindowsTerminal",  # Windows Terminal cache
            f"{local_appdata}/Microsoft/Windows/INetCache/Content.IE5",  # IE cache
            f"{local_appdata}/Microsoft/Windows/WebCache/V01"  # Web cache
        ],
        "system_logs": [
            "C:/Windows/System32/winevt/Logs",
            "C:/Windows/Logs",
            "C:/ProgramData/Microsoft/Windows/WindowsUpdate/Log",
            "C:/Windows/System32/config/systemprofile/AppData/Local/Microsoft/Windows/INetCache/Logs"
        ],
        "temp_files": [
            temp,
            f"{local_appdata}/Temp",
            f"{home}/AppData/Local/Temp",
            f"{local_appdata}/Microsoft/Windows/INetCache/Temp"
        ],
        "downloads": [
            f"{home}/Downloads",
            f"{home}/Desktop",
            f"{home}/OneDrive/Downloads" if os.path.exists(f"{home}/OneDrive") else None
        ],
        "startup_items": [
            "C:/Users/All Users/Microsoft/Windows/Start Menu/Programs/Startup",
            f"{home}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup",
            "C:/Windows/System32/config/systemprofile/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        ]
    }
    
    # Windows 11 specific paths
    windows_11_paths = {
        "wsl_caches": [
            f"{local_appdata}/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc",
            f"{local_appdata}/Packages/TheDebianProject.DebianGNULinux_76v4gfsz19hv4",
            f"{local_appdata}/Packages/OpenMediaVault.WSL_1.0.0.0_x64__q4m6cd70nt8jt"
        ],
        "microsoft_store_caches": [
            "C:/Program Files/WindowsApps",
            f"{local_appdata}/Packages",
            f"{local_appdata}/Microsoft/Windows/INetCache/Packages"
        ],
        "windows_security_caches": [
            f"{local_appdata}/Microsoft/Windows Defender",
            f"{local_appdata}/Microsoft/Windows Defender Advanced Threat Protection",
            "C:/ProgramData/Microsoft/Windows Defender/Scans/History"
        ],
        "windows_search_caches": [
            f"{local_appdata}/Microsoft/Search/Data/Applications/Windows",
            f"{local_appdata}/Microsoft/Windows/Search/Data/Applications/Windows"
        ],
        "cloud_integration_caches": [
            f"{local_appdata}/Microsoft/OneDrive",
            f"{local_appdata}/Microsoft/Teams",
            f"{local_appdata}/Microsoft/Office",
            f"{local_appdata}/Microsoft/Outlook"
        ]
    }
    
    # Combine base paths with Windows 11 specific paths
    all_paths = base_paths.copy()
    all_paths.update(windows_11_paths)
    
    # Remove None values
    for category, paths in all_paths.items():
        all_paths[category] = [path for path in paths if path is not None]
    
    return all_paths


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
                f"{local_appdata}/Google/Chrome/User Data/Default/Storage",
                f"{local_appdata}/Google/Chrome/User Data/Default/Code Cache",
                f"{local_appdata}/Google/Chrome/User Data/Default/GPUCache"
            ],
            "firefox": [
                f"{appdata}/Mozilla/Firefox/Profiles",
                f"{local_appdata}/Mozilla/Firefox/Profiles",
                f"{local_appdata}/Mozilla/Firefox/Profiles/*/cache2",
                f"{local_appdata}/Mozilla/Firefox/Profiles/*/storage"
            ],
            "edge": [
                f"{local_appdata}/Microsoft/Edge/User Data/Default",
                f"{local_appdata}/Microsoft/Edge/User Data/Default/Cache",
                f"{local_appdata}/Microsoft/Edge/User Data/Default/Storage",
                f"{local_appdata}/Microsoft/Edge/User Data/Default/Code Cache",
                f"{local_appdata}/Microsoft/Edge/User Data/Default/GPUCache"
            ],
            "ie": [
                f"{local_appdata}/Microsoft/Windows/INetCache",
                f"{local_appdata}/Microsoft/Windows/WebCache",
                f"{local_appdata}/Microsoft/Windows/INetCache/Content.IE5"
            ],
            "opera": [
                f"{local_appdata}/Opera Software/Opera Stable",
                f"{local_appdata}/Opera Software/Opera Stable/Cache",
                f"{local_appdata}/Opera Software/Opera Stable/Storage"
            ],
            "brave": [
                f"{local_appdata}/BraveSoftware/Brave-Browser/User Data/Default",
                f"{local_appdata}/BraveSoftware/Brave-Browser/User Data/Default/Cache",
                f"{local_appdata}/BraveSoftware/Brave-Browser/User Data/Default/Storage"
            ],
            "vivaldi": [
                f"{local_appdata}/Vivaldi/User Data/Default",
                f"{local_appdata}/Vivaldi/User Data/Default/Cache",
                f"{local_appdata}/Vivaldi/User Data/Default/Storage"
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