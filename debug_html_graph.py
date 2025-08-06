#!/usr/bin/env python3
"""
Debug script để test HTML nodes trong graph
"""

from html_analyzer import HTMLAwareAnalyzer

def test_html_graph_generation():
    """Test việc tạo graph với HTML nodes"""
    
    print("🔍 Testing HTML graph generation...")
    
    # Initialize analyzer
    analyzer = HTMLAwareAnalyzer('java-test-project2')
    analyzer.analyze()
    
    # Simulate HTML function selection
    selected_functions = ['html_1']  # User Login Form
    
    print(f"📋 Before filter_by_selection:")
    print(f"   selected_html_functions: {getattr(analyzer, 'selected_html_functions', 'Not set')}")
    print(f"   html_to_java_mappings: {getattr(analyzer, 'html_to_java_mappings', 'Not set')}")
    
    # Call filter method
    analyzer.filter_by_selection(selected_functions)
    
    print(f"\n📋 After filter_by_selection:")
    print(f"   selected_html_functions: {getattr(analyzer, 'selected_html_functions', 'Not set')}")
    print(f"   html_to_java_mappings: {getattr(analyzer, 'html_to_java_mappings', 'Not set')}")
    
    if hasattr(analyzer, 'selected_html_functions') and analyzer.selected_html_functions:
        print(f"\n✅ HTML functions data stored:")
        for func in analyzer.selected_html_functions:
            print(f"   - {func['name']} (ID: {func['function_id']})")
    
    if hasattr(analyzer, 'html_to_java_mappings') and analyzer.html_to_java_mappings:
        print(f"\n✅ HTML→Java mappings stored:")
        for html_func, java_comp in analyzer.html_to_java_mappings.items():
            print(f"   - {html_func} → {java_comp}")
    
    # Generate graph
    print(f"\n📊 Generating graph...")
    html_file, metadata_file = analyzer.generate_enhanced_graph("test_dependencies.dot")
    
    if html_file:
        print(f"✅ Graph generated: {html_file}")
        
        # Read DOT content để check HTML nodes
        with open("test_dependencies.dot", 'r', encoding='utf-8') as f:
            dot_content = f.read()
        
        if "HTML_" in dot_content:
            print("✅ HTML nodes found in DOT file!")
            # Show HTML nodes
            lines = dot_content.split('\n')
            html_lines = [line for line in lines if 'HTML_' in line]
            for line in html_lines:
                print(f"   {line.strip()}")
        else:
            print("❌ No HTML nodes found in DOT file")
            
    else:
        print("❌ Failed to generate graph")

if __name__ == "__main__":
    test_html_graph_generation()
