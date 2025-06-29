"""
Purrify CLI Utilities

This module provides utility functions for the command-line interface
including banners, system information display, and formatted output.
"""

import os
import sys
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.markdown import Markdown
from loguru import logger

from .platform import detect_platform, format_bytes, get_system_info


def print_banner():
    """Print the Purrify application banner."""
    banner_text = """
🐱  Purrify - AI-Driven System Optimization Utility  🐱

    Making your system purr with performance!
    
    Version: 1.0.0 | MIT License | Cross-Platform
    """
    
    console = Console()
    console.print(Panel(
        banner_text,
        title="[bold blue]Welcome to Purrify[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))


def print_system_info(platform_info: Dict[str, Any]):
    """Print system information in a formatted table."""
    console = Console()
    
    # Create system info table
    table = Table(title="🖥️ System Information")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    
    # Add platform information
    table.add_row("Platform", platform_info.get("platform_type", "Unknown"))
    table.add_row("System", platform_info.get("system", "Unknown"))
    table.add_row("Release", platform_info.get("release", "Unknown"))
    table.add_row("Architecture", platform_info.get("architecture", "Unknown"))
    
    # Add platform-specific info
    if platform_info.get("system") == "darwin":
        table.add_row("macOS Version", platform_info.get("macos_version", "Unknown"))
        table.add_row("Build Version", platform_info.get("macos_build", "Unknown"))
        table.add_row("Apple Silicon", "✅" if platform_info.get("is_apple_silicon") else "❌")
    elif platform_info.get("system") == "windows":
        table.add_row("Windows Version", platform_info.get("windows_version", "Unknown"))
        table.add_row("Build Number", platform_info.get("windows_build", "Unknown"))
    
    # Add Python information
    table.add_row("Python Version", platform_info.get("python_version", "Unknown").split()[0])
    table.add_row("Python Implementation", platform_info.get("python_implementation", "Unknown"))
    
    # Add support status
    supported = platform_info.get("supported", False)
    table.add_row("Supported Platform", "✅" if supported else "❌")
    
    console.print(table)
    
    # Show warning if platform not supported
    if not supported:
        console.print(Panel(
            "⚠️  This platform is not officially supported. "
            "Some features may not work correctly.",
            title="[bold yellow]Warning[/bold yellow]",
            border_style="yellow"
        ))


def print_detailed_system_info():
    """Print detailed system information including disk and memory usage."""
    console = Console()
    
    try:
        system_info = get_system_info()
        
        # System overview
        overview_table = Table(title="📊 System Overview")
        overview_table.add_column("Metric", style="cyan")
        overview_table.add_column("Value", style="green")
        
        # Disk usage
        disk_info = system_info.get("disk_usage", {})
        if "error" not in disk_info:
            overview_table.add_row("Total Disk Space", format_bytes(disk_info.get("total", 0)))
            overview_table.add_row("Used Disk Space", format_bytes(disk_info.get("used", 0)))
            overview_table.add_row("Free Disk Space", format_bytes(disk_info.get("free", 0)))
            overview_table.add_row("Disk Usage %", f"{disk_info.get('percent_used', 0):.1f}%")
        
        # Memory usage
        memory_info = system_info.get("memory_info", {})
        if "error" not in memory_info:
            overview_table.add_row("Total Memory", format_bytes(memory_info.get("total", 0)))
            overview_table.add_row("Used Memory", format_bytes(memory_info.get("used", 0)))
            overview_table.add_row("Available Memory", format_bytes(memory_info.get("available", 0)))
            overview_table.add_row("Memory Usage %", f"{memory_info.get('percent_used', 0):.1f}%")
        
        # Admin status
        overview_table.add_row("Admin Privileges", "✅" if system_info.get("is_admin") else "❌")
        
        console.print(overview_table)
        
    except Exception as e:
        console.print(f"[red]Error getting system info: {e}[/red]")


def show_progress_bar(description: str, total: int = None):
    """
    Show a progress bar for long-running operations.
    
    Args:
        description: Description of the operation
        total: Total number of items to process (optional)
    
    Returns:
        Progress context manager
    """
    if total:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=Console()
        )
        task = progress.add_task(description, total=total)
    else:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=Console()
        )
        task = progress.add_task(description)
    
    return progress, task


def confirm_operation(message: str, default: bool = False) -> bool:
    """
    Ask user to confirm an operation.
    
    Args:
        message: Confirmation message
        default: Default answer if user just presses Enter
    
    Returns:
        True if confirmed, False otherwise
    """
    return Confirm.ask(message, default=default)


def prompt_for_input(message: str, default: str = None, password: bool = False) -> str:
    """
    Prompt user for input.
    
    Args:
        message: Input prompt message
        default: Default value
        password: Whether to hide input (for passwords)
    
    Returns:
        User input string
    """
    return Prompt.ask(message, default=default, password=password)


def print_success(message: str):
    """Print a success message."""
    console = Console()
    console.print(f"✅ {message}", style="green")


def print_error(message: str):
    """Print an error message."""
    console = Console()
    console.print(f"❌ {message}", style="red")


def print_warning(message: str):
    """Print a warning message."""
    console = Console()
    console.print(f"⚠️ {message}", style="yellow")


def print_info(message: str):
    """Print an info message."""
    console = Console()
    console.print(f"ℹ️ {message}", style="blue")


def print_help():
    """Print help information."""
    help_text = """
# 🐱 Purrify Help

## Available Commands

### 🔍 `purrify scan`
Scan your system for optimization opportunities.

**Options:**
- `--quick, -q`: Quick scan mode
- `--detailed, -d`: Detailed scan with file analysis
- `--output, -o`: Save results to file

**Examples:**
```bash
purrify scan                    # Standard scan
purrify scan --quick           # Quick scan
purrify scan --detailed        # Detailed scan
purrify scan --output results.json  # Save to file
```

### 🧹 `purrify clean`
Clean system caches and temporary files.

**Options:**
- `--all, -a`: Clean all detected items
- `--caches, -c`: Clean system and application caches
- `--logs, -l`: Clean system and application logs
- `--temp, -t`: Clean temporary files
- `--safe, -s`: Safe mode (preview only)
- `--backup, -b`: Create backup before cleaning

**Examples:**
```bash
purrify clean --all            # Clean everything
purrify clean --caches         # Clean only caches
purrify clean --safe           # Preview what would be cleaned
```

### ⚡ `purrify optimize`
Optimize system performance.

**Options:**
- `--all, -a`: Apply all optimizations
- `--startup, -s`: Optimize startup items
- `--memory, -m`: Optimize memory usage
- `--disk, -d`: Optimize disk performance
- `--safe`: Safe mode (preview only)

**Examples:**
```bash
purrify optimize --all         # Apply all optimizations
purrify optimize --startup     # Optimize startup only
purrify optimize --safe        # Preview optimizations
```

### 📊 `purrify report`
Generate system optimization report.

**Options:**
- `--detailed, -d`: Include detailed information
- `--output, -o`: Save report to file

**Examples:**
```bash
purrify report                 # Standard report
purrify report --detailed      # Detailed report
purrify report --output report.md  # Save to markdown
```

### 🎮 `purrify gui`
Launch the graphical user interface.

### 📈 `purrify status`
Show current system status.

## Global Options

- `--verbose, -v`: Enable verbose logging
- `--config, -c`: Use custom configuration file
- `--help, -h`: Show help information
- `--version`: Show version information

## Examples

```bash
# Quick system cleanup
purrify scan --quick
purrify clean --all --safe
purrify clean --all

# Full system optimization
purrify scan --detailed
purrify optimize --all
purrify report --detailed

# Launch GUI
purrify gui
```

## Configuration

Purrify uses a YAML configuration file. The default location is:
- `./config/purrify.yaml`
- `./purrify.yaml`
- `./config.yaml`

You can specify a custom config file with `--config`.

## Safety Features

- **Safe Mode**: Use `--safe` to preview changes before applying
- **Backup System**: Automatic backup of critical files
- **AI Safety Checks**: Machine learning-based safety validation
- **Whitelist Protection**: Protect important files and directories

## Support

For more information, visit:
- GitHub: https://github.com/your-username/purrify
- Issues: https://github.com/your-username/purrify/issues
- Documentation: https://github.com/your-username/purrify/wiki
"""
    
    console = Console()
    md = Markdown(help_text)
    console.print(md)


def print_version():
    """Print version information."""
    version_info = """
# 🐱 Purrify Version Information

**Version:** 1.0.0
**License:** MIT
**Author:** Purrify Team
**Email:** team@purrify.app

## Features

- 🔍 **Smart System Scanning**: AI-powered system analysis
- 🧹 **Intelligent Cleaning**: Safe cache and file cleaning
- ⚡ **Performance Optimization**: System speed improvements
- 🤖 **AI-Driven**: Machine learning for optimal results
- 🔒 **Safety First**: Multiple safety mechanisms
- 🎯 **Cross-Platform**: macOS and Windows support

## Technology Stack

- **Backend:** Python 3.8+ with asyncio
- **AI/ML:** TensorFlow/PyTorch for intelligent analysis
- **GUI:** Electron.js with React (optional)
- **Database:** SQLite for local data storage
- **Cross-Platform:** PyInstaller for packaging

## System Requirements

- **macOS:** 10.15 (Catalina) or later
- **Windows:** Windows 10 or later
- **Python:** 3.8 or later
- **Memory:** 4GB RAM minimum
- **Storage:** 100MB free space

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Made with ❤️ by the Purrify Team
"""
    
    console = Console()
    md = Markdown(version_info)
    console.print(md)


def print_config_info(config_path: str):
    """Print configuration file information."""
    console = Console()
    
    config_text = f"""
# ⚙️ Configuration Information

**Config File:** `{config_path}`

## Configuration Sections

### General Settings
- Safe mode operation
- Automatic backup settings
- Logging configuration
- AI/ML feature toggles

### Scanning Settings
- System cache inclusion
- User cache inclusion
- Application cache inclusion
- Exclusion patterns
- Scan depth and timeout

### Cleaning Settings
- Browser cache cleaning
- System log cleaning
- Temporary file cleaning
- File age requirements
- Confirmation settings

### Optimization Settings
- Startup optimization
- Memory optimization
- Disk optimization
- Platform-specific optimizations

### AI Settings
- Machine learning analysis
- Model configuration
- Confidence thresholds
- Learning capabilities

### Security Settings
- Whitelist paths
- Blacklist paths
- Confirmation requirements
- File signature validation

## Editing Configuration

You can edit the configuration file manually or use the GUI settings panel.
The configuration is automatically validated on startup.

## Platform-Specific Settings

Purrify automatically applies platform-specific settings based on your operating system.
"""
    
    md = Markdown(config_text)
    console.print(md)


def print_operation_summary(operation: str, results: Dict[str, Any]):
    """Print a summary of operation results."""
    console = Console()
    
    # Create summary table
    table = Table(title=f"📋 {operation.title()} Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    # Add results to table
    for key, value in results.items():
        if isinstance(value, (int, float)):
            if "bytes" in key.lower() or "size" in key.lower():
                table.add_row(key.replace("_", " ").title(), format_bytes(value))
            else:
                table.add_row(key.replace("_", " ").title(), f"{value:,}")
        else:
            table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)


def print_file_list(files: list, title: str = "Files"):
    """Print a formatted list of files."""
    console = Console()
    
    if not files:
        console.print(f"No {title.lower()} found.")
        return
    
    table = Table(title=f"📁 {title}")
    table.add_column("File Path", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Modified", style="yellow")
    
    for file_info in files[:100]:  # Limit to first 100 files
        path = file_info.get("path", "")
        size = format_bytes(file_info.get("size", 0))
        modified = file_info.get("modified", "")
        
        table.add_row(path, size, modified)
    
    if len(files) > 100:
        table.add_row(f"... and {len(files) - 100} more files", "", "")
    
    console.print(table) 