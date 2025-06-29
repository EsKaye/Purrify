#!/usr/bin/env python3
"""
Purrify Installation Script

This script helps users install and set up Purrify on their system.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print installation banner."""
    print("🐱 Purrify - AI-Driven System Optimization Utility")
    print("=" * 50)
    print("Installation Script")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_platform():
    """Check if platform is supported."""
    print("\n🖥️ Checking platform...")
    
    system = platform.system().lower()
    if system in ["darwin", "windows"]:
        print(f"✅ Platform {system.title()} - Supported")
        return True
    else:
        print(f"⚠️ Platform {system.title()} - Limited support")
        return True  # Allow installation but warn

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install core requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Core dependencies installed")
        
        # Ask about optional dependencies
        install_ai = input("\n🤖 Install AI/ML dependencies? (y/N): ").lower().startswith('y')
        if install_ai:
            print("Installing AI/ML dependencies...")
            ai_deps = [
                "numpy==1.24.3",
                "pandas==2.0.3", 
                "scikit-learn==1.3.0"
            ]
            for dep in ai_deps:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print("✅ AI/ML dependencies installed")
        
        install_gui = input("\n🎮 Install GUI dependencies? (y/N): ").lower().startswith('y')
        if install_gui:
            print("Installing GUI dependencies...")
            gui_deps = [
                "customtkinter==5.2.0",
                "pillow==10.0.0"
            ]
            for dep in gui_deps:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print("✅ GUI dependencies installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_purrify():
    """Install Purrify in development mode."""
    print("\n🚀 Installing Purrify...")
    
    try:
        subprocess.check_call([sys.executable, "setup.py", "develop"])
        print("✅ Purrify installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Purrify: {e}")
        return False

def run_tests():
    """Run installation tests."""
    print("\n🧪 Running installation tests...")
    
    try:
        subprocess.check_call([sys.executable, "test_installation.py"])
        print("✅ All tests passed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = [
        "logs",
        "backups", 
        "config",
        "data",
        "models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/")

def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "=" * 50)
    print("🎉 Installation Complete!")
    print("=" * 50)
    
    print("\n🚀 Next Steps:")
    print("1. Test the installation:")
    print("   python test_installation.py")
    print("\n2. Run Purrify:")
    print("   purrify --help")
    print("   purrify scan")
    print("   purrify status")
    print("\n3. Launch GUI (if installed):")
    print("   purrify gui")
    
    print("\n📚 Documentation:")
    print("- README.md - Main documentation")
    print("- CONTRIBUTING.md - Development guide")
    
    print("\n🔧 Configuration:")
    print("- Edit config/purrify.yaml to customize settings")
    print("- Run 'purrify --help' for all available options")
    
    print("\n💡 Tips:")
    print("- Start with 'purrify scan --safe' to preview what can be cleaned")
    print("- Use '--verbose' flag for detailed output")
    print("- Run as administrator/sudo for full system access")

def main():
    """Main installation function."""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    check_platform()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Install Purrify
    if not install_purrify():
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Run tests
    if not run_tests():
        print("\n⚠️ Installation completed but tests failed.")
        print("You may still be able to use Purrify, but some features might not work.")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main() 