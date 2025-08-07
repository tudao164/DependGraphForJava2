#!/usr/bin/env python3
"""
Test script để kiểm tra service call detection
"""

from analyzer import EnhancedJavaDependencyAnalyzer
from pathlib import Path

def test_review_controller():
    print("🔍 Testing ReviewController service call detection...")
    
    # Initialize analyzer
    analyzer = EnhancedJavaDependencyAnalyzer("Api_LTDD_CuoiKy-master/src")
    analyzer.analyze()
    
    # Find ReviewController file
    review_controller_file = None
    for file_path, classes in analyzer.file_to_classes.items():
        if 'ReviewController' in classes:
            review_controller_file = file_path
            break
    
    if not review_controller_file:
        print("❌ ReviewController not found!")
        return
        
    print(f"📁 Found ReviewController: {review_controller_file}")
    
    # Check method calls from ReviewController
    if review_controller_file in analyzer.method_calls:
        print("\n🔗 Method calls from ReviewController:")
        for target_file, methods in analyzer.method_calls[review_controller_file].items():
            target_classes = analyzer.file_to_classes.get(target_file, ["Unknown"])
            print(f"  → {target_classes} ({target_file.name})")
            for method in methods:
                print(f"    📞 {method}()")
    else:
        print("❌ No method calls detected from ReviewController")
    
    # Check if ReviewService exists
    print("\n📋 Available Service classes:")
    for class_name, file_path in analyzer.classes.items():
        if 'Service' in class_name:
            print(f"  ✅ {class_name} → {file_path.name}")

if __name__ == "__main__":
    test_review_controller()
