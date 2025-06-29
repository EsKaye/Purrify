#!/usr/bin/env python3
"""
Purrify Installation Test

This script tests that the Purrify installation is working correctly
by importing modules and running basic functionality.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all core modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        # Test core imports
        from purrify.core.config import Config
        from purrify.core.engine import PurrifyEngine
        from purrify.core.logger import setup_logger
        print("✅ Core modules imported successfully")
        
        # Test utility imports
        from purrify.utils.platform import detect_platform, format_bytes
        from purrify.utils.cli_utils import print_banner
        print("✅ Utility modules imported successfully")
        
        # Test scanner imports
        from purrify.scanners.system_scanner import SystemScanner
        print("✅ Scanner modules imported successfully")
        
        # Test cleaner imports
        from purrify.cleaners.cache_cleaner import CacheCleaner
        print("✅ Cleaner modules imported successfully")
        
        # Test optimizer imports
        from purrify.optimizers.performance_optimizer import PerformanceOptimizer
        print("✅ Optimizer modules imported successfully")
        
        # Test AI imports
        from purrify.ai.intelligence_engine import IntelligenceEngine
        print("✅ AI modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\n⚙️ Testing configuration...")
    
    try:
        from purrify.core.config import Config
        
        # Test default configuration
        config = Config()
        print("✅ Default configuration loaded")
        
        # Test configuration validation
        if config.validate():
            print("✅ Configuration validation passed")
        else:
            print("❌ Configuration validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_platform_detection():
    """Test platform detection."""
    print("\n🖥️ Testing platform detection...")
    
    try:
        from purrify.utils.platform import detect_platform, get_system_paths
        
        # Test platform detection
        platform_info = detect_platform()
        print(f"✅ Platform detected: {platform_info.get('platform_type', 'Unknown')}")
        
        # Test system paths
        system_paths = get_system_paths()
        if "error" not in system_paths:
            print("✅ System paths retrieved successfully")
        else:
            print(f"❌ System paths failed: {system_paths['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Platform detection failed: {e}")
        return False

def test_engine_initialization():
    """Test engine initialization."""
    print("\n🚀 Testing engine initialization...")
    
    try:
        from purrify.core.config import Config
        from purrify.core.engine import PurrifyEngine
        
        # Initialize configuration and engine
        config = Config()
        engine = PurrifyEngine(config)
        print("✅ Engine initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Engine initialization failed: {e}")
        return False

def test_cli_utilities():
    """Test CLI utilities."""
    print("\n🖥️ Testing CLI utilities...")
    
    try:
        from purrify.utils.cli_utils import format_bytes
        
        # Test byte formatting
        test_bytes = 1024 * 1024 * 100  # 100 MB
        formatted = format_bytes(test_bytes)
        print(f"✅ Byte formatting: {test_bytes} -> {formatted}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI utilities test failed: {e}")
        return False

def main():
    """Run all installation tests."""
    print("🐱 Purrify Installation Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_configuration,
        test_platform_detection,
        test_engine_initialization,
        test_cli_utilities
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ Test {test.__name__} failed")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Purrify is ready to use.")
        print("\n🚀 You can now run:")
        print("   purrify --help")
        print("   purrify scan")
        print("   purrify status")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 