#!/usr/bin/env python3
"""
Demo script để test Function Selector
"""

import subprocess
import sys
import os

def run_demo():
    print("🎯 DEMO: Java Dependency Graph với Function Selector")
    print("="*60)
    
    # Kiểm tra graphviz
    try:
        subprocess.run(['dot', '-V'], capture_output=True, check=True)
        print("✅ Graphviz đã được cài đặt")
    except:
        print("❌ Vui lòng cài đặt Graphviz trước!")
        return
    
    print("\n📝 Các options có sẵn:")
    print("1. Function Selector (mặc định) - Chọn functions trước khi tạo graph")
    print("2. Direct mode - Tạo graph với tất cả functions ngay")
    print("3. Direct + Web - Tạo graph và mở web interface")
    
    choice = input("\nChọn option (1/2/3): ").strip()
    
    source_dir = "java-test-project2/src"
    
    if choice == "1" or choice == "":
        print(f"\n🚀 Khởi động Function Selector...")
        cmd = ["python", "main.py", source_dir]
        
    elif choice == "2":
        print(f"\n🚀 Tạo graph trực tiếp...")
        cmd = ["python", "main.py", source_dir, "--direct"]
        
    elif choice == "3":
        print(f"\n🚀 Tạo graph trực tiếp + Web interface...")
        cmd = ["python", "main.py", source_dir, "--direct", "--web"]
        
    else:
        print("❌ Lựa chọn không hợp lệ!")
        return
    
    print(f"Command: {' '.join(cmd)}")
    print("\n" + "="*60)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Demo stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if not os.path.exists("java-test-project2/src"):
        print("❌ Test project không tìm thấy!")
        print("Vui lòng chạy script này từ thư mục DependGraphForJava2")
        sys.exit(1)
    
    run_demo()
