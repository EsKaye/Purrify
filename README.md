# 🐱 Purrify - AI-Driven System Optimization Utility

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-blue.svg)](https://www.apple.com/macos/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![AI-Powered](https://img.shields.io/badge/AI-Powered-FF6B6B.svg)](https://github.com/your-username/purrify)

> **Transform your system optimization into a beautiful, Aphrodite-inspired experience**

Purrify is a cross-platform system optimization utility that combines powerful AI-driven analysis with a stunning, fluid GUI inspired by the goddess of love and beauty. Experience system optimization like never before with flowing animations, graceful interfaces, and intuitive design.

## 🚀 Features

### 🎨 **Beautiful Aphrodite-Inspired GUI**
- **Flowing Animations**: Water-like ripple effects and smooth transitions
- **Graceful Color Palette**: Soft rose pinks, azure blues, and lavender purples
- **Intuitive Design**: Modern, responsive interface that feels like a spa for your computer
- **Real-time Feedback**: Live system monitoring with beautiful visualizations

### 🔧 **Powerful System Optimization**
- **AI-Driven Analysis**: Intelligent scanning and optimization recommendations
- **Enhanced Scanning**: Duplicate detection, photo analysis, large file identification
- **Safe Cleaning**: Preview mode and intelligent file categorization
- **Performance Optimization**: Real-time system monitoring and optimization
- **Cross-Platform**: Works seamlessly on macOS and Windows

### 🚀 **Advanced Features**
- **Modular Architecture**: Extensible design for custom optimizations
- **Comprehensive Logging**: Detailed operation tracking and error reporting
- **Configuration Management**: Flexible settings for different use cases
- **CLI & GUI**: Both command-line and graphical interfaces available
- **Deep Scanning**: Advanced duplicate detection with MD5 hashing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- macOS or Windows
- Administrator privileges (for some operations)

### Installation

**📖 For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)**

#### Quick Setup (macOS):
```bash
# Install tkinter (required for GUI)
brew install python-tk

# Clone and setup
git clone https://github.com/yourusername/purrify.git
cd purrify

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Launch the beautiful GUI
./launch_gui.py
```

#### Quick Setup (Windows):
```cmd
# Clone and setup
git clone https://github.com/yourusername/purrify.git
cd purrify

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Launch the beautiful GUI
python launch_gui.py
```

## 🎮 Usage

### GUI Mode (Recommended)
```bash
# Launch the beautiful Aphrodite-inspired interface
./launch_gui.py

# Or use the CLI command
purrify gui
```

### CLI Mode
```bash
# Quick system scan
purrify scan --quick

# Full system analysis with enhanced features
purrify scan --detailed

# Scan for specific optimization opportunities
purrify scan --duplicates    # Find duplicate files
purrify scan --photos        # Analyze photos for optimization
purrify scan --large-files   # Identify large files

# Safe cleaning mode
purrify clean --safe

# Performance optimization
purrify optimize

# Generate system report
purrify report

# Show system status
purrify status
```

## 🏗️ Architecture

```
src/purrify/
├── ai/                    # AI intelligence engine
├── cleaners/              # Cache and file cleaning
├── core/                  # Core engine and configuration
├── gui/                   # Beautiful Aphrodite-inspired GUI
├── optimizers/            # Performance optimization
├── scanners/              # System scanning
└── utils/                 # Platform and CLI utilities
```

## 🎨 GUI Features

### **🏠 Home Page**
- System overview with quick actions
- Real-time performance metrics
- Beautiful status indicators

### **🔍 Scan Page**
- Fluid scanning animations
- Real-time progress with water-like effects
- Detailed file categorization

### **🧹 Clean Page**
- Safe preview mode
- Intelligent file selection
- Graceful cleaning animations

### **⚡ Optimize Page**
- Performance optimization tools
- Real-time system monitoring
- Beautiful progress visualizations

### **📊 Reports Page**
- Generate detailed reports
- Export functionality
- Historical data tracking

### **⚙️ Settings Page**
- Application configuration
- Theme customization
- Performance preferences

## 🔧 Configuration

Purrify uses YAML configuration files located in `config/`. Key settings include:

- **Scanning paths**: Directories to scan for optimization
- **Safety thresholds**: Limits for safe cleaning operations
- **Performance settings**: Optimization parameters
- **GUI preferences**: Theme and animation settings

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🐛 Issues & Support

- **Bug Reports**: Please use the GitHub issue tracker
- **Feature Requests**: We'd love to hear your ideas!
- **Documentation**: Check our comprehensive guides

## 🎉 Why Purrify?

Purrify goes beyond traditional system optimization tools by:

- **✨ Combining Beauty with Function**: Transform mundane system tasks into beautiful experiences
- **🌊 Fluid User Experience**: Smooth animations that feel cleansing and purifying
- **🎨 Emotional Connection**: Design that makes you feel good about optimizing your system
- **🚀 Powerful Performance**: All the functionality you need with none of the complexity

**Experience the power of beauty and performance combined! ✨🐱**

---

*Made with 💖 and inspired by the grace of Aphrodite*

## 🤖 AI Features

### Intelligent Analysis
- **Pattern Recognition**: Learn from user behavior and system patterns
- **Risk Assessment**: AI-powered safety evaluation of cleanup operations
- **Performance Prediction**: Predict optimization impact before execution
- **Adaptive Cleaning**: Adjust cleaning strategies based on system usage

### Machine Learning Models
- **Cache Classification**: Identify different types of cache files
- **Performance Profiling**: Analyze system performance patterns
- **User Behavior Learning**: Adapt to individual user preferences
- **Anomaly Detection**: Identify unusual system behavior

## 📊 Performance Metrics

Purrify tracks and reports various performance metrics:

- **Disk Space Saved**: Total space reclaimed
- **Performance Improvement**: System speed enhancements
- **Cache Hit Rates**: Effectiveness of cache cleaning
- **Optimization Impact**: Measurable performance gains

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_scanners/
python -m pytest tests/test_cleaners/
python -m pytest tests/test_ai/

# Run with coverage
python -m pytest --cov=src tests/
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/purrify/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/purrify/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/purrify/wiki)

---

**Made with ❤️ by the Purrify Team**

*Purrify - Making your system purr with performance! 🐱✨* 