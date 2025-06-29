# 🚀 Purrify Installation Guide

This guide will help you install Purrify with its beautiful Aphrodite-inspired GUI on your system.

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Platform**: macOS or Windows
- **Administrator privileges**: Required for some operations

## 🍎 macOS Installation

### 1. Install Python Dependencies

```bash
# Install Python tkinter (required for GUI)
brew install python-tk

# Verify tkinter installation
python3 -c "import tkinter; print('✅ Tkinter is available!')"
```

### 2. Clone and Setup Purrify

```bash
# Clone the repository
git clone https://github.com/yourusername/purrify.git
cd purrify

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 3. Verify Installation

```bash
# Test the installation
python test_installation.py

# Test CLI functionality
purrify --help
purrify scan --quick
```

### 4. Launch the Beautiful GUI

```bash
# Option 1: Use the launcher script
./launch_gui.py

# Option 2: Use the CLI command
purrify gui

# Option 3: Direct execution
python -m purrify.gui.main_window
```

## 🪟 Windows Installation

### 1. Install Python

Download and install Python 3.8+ from [python.org](https://python.org)

### 2. Clone and Setup Purrify

```cmd
# Clone the repository
git clone https://github.com/yourusername/purrify.git
cd purrify

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 3. Verify Installation

```cmd
# Test the installation
python test_installation.py

# Test CLI functionality
purrify --help
purrify scan --quick
```

### 4. Launch the Beautiful GUI

```cmd
# Option 1: Use the launcher script
python launch_gui.py

# Option 2: Use the CLI command
purrify gui

# Option 3: Direct execution
python -m purrify.gui.main_window
```

## 🐧 Linux Installation

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-tk python3-pip python3-venv

# Clone and setup
git clone https://github.com/yourusername/purrify.git
cd purrify

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Test and launch
python test_installation.py
./launch_gui.py
```

### Fedora/CentOS

```bash
# Install system dependencies
sudo dnf install python3-tkinter python3-pip

# Follow the same setup steps as Ubuntu
```

## 🔧 Troubleshooting

### Tkinter Issues

**Error**: `ModuleNotFoundError: No module named '_tkinter'`

**Solution**:
- **macOS**: `brew install python-tk`
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **Windows**: Reinstall Python with tkinter option checked

### Permission Issues

**Error**: Permission denied when running operations

**Solution**:
```bash
# Run with administrator privileges
sudo purrify scan --quick

# Or add your user to the appropriate groups
```

### Virtual Environment Issues

**Error**: Command not found: purrify

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall the package
pip install -e .
```

## 🎨 GUI Features

Once installed, you'll have access to:

- **🏠 Home Page**: System overview with quick actions
- **🔍 Scan Page**: Beautiful system scanning with fluid animations
- **🧹 Clean Page**: Safe cleaning operations with preview mode
- **⚡ Optimize Page**: Performance optimization with real-time feedback
- **📊 Reports Page**: Generate and save detailed reports
- **⚙️ Settings Page**: Configure application preferences

## 🚀 Quick Start

After installation:

1. **Activate the environment**:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Launch the GUI**:
   ```bash
   ./launch_gui.py
   ```

3. **Or use CLI**:
   ```bash
   purrify scan --quick    # Quick system scan
   purrify status          # System status
   purrify clean --safe    # Safe cleaning mode
   ```

## 🎉 Success!

You now have a beautiful, Aphrodite-inspired system optimization tool that:

- ✨ **Transforms system optimization into a beautiful experience**
- 🌊 **Features flowing animations that feel cleansing and purifying**
- 🎨 **Uses a color palette inspired by love, beauty, and grace**
- 🚀 **Provides intuitive, modern interface design**
- 🔧 **Maintains all the powerful functionality of Purrify**

**Enjoy the power of beauty and performance combined! ✨🐱** 