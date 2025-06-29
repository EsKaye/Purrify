#!/bin/bash

# Purrify Virtual Environment Activation Script
# This script activates the virtual environment and sets up Purrify

echo "🐱 Activating Purrify virtual environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if not already installed
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    pip install -e .
fi

echo "✅ Purrify is ready to use!"
echo ""
echo "🚀 Available commands:"
echo "   purrify --help          # Show all commands"
echo "   purrify scan --quick    # Quick system scan"
echo "   purrify status          # System status"
echo "   purrify clean --safe    # Safe cleaning mode"
echo ""
echo "💡 To deactivate the virtual environment, run: deactivate" 