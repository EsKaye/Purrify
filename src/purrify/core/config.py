"""
Purrify Configuration Management

This module handles configuration loading, validation, and management
for the Purrify system optimization utility.
"""

import os
import yaml
import platform
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class GeneralConfig:
    """General application configuration settings."""
    safe_mode: bool = True
    auto_backup: bool = True
    max_backup_size: str = "1GB"
    log_level: str = "INFO"
    enable_ai: bool = True
    data_retention_days: int = 30


@dataclass
class ScanningConfig:
    """System scanning configuration settings."""
    include_system_caches: bool = True
    include_user_caches: bool = True
    include_application_caches: bool = True
    include_browser_caches: bool = True
    include_logs: bool = True
    include_temp_files: bool = True
    quick_mode: bool = False
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "*.important",
        "backup/*",
        "*.backup",
        "*.bak"
    ])
    max_scan_depth: int = 10
    scan_timeout: int = 300  # seconds


@dataclass
class CleaningConfig:
    """System cleaning configuration settings."""
    browser_caches: bool = True
    system_logs: bool = True
    temp_files: bool = True
    download_history: bool = False
    application_caches: bool = True
    system_caches: bool = True
    user_caches: bool = True
    min_file_age_hours: int = 24
    confirm_deletion: bool = True
    dry_run: bool = False


@dataclass
class OptimizationConfig:
    """System optimization configuration settings."""
    startup_optimization: bool = True
    memory_optimization: bool = True
    disk_optimization: bool = True
    registry_optimization: bool = True  # Windows only
    launch_agents_optimization: bool = True  # macOS only
    background_processes: bool = True
    power_optimization: bool = True
    # Windows 11 specific optimizations
    windows_11_optimizations: bool = True
    wsl_optimization: bool = False
    microsoft_store_optimization: bool = False
    windows_terminal_optimization: bool = False
    cloud_integration_optimization: bool = True


@dataclass
class AIConfig:
    """AI/ML configuration settings."""
    enable_ml_analysis: bool = True
    model_path: str = "models/"
    confidence_threshold: float = 0.8
    enable_learning: bool = True
    training_data_path: str = "data/training/"
    prediction_cache_size: int = 1000


@dataclass
class SecurityConfig:
    """Security and safety configuration settings."""
    whitelist_paths: List[str] = field(default_factory=lambda: [
        "/System/",
        "/Applications/",
        "/Users/*/Documents/",
        "/Users/*/Desktop/"
    ])
    blacklist_paths: List[str] = field(default_factory=lambda: [
        "/System/Library/",
        "/Library/",
        "/bin/",
        "/sbin/",
        "/usr/bin/",
        "/usr/sbin/"
    ])
    require_confirmation: bool = True
    backup_critical_files: bool = True
    validate_file_signatures: bool = True


class Config:
    """
    Main configuration class for Purrify.
    
    Handles loading, validation, and access to all configuration settings
    across different platforms and use cases.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration with optional custom config file path.
        
        Args:
            config_path: Path to custom configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.platform = platform.system().lower()
        
        # Initialize configuration sections
        self.general = GeneralConfig()
        self.scanning = ScanningConfig()
        self.cleaning = CleaningConfig()
        self.optimization = OptimizationConfig()
        self.ai = AIConfig()
        self.security = SecurityConfig()
        
        # Load configuration
        self._load_config()
        self._apply_platform_specific_settings()
        
        logger.info(f"Configuration loaded from: {self.config_path}")
    
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        # Try to find config in current directory
        current_dir = Path.cwd()
        config_files = [
            current_dir / "config" / "purrify.yaml",
            current_dir / "purrify.yaml",
            current_dir / "config.yaml",
        ]
        
        for config_file in config_files:
            if config_file.exists():
                return str(config_file)
        
        # Return default path for creation
        return str(current_dir / "config" / "purrify.yaml")
    
    def _load_config(self):
        """Load configuration from YAML file."""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            logger.warning(f"Configuration file not found: {self.config_path}")
            logger.info("Creating default configuration file...")
            self._create_default_config()
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}
            
            # Update configuration sections
            self._update_section(self.general, config_data.get('general', {}))
            self._update_section(self.scanning, config_data.get('scanning', {}))
            self._update_section(self.cleaning, config_data.get('cleaning', {}))
            self._update_section(self.optimization, config_data.get('optimization', {}))
            self._update_section(self.ai, config_data.get('ai', {}))
            self._update_section(self.security, config_data.get('security', {}))
            
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            logger.info("Using default configuration")
    
    def _update_section(self, section: Any, data: Dict[str, Any]):
        """Update a configuration section with new data."""
        for key, value in data.items():
            if hasattr(section, key):
                setattr(section, key, value)
    
    def _create_default_config(self):
        """Create a default configuration file."""
        config_dir = Path(self.config_path).parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        default_config = {
            'general': {
                'safe_mode': True,
                'auto_backup': True,
                'max_backup_size': '1GB',
                'log_level': 'INFO',
                'enable_ai': True,
                'data_retention_days': 30
            },
            'scanning': {
                'include_system_caches': True,
                'include_user_caches': True,
                'include_application_caches': True,
                'include_browser_caches': True,
                'include_logs': True,
                'include_temp_files': True,
                'quick_mode': False,
                'exclude_patterns': [
                    '*.important',
                    'backup/*',
                    '*.backup',
                    '*.bak'
                ],
                'max_scan_depth': 10,
                'scan_timeout': 300
            },
            'cleaning': {
                'browser_caches': True,
                'system_logs': True,
                'temp_files': True,
                'download_history': False,
                'application_caches': True,
                'system_caches': True,
                'user_caches': True,
                'min_file_age_hours': 24,
                'confirm_deletion': True,
                'dry_run': False
            },
            'optimization': {
                'startup_optimization': True,
                'memory_optimization': True,
                'disk_optimization': True,
                'registry_optimization': True,
                'launch_agents_optimization': True,
                'background_processes': True,
                'power_optimization': True
            },
            'ai': {
                'enable_ml_analysis': True,
                'model_path': 'models/',
                'confidence_threshold': 0.8,
                'enable_learning': True,
                'training_data_path': 'data/training/',
                'prediction_cache_size': 1000
            },
            'security': {
                'whitelist_paths': [
                    '/System/',
                    '/Applications/',
                    '/Users/*/Documents/',
                    '/Users/*/Desktop/'
                ],
                'blacklist_paths': [
                    '/System/Library/',
                    '/Library/',
                    '/bin/',
                    '/sbin/',
                    '/usr/bin/',
                    '/usr/sbin/'
                ],
                'require_confirmation': True,
                'backup_critical_files': True,
                'validate_file_signatures': True
            }
        }
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, indent=2)
            logger.info(f"Default configuration created: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to create default configuration: {e}")
    
    def _apply_platform_specific_settings(self):
        """Apply platform-specific configuration settings."""
        if self.platform == "darwin":  # macOS
            self._apply_macos_settings()
        elif self.platform == "windows":
            self._apply_windows_settings()
        else:
            logger.warning(f"Unsupported platform: {self.platform}")
    
    def _apply_macos_settings(self):
        """Apply macOS-specific configuration settings."""
        # Add macOS-specific paths
        self.security.whitelist_paths.extend([
            "/Applications/",
            "/System/Applications/",
            "/Users/*/Library/Application Support/",
            "/Users/*/Library/Preferences/"
        ])
        
        self.security.blacklist_paths.extend([
            "/System/Library/",
            "/Library/",
            "/private/",
            "/.Spotlight-V100/",
            "/.fseventsd/"
        ])
        
        # Disable Windows-specific optimizations
        self.optimization.registry_optimization = False
        
        logger.info("Applied macOS-specific configuration")
    
    def _apply_windows_settings(self):
        """Apply Windows-specific configuration settings."""
        # Add Windows-specific paths
        self.security.whitelist_paths.extend([
            "C:\\Program Files\\",
            "C:\\Program Files (x86)\\",
            "C:\\Users\\*\\Documents\\",
            "C:\\Users\\*\\Desktop\\",
            "C:\\Users\\*\\OneDrive\\"  # Protect OneDrive files
        ])
        
        self.security.blacklist_paths.extend([
            "C:\\Windows\\",
            "C:\\Windows\\System32\\",
            "C:\\Windows\\SysWOW64\\",
            "C:\\ProgramData\\",
            "C:\\Windows\\WinSxS\\",  # Windows component store
            "C:\\Windows\\System32\\config\\"  # Registry files
        ])
        
        # Disable macOS-specific optimizations
        self.optimization.launch_agents_optimization = False
        
        # Windows 11 specific settings
        if hasattr(self, 'platform') and self.platform.get("is_windows_11", False):
            self._apply_windows_11_settings()
        
        logger.info("Applied Windows-specific configuration")
    
    def _apply_windows_11_settings(self):
        """Apply Windows 11 specific configuration settings."""
        logger.info("Detected Windows 11 - applying specific optimizations")
        
        # Add Windows 11 specific whitelist paths
        self.security.whitelist_paths.extend([
            "C:\\Program Files\\WindowsApps\\",  # Microsoft Store apps
            "C:\\Users\\*\\AppData\\Local\\Packages\\",  # UWP app data
            "C:\\Users\\*\\AppData\\Local\\Microsoft\\Windows\\Explorer\\",  # Explorer settings
            "C:\\Users\\*\\AppData\\Local\\Microsoft\\Windows\\Shell\\"  # Shell settings
        ])
        
        # Add Windows 11 specific blacklist paths
        self.security.blacklist_paths.extend([
            "C:\\Windows\\System32\\winevt\\Logs\\",  # Event logs (be careful)
            "C:\\Windows\\System32\\config\\systemprofile\\",  # System profile
            "C:\\ProgramData\\Microsoft\\Windows Defender\\"  # Defender files
        ])
        
        logger.info("Applied Windows 11 specific configuration")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key (e.g., 'general.safe_mode')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            keys = key.split('.')
            value = self
            
            for k in keys:
                value = getattr(value, k)
            
            return value
        except AttributeError:
            return default
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value by key.
        
        Args:
            key: Configuration key (e.g., 'general.safe_mode')
            value: Value to set
        """
        try:
            keys = key.split('.')
            obj = self
            
            for k in keys[:-1]:
                obj = getattr(obj, k)
            
            setattr(obj, keys[-1], value)
        except AttributeError as e:
            logger.error(f"Failed to set configuration key '{key}': {e}")
    
    def save(self, path: Optional[str] = None):
        """
        Save current configuration to file.
        
        Args:
            path: Optional custom path to save configuration
        """
        save_path = path or self.config_path
        
        config_data = {
            'general': self._section_to_dict(self.general),
            'scanning': self._section_to_dict(self.scanning),
            'cleaning': self._section_to_dict(self.cleaning),
            'optimization': self._section_to_dict(self.optimization),
            'ai': self._section_to_dict(self.ai),
            'security': self._section_to_dict(self.security)
        }
        
        try:
            save_dir = Path(save_path).parent
            save_dir.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to: {save_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def _section_to_dict(self, section: Any) -> Dict[str, Any]:
        """Convert a configuration section to dictionary."""
        return {
            key: getattr(section, key)
            for key in section.__annotations__.keys()
        }
    
    def validate(self) -> bool:
        """
        Validate current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Validate general settings
            if self.general.data_retention_days < 1:
                logger.error("data_retention_days must be at least 1")
                return False
            
            # Validate scanning settings
            if self.scanning.max_scan_depth < 1:
                logger.error("max_scan_depth must be at least 1")
                return False
            
            if self.scanning.scan_timeout < 30:
                logger.error("scan_timeout must be at least 30 seconds")
                return False
            
            # Validate AI settings
            if not 0.0 <= self.ai.confidence_threshold <= 1.0:
                logger.error("confidence_threshold must be between 0.0 and 1.0")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False 