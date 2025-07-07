#!/usr/bin/env python3
"""
Test Disk Cleanup Script
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from purrify.core.engine import PurrifyEngine
from purrify.core.config import Config

async def main():
    """Test disk cleanup."""
    print("🧹 Testing Enhanced Disk Cleanup...")
    
    # Initialize engine
    config = Config()
    engine = PurrifyEngine(config)
    
    # Run cleanup
    clean_options = {
        'caches': True,
        'logs': True,
        'temp_files': True
    }
    
    print("🧹 Running cleanup...")
    clean_results = await engine.clean_system(
        clean_options=clean_options,
        safe_mode=False
    )
    
    # Display results
    print("\n📊 CLEANUP RESULTS:")
    print("=" * 40)
    
    if hasattr(clean_results, 'files_cleaned'):
        # CleanResult object
        print(f"🗑️  Files cleaned: {clean_results.files_cleaned:,}")
        print(f"💾 Space freed: {clean_results.space_freed / (1024**3):.1f} GB")
        print(f"⏱️  Duration: {clean_results.clean_duration:.2f}s")
        
        if clean_results.clean_errors:
            print(f"⚠️  Errors: {len(clean_results.clean_errors)}")
            for error in clean_results.clean_errors[:3]:
                print(f"   - {error}")
    else:
        # Dictionary format
        print(f"🗑️  Files cleaned: {clean_results.get('files_cleaned', 0):,}")
        print(f"💾 Space freed: {clean_results.get('space_freed', 0) / (1024**3):.1f} GB")
        print(f"⏱️  Duration: {clean_results.get('clean_duration', 0):.2f}s")
        
        if 'lilithos_cleaned' in clean_results:
            lilithos = clean_results['lilithos_cleaned']
            print(f"\n🖤 LilithOS cleanup:")
            print(f"   📁 Paths cleaned: {len(lilithos['paths_cleaned'])}")
            print(f"   💾 Space freed: {lilithos['space_freed'] / (1024**3):.1f} GB")
            print(f"   🗑️  Files removed: {lilithos['files_removed']:,}")
    
    print("\n✅ Cleanup test completed!")

if __name__ == "__main__":
    asyncio.run(main()) 