#!/usr/bin/env python3
"""
Quick Optimization Script for Purrify
Runs comprehensive scan and optimization with enhanced features
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from purrify.core.engine import PurrifyEngine
from purrify.core.config import Config

async def main():
    """Run comprehensive optimization."""
    print("🚀 Starting Purrify Quick Optimization...")
    print("=" * 60)
    
    # Initialize engine
    config = Config()
    engine = PurrifyEngine(config)
    
    # Step 1: Quick Scan
    print("🔍 Step 1: Quick System Scan")
    print("-" * 40)
    scan_results = await engine.scan_system(
        quick_mode=True,
        detailed_mode=True,
        include_duplicates=True,
        include_photos=True,
        include_large_files=True
    )
    
    print(f"✅ Scan completed: {scan_results.get('total_files', 0):,} files found")
    print(f"💾 Total size: {scan_results.get('total_size', 0) / (1024**3):.1f} GB")
    
    # Step 2: Optimization
    print("\n⚡ Step 2: System Optimization")
    print("-" * 40)
    opt_results = await engine.optimize_system({
        'startup': True,
        'memory': True,
        'disk': True,
        'windows_11': True,
        'wsl': True,
        'microsoft_store': True
    }, safe_mode=False)
    
    print(f"✅ Optimization completed: {opt_results.optimizations_applied} optimizations applied")
    print(f"📈 Performance improvement: {opt_results.performance_improvement:.1f}%")
    
    # Step 3: Display Results
    print("\n" + "=" * 60)
    print("📊 OPTIMIZATION SUMMARY")
    print("=" * 60)
    
    # Display scan results
    if "duplicates" in scan_results:
        duplicates = scan_results["duplicates"]
        print(f"🔄 Duplicate files: {duplicates['groups']} groups")
        print(f"💾 Potential savings: {duplicates['potential_savings'] / (1024**3):.1f} GB")
    
    if "photos" in scan_results:
        photos = scan_results["photos"]
        print(f"📸 Photos analyzed: {photos['count']}")
        print(f"💾 Compression potential: {photos['potential_savings'] / (1024**2):.1f} MB")
    
    if "large_files" in scan_results:
        large_files = scan_results["large_files"]
        print(f"📦 Large files: {large_files['count']}")
        print(f"💾 Total size: {large_files['total_size'] / (1024**3):.1f} GB")
    
    # Display optimization results
    print(f"\n🔧 Optimizations applied: {opt_results.optimizations_applied}")
    print(f"📈 Performance improvement: {opt_results.performance_improvement:.1f}%")
    print(f"⏱️  Duration: {opt_results.optimization_duration:.2f}s")
    
    if opt_results.optimization_errors:
        print(f"\n⚠️  Errors: {len(opt_results.optimization_errors)}")
        for error in opt_results.optimization_errors[:3]:
            print(f"   - {error}")
    
    print("\n🎉 Optimization completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 