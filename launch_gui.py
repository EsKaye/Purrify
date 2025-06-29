#!/usr/bin/env python3
"""
Purrify GUI Launcher

This script launches the beautiful Aphrodite-inspired GUI for Purrify.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Launch the Purrify GUI."""
    try:
        print("🐱 Launching Purrify GUI...")
        print("✨ Preparing Aphrodite-inspired interface...")
        
        # Import and launch GUI
        from purrify.gui.main_window import launch_gui
        launch_gui()
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have activated the virtual environment:")
        print("   source venv/bin/activate")
        print("   pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 