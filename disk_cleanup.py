#!/usr/bin/env python3
"""
Enhanced Disk Cleanup Script for Purrify
Runs comprehensive disk cleanup with enhanced features and LilithOS detection
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from purrify.core.engine import PurrifyEngine
from purrify.core.config import Config

async def main():
    """Run comprehensive disk cleanup."""
    print("🧹 Starting Purrify Enhanced Disk Cleanup...")
    print("=" * 60)
    
    # Initialize engine
    config = Config()
    engine = PurrifyEngine(config)
    
    # Step 1: Pre-cleanup scan
    print("🔍 Step 1: Pre-cleanup System Scan")
    print("-" * 40)
    scan_results = await engine.scan_system(
        quick_mode=True,
        detailed_mode=True,
        include_duplicates=True,
        include_photos=True,
        include_large_files=True
    )
    
    print(f"✅ Pre-cleanup scan completed: {scan_results.get('total_files', 0):,} files found")
    print(f"💾 Total size before cleanup: {scan_results.get('total_size', 0) / (1024**3):.1f} GB")
    
    # Step 2: Enhanced Disk Cleanup
    print("\n🧹 Step 2: Enhanced Disk Cleanup")
    print("-" * 40)
    
    # Comprehensive cleaning options
    clean_options = {
        'caches': True,              # All cache files
        'logs': True,                # System log files
        'temp_files': True,          # Temporary files
    }
    
    print("🧹 Cleaning options enabled:")
    for option, enabled in clean_options.items():
        if enabled:
            print(f"   ✅ {option.replace('_', ' ').title()}")
    
    clean_results = await engine.clean_system(
        clean_options=clean_options,
        safe_mode=False  # Allow more aggressive cleaning
    )
    
    print(f"✅ Cleanup completed: {clean_results.files_cleaned:,} files cleaned")
    print(f"💾 Space freed: {clean_results.space_freed / (1024**3):.1f} GB")
    
    # Step 3: Post-cleanup scan
    print("\n🔍 Step 3: Post-cleanup System Scan")
    print("-" * 40)
    post_scan_results = await engine.scan_system(
        quick_mode=True,
        detailed_mode=False,
        include_duplicates=False,
        include_photos=False,
        include_large_files=False
    )
    
    print(f"✅ Post-cleanup scan completed: {post_scan_results.get('total_files', 0):,} files remaining")
    print(f"💾 Total size after cleanup: {post_scan_results.get('total_size', 0) / (1024**3):.1f} GB")
    
    # Step 4: Display Results
    print("\n" + "=" * 60)
    print("📊 DISK CLEANUP SUMMARY")
    print("=" * 60)
    
    # Calculate space savings
    pre_size = scan_results.get('total_size', 0)
    post_size = post_scan_results.get('total_size', 0)
    space_saved = pre_size - post_size
    
    print(f"🗑️  Files cleaned: {clean_results.files_cleaned:,}")
    print(f"💾 Space freed: {clean_results.space_freed / (1024**3):.1f} GB")
    print(f"📉 Size reduction: {space_saved / (1024**3):.1f} GB")
    print(f"⏱️  Cleanup duration: {clean_results.clean_duration:.2f}s")
    
    # Display LilithOS cleanup results
    if "lilithos_cleaned" in clean_results:
        lilithos = clean_results["lilithos_cleaned"]
        print(f"\n🖤 LilithOS cleanup:")
        print(f"   📁 Paths cleaned: {len(lilithos['paths_cleaned'])}")
        print(f"   💾 Space freed: {lilithos['space_freed'] / (1024**3):.1f} GB")
        print(f"   🗑️  Files removed: {lilithos['files_removed']:,}")
        if lilithos['paths_cleaned']:
            print("   📍 Paths cleaned:")
            for path in lilithos['paths_cleaned'][:3]:  # Show first 3 paths
                print(f"      - {path}")
    
    # Display scan comparison
    print(f"\n📊 Scan comparison:")
    print(f"   📁 Files before: {scan_results.get('total_files', 0):,}")
    print(f"   📁 Files after: {post_scan_results.get('total_files', 0):,}")
    print(f"   📁 Files removed: {scan_results.get('total_files', 0) - post_scan_results.get('total_files', 0):,}")
    print(f"   💾 Size before: {pre_size / (1024**3):.1f} GB")
    print(f"   💾 Size after: {post_size / (1024**3):.1f} GB")
    print(f"   💾 Total savings: {space_saved / (1024**3):.1f} GB")
    
    # Display any errors
    if clean_results.clean_errors:
        print(f"\n⚠️  Cleanup errors: {len(clean_results.clean_errors)}")
        for error in clean_results.clean_errors[:3]:  # Show first 3 errors
            print(f"   - {error}")
    
    print("\n🎉 Disk cleanup completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 