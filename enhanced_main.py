#!/usr/bin/env python3
"""
Enhanced main entry point for testing advanced dependency analysis
"""

import os
import argparse
import subprocess
from html_analyzer import HTMLAwareAnalyzer
from server import WebUIServer


def main():
    parser = argparse.ArgumentParser(description="Enhanced Java Dependency Graph Generator with Advanced Analysis")
    parser.add_argument("source_dir", help="Đường dẫn đến thư mục source Java")
    parser.add_argument("--output", "-o", default="enhanced_dependencies.dot", 
                       help="Tên file output DOT (mặc định: enhanced_dependencies.dot)")
    parser.add_argument("--web", "-w", action="store_true",
                       help="Tự động mở web interface sau khi generate")
    parser.add_argument("--port", "-p", type=int, default=8000,
                       help="Port cho web server (mặc định: 8000)")
    parser.add_argument("--direct", "-d", action="store_true",
                       help="Tạo graph trực tiếp mà không qua màn hình lựa chọn")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source_dir):
        print(f"❌ Lỗi: Thư mục '{args.source_dir}' không tồn tại")
        return
    
    try:
        subprocess.run(['dot', '-V'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Graphviz không được tìm thấy!")
        print("   Vui lòng cài đặt Graphviz:")
        print("   - Ubuntu/Debian: sudo apt-get install graphviz")
        print("   - macOS: brew install graphviz")
        print("   - Windows: Tải từ https://graphviz.org/download/")
        return
        
    print("🚀 Initializing Enhanced Java Dependency Analyzer...")
    analyzer = HTMLAwareAnalyzer(args.source_dir)
    
    print(f"🔍 Đang thực hiện enhanced analysis cho: {args.source_dir}")
    print("This includes:")
    print("  📋 Interface-Implementation detection")
    print("  🔀 Conditional method calls (if/switch)")
    print("  ⛓️ Method chaining analysis")
    print("  💉 Annotation-based dependencies")
    print("  📝 Field type analysis")
    
    analyzer.analyze()
    
    # Nếu user chọn direct mode, tạo graph ngay
    if args.direct:
        html_file, metadata_file = analyzer.generate_enhanced_graph(args.output)
        
        if html_file:
            print(f"\n💡 Enhanced Analysis Results:")
            print(f"  🌐 Interactive HTML: {html_file}")
            print(f"  🖼️ Graph Image: {args.output.replace('.dot', '.png')}")
            print(f"  📊 Metadata: {metadata_file}")
            print(f"  ✏️ Graph Editing: Available in web interface")
            
            if args.web:
                print(f"\n🚀 Launching enhanced web interface...")
                server = WebUIServer(html_file, metadata_file, analyzer)
                server.port = args.port
                server.start_server()
            else:
                print(f"\n🌐 To launch web interface: python {__file__} {args.source_dir} --web")
        else:
            print(f"\n❌ Failed to generate interactive HTML. Check Graphviz installation.")
    else:
        # Mở function selector trước
        print(f"\n🎯 Khởi động enhanced function selector...")
        server = WebUIServer("function_selector.html", None, analyzer)
        server.port = args.port
        server.start_function_selector()


if __name__ == "__main__":
    main()
