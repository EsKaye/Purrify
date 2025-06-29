#!/usr/bin/env python3
"""
Purrify Main Application Entry Point

This module provides the main CLI interface and application entry point
for the Purrify system optimization utility.
"""

import sys
import asyncio
import click
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from purrify.core.engine import PurrifyEngine
from purrify.core.config import Config
from purrify.core.logger import setup_logger
from purrify.utils.platform import detect_platform
from purrify.utils.cli_utils import print_banner, print_system_info


@click.group()
@click.version_option(version="1.0.0", prog_name="Purrify")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to config file")
@click.pass_context
def cli(ctx, verbose: bool, config: Optional[str]):
    """
    🐱 Purrify - AI-Driven System Optimization Utility
    
    Clean caches, optimize files, and improve system performance
    using intelligent AI-powered analysis.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Setup logging
    setup_logger(verbose=verbose)
    
    # Load configuration
    config_path = config or "config/purrify.yaml"
    ctx.obj["config"] = Config(config_path)
    
    # Print banner
    print_banner()
    
    # Detect and display platform info
    platform_info = detect_platform()
    print_system_info(platform_info)


@cli.command()
@click.option("--quick", "-q", is_flag=True, help="Quick scan mode")
@click.option("--detailed", "-d", is_flag=True, help="Detailed scan with file analysis")
@click.option("--duplicates", is_flag=True, help="Scan for duplicate files")
@click.option("--photos", is_flag=True, help="Analyze photos for optimization")
@click.option("--large-files", is_flag=True, help="Identify large files")
@click.option("--output", "-o", type=click.Path(), help="Output scan results to file")
@click.pass_context
def scan(ctx, quick: bool, detailed: bool, duplicates: bool, photos: bool, large_files: bool, output: Optional[str]):
    """
    🔍 Scan system for optimization opportunities
    
    Analyzes your system to identify caches, temporary files, duplicates,
    photos, and optimization opportunities.
    """
    config = ctx.obj["config"]
    engine = PurrifyEngine(config)
    
    click.echo("🔍 Starting enhanced system scan...")
    
    try:
        # Determine scan options
        include_duplicates = duplicates or (not quick and not detailed)
        include_photos = photos or (not quick and not detailed)
        include_large_files = large_files or (not quick and not detailed)
        
        # Run enhanced system scan
        scan_results = asyncio.run(engine.scan_system(
            quick_mode=quick,
            detailed_mode=detailed,
            include_duplicates=include_duplicates,
            include_photos=include_photos,
            include_large_files=include_large_files
        ))
        
        # Display results
        engine.display_scan_results(scan_results, output_file=output)
        
    except Exception as e:
        click.echo(f"❌ Enhanced scan failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--all", "-a", is_flag=True, help="Clean all detected items")
@click.option("--caches", "-c", is_flag=True, help="Clean system and application caches")
@click.option("--logs", "-l", is_flag=True, help="Clean system and application logs")
@click.option("--temp", "-t", is_flag=True, help="Clean temporary files")
@click.option("--safe", "-s", is_flag=True, help="Safe mode - preview only")
@click.option("--backup", "-b", is_flag=True, help="Create backup before cleaning")
@click.pass_context
def clean(ctx, all: bool, caches: bool, logs: bool, temp: bool, safe: bool, backup: bool):
    """
    🧹 Clean system caches and temporary files
    
    Removes unnecessary files to free up disk space and improve performance.
    """
    config = ctx.obj["config"]
    engine = PurrifyEngine(config)
    
    # Determine what to clean
    clean_options = {
        "caches": all or caches,
        "logs": all or logs,
        "temp_files": all or temp,
    }
    
    if not any(clean_options.values()):
        click.echo("❌ Please specify what to clean. Use --help for options.")
        return
    
    click.echo("🧹 Starting system cleaning...")
    
    try:
        # Run cleaning operation
        clean_results = asyncio.run(engine.clean_system(
            clean_options=clean_options,
            safe_mode=safe,
            create_backup=backup
        ))
        
        # Display results
        engine.display_clean_results(clean_results)
        
    except Exception as e:
        click.echo(f"❌ Cleaning failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--startup", "-s", is_flag=True, help="Optimize startup items")
@click.option("--memory", "-m", is_flag=True, help="Optimize memory usage")
@click.option("--disk", "-d", is_flag=True, help="Optimize disk performance")
@click.option("--all", "-a", is_flag=True, help="Apply all optimizations")
@click.option("--safe", is_flag=True, help="Safe mode - preview only")
@click.pass_context
def optimize(ctx, startup: bool, memory: bool, disk: bool, all: bool, safe: bool):
    """
    ⚡ Optimize system performance
    
    Applies various optimizations to improve system speed and efficiency.
    """
    config = ctx.obj["config"]
    engine = PurrifyEngine(config)
    
    # Determine optimization options
    opt_options = {
        "startup": all or startup,
        "memory": all or memory,
        "disk": all or disk,
    }
    
    if not any(opt_options.values()):
        click.echo("❌ Please specify optimization type. Use --help for options.")
        return
    
    click.echo("⚡ Starting system optimization...")
    
    try:
        # Run optimization
        opt_results = asyncio.run(engine.optimize_system(
            optimization_options=opt_options,
            safe_mode=safe
        ))
        
        # Display results
        engine.display_optimization_results(opt_results)
        
    except Exception as e:
        click.echo(f"❌ Optimization failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--detailed", "-d", is_flag=True, help="Detailed report")
@click.option("--output", "-o", type=click.Path(), help="Output report to file")
@click.pass_context
def report(ctx, detailed: bool, output: Optional[str]):
    """
    📊 Generate system optimization report
    
    Creates a comprehensive report of system status and optimization history.
    """
    config = ctx.obj["config"]
    engine = PurrifyEngine(config)
    
    click.echo("📊 Generating system report...")
    
    try:
        # Generate report
        report_data = asyncio.run(engine.generate_report(detailed=detailed))
        
        # Display or save report
        engine.display_report(report_data, output_file=output)
        
    except Exception as e:
        click.echo(f"❌ Report generation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def gui():
    """
    🎮 Launch graphical user interface
    
    Opens the Purrify GUI for easy system optimization.
    """
    try:
        from purrify.gui.main_window import launch_gui
        launch_gui()
    except ImportError:
        click.echo("❌ GUI dependencies not installed. Install with: pip install purrify[gui]")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ GUI launch failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def status():
    """
    📈 Show system status
    
    Displays current system status and optimization metrics.
    """
    config = Config()
    engine = PurrifyEngine(config)
    
    try:
        status_info = asyncio.run(engine.get_system_status())
        engine.display_system_status(status_info)
    except Exception as e:
        click.echo(f"❌ Status check failed: {e}", err=True)
        sys.exit(1)


def main():
    """Main entry point for the Purrify application."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n👋 Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 