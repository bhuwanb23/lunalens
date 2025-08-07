#!/usr/bin/env python3
"""
Test script for large file optimization
"""

import os
import sys
import time
from lunar_main import LunarMainController, estimate_processing_time

def test_optimization():
    """Test the optimization features"""
    
    # Test file size estimation
    print("🧪 Testing File Size Estimation")
    print("=" * 50)
    
    test_sizes = [1, 5, 10, 15, 20]
    for size in test_sizes:
        estimate = estimate_processing_time(size)
        print(f"📏 {size}GB file:")
        print(f"   ⏱️  Estimated time: {estimate['hours']}h {estimate['minutes']:.0f}m")
        print(f"   📊 Total minutes: {estimate['total_minutes']:.1f}")
        print(f"   🔍 Breakdown:")
        for analysis, minutes in estimate['breakdown'].items():
            print(f"      - {analysis}: {minutes:.1f}m")
        print()
    
    # Test progress tracker
    print("🧪 Testing Progress Tracker")
    print("=" * 50)
    
    controller = LunarMainController("test_output")
    
    # Simulate progress
    controller.progress_tracker.start_analysis('test_analysis')
    time.sleep(2)  # Simulate processing
    controller.progress_tracker.complete_analysis('test_analysis')
    
    summary = controller.progress_tracker.get_summary()
    print(f"📊 Progress Summary:")
    print(f"   - Total analyses: {summary['total_analyses']}")
    print(f"   - Completed: {summary['completed_analyses']}")
    print(f"   - Total time: {summary['total_time_minutes']:.1f} minutes")
    print(f"   - Average time: {summary['average_time_per_analysis']:.1f} seconds")
    
    # Test progress saving
    print("\n🧪 Testing Progress Saving")
    print("=" * 50)
    
    progress_data = controller.save_progress_info()
    if progress_data:
        print("✅ Progress data saved successfully")
        print(f"📊 Progress percentage: {progress_data['progress_percentage']:.1f}%")
        print(f"🕐 Timestamp: {progress_data['timestamp']}")
    else:
        print("❌ Failed to save progress data")
    
    print("\n✅ Optimization tests completed!")

if __name__ == "__main__":
    test_optimization() 