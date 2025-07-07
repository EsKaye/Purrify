#!/usr/bin/env python3
"""
Full System Optimization Script

This script runs a complete system scan, optimization, and cleaning
with special attention to LilithOS references and redundant folders.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from purrify.core.engine import PurrifyEngine
from purrify.core.config import Config
from purrify.utils.cli_utils import print_banner


async def run_full_optimization():
    """Run complete system optimization."""
    
    print_banner()
    print("🚀 Starting Full System Optimization with LilithOS Detection")
    print("=" * 60)
    
    # Initialize engine
    config = Config()
    engine = PurrifyEngine(config)
    
    try:
        # Step 1: Comprehensive System Scan
        print("\n🔍 Step 1: Comprehensive System Scan")
        print("-" * 40)
        scan_start = time.time()
        
        scan_results = await engine.scan_system(
            quick_mode=False,
            detailed_mode=True,
            include_duplicates=True,
            include_photos=True,
            include_large_files=True
        )
        
        scan_duration = time.time() - scan_start
        print(f"✅ Scan completed in {scan_duration:.2f} seconds")
        
        # Display scan results
        engine.display_scan_results(scan_results)
        
        # Generate machine-specific optimization script
        print("\n🛠️  Generating machine-specific optimization script...")
        script_path = await engine.generate_optimization_script(scan_results)
        print(f"📄 Optimization script saved at: {script_path}")
        
        # Step 2: System Optimization
        print("\n⚡ Step 2: System Optimization")
        print("-" * 40)
        opt_start = time.time()
        
        optimization_options = {
            "startup": True,
            "memory": True,
            "disk": True,
            "windows_11": True,
            "wsl": True,
            "microsoft_store": True,
        }
        
        opt_results = await engine.optimize_system(
            optimization_options=optimization_options,
            safe_mode=False
        )
        
        opt_duration = time.time() - opt_start
        print(f"✅ Optimization completed in {opt_duration:.2f} seconds")
        
        # Display optimization results
        engine.display_optimization_results(opt_results)
        
        # Step 3: System Cleaning
        print("\n🧹 Step 3: System Cleaning")
        print("-" * 40)
        clean_start = time.time()
        
        clean_options = {
            "caches": True,
            "logs": True,
            "temp_files": True,
        }
        
        clean_results = await engine.clean_system(
            clean_options=clean_options,
            safe_mode=False,
            create_backup=True
        )
        
        clean_duration = time.time() - clean_start
        print(f"✅ Cleaning completed in {clean_duration:.2f} seconds")
        
        # Display cleaning results
        engine.display_clean_results(clean_results)
        
        # Step 4: Final Report
        print("\n📊 Step 4: Final System Report")
        print("-" * 40)
        
        report_data = await engine.generate_report(detailed=True)
        engine.display_report(report_data)
        
        # Summary
        total_duration = time.time() - scan_start
        print(f"\n🎉 Full optimization completed in {total_duration:.2f} seconds")
        print("=" * 60)
        
        # Calculate total space saved
        total_saved = 0
        if "space_freed" in clean_results:
            total_saved += clean_results["space_freed"]
        if "lilithos_cleaned" in clean_results:
            total_saved += clean_results["lilithos_cleaned"].get("space_freed", 0)
        
        if total_saved > 0:
            from purrify.utils.platform import format_bytes
            print(f"💾 Total space freed: {format_bytes(total_saved)}")
        
        print("\n✨ Your system is now optimized and clean!")
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_full_optimization()) 