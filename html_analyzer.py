#!/usr/bin/env python3
"""
Enhanced analyzer với HTML nodes support và advanced dependency detection
"""

from collections import defaultdict
from enhanced_analyzer import SuperEnhancedJavaDependencyAnalyzer
from html_db import HTMLFunctionDatabase

class HTMLAwareAnalyzer(SuperEnhancedJavaDependencyAnalyzer):
    def __init__(self, source_directory: str):
        super().__init__(source_directory)
        # HTML functions integration
        self.selected_html_functions = []
        self.html_to_java_mappings = {}
    
    def filter_by_selection(self, selected_functions):
        """Override to preserve HTML data through filtering"""
        # Extract Java function names from selected functions for detailed analysis
        java_function_names = []
        
        # First, process HTML functions and store them
        selected_html_functions = [func_id for func_id in selected_functions if func_id.startswith('html_')]
        
        if selected_html_functions:
            try:
                # Get HTML function data
                html_function_ids = [int(func_id.replace('html_', '')) for func_id in selected_html_functions]
                html_functions_data = []
                
                for func_id in html_function_ids:
                    func_data = self.html_db.get_function_by_id(f"html_{func_id}")
                    if func_data:
                        html_functions_data.append(func_data)
                        # Extract function name for Java analysis
                        func_name = func_data['name']
                        # Remove parentheses and clean up function name
                        clean_func_name = func_name.replace('()', '').replace('/', '_').split('.')[-1]
                        if clean_func_name not in java_function_names:
                            java_function_names.append(clean_func_name)
                
                # Get controller mappings
                controller_mappings = self.html_db.get_controller_mappings_for_html(selected_html_functions)
                
                # Store HTML data for graph generation
                self.selected_html_functions = html_functions_data
                self.html_to_java_mappings = {}
                
                for func_data in html_functions_data:
                    func_name = func_data['name']
                    html_func_id = f"html_{func_data['function_id']}"
                    
                    if html_func_id in controller_mappings:
                        java_component = controller_mappings[html_func_id]
                        self.html_to_java_mappings[func_name] = java_component
                        
            except Exception as e:
                print(f"❌ Error processing HTML functions in filter: {e}")
        
        # Extract function names from regular Java selections
        for func_id in selected_functions:
            if not func_id.startswith('html_'):
                # Assume func_id is a Java class or method name
                if '.' in func_id:
                    # Extract method name if it's in format ClassName.methodName
                    method_name = func_id.split('.')[-1]
                    if method_name not in java_function_names:
                        java_function_names.append(method_name)
                elif func_id not in java_function_names:
                    java_function_names.append(func_id)
        
        # Set selected functions for detailed implementation analysis
        if java_function_names:
            print(f"🎯 Setting selected functions for implementation analysis: {java_function_names}")
            self.set_selected_functions(java_function_names)
            # Filter method calls to only show selected function calls
            self._filter_method_calls_by_selected_functions(java_function_names)
        
        # Call parent method to handle Java filtering
        super().filter_by_selection(selected_functions)
    
    def _filter_method_calls_by_selected_functions(self, selected_function_names):
        """Filter method calls để chỉ hiển thị calls liên quan đến selected functions"""
        if not selected_function_names:
            return
            
        print(f"🔍 Filtering method calls to show only: {', '.join(selected_function_names)}")
        
        # Create filtered method_calls
        filtered_method_calls = defaultdict(lambda: defaultdict(list))
        
        for source_file, targets in self.method_calls.items():
            for target_file, methods in targets.items():
                filtered_methods = []
                
                for method in methods:
                    # Keep method if it matches any selected function name
                    should_keep = False
                    
                    # Check if method contains selected function name
                    for func_name in selected_function_names:
                        if func_name.lower() in method.lower():
                            should_keep = True
                            break
                    
                    # Keep field declarations and other structural relationships
                    if (method.startswith('field:') or 
                        method.startswith('implements') or 
                        method.startswith('@Autowired') or
                        method.startswith('success') or  # Response methods
                        'dependency' in method.lower()):
                        should_keep = True
                    
                    if should_keep:
                        filtered_methods.append(method)
                
                # Only add if there are methods to keep
                if filtered_methods:
                    filtered_method_calls[source_file][target_file] = filtered_methods
        
        # Replace original method_calls with filtered version
        self.method_calls = filtered_method_calls
        print(f"✅ Filtered method calls: {sum(len(targets) for targets in filtered_method_calls.values())} connections")
        
    def add_html_functions_to_graph(self, selected_html_function_ids):
        """Add HTML functions to graph data"""
        if not self.html_db or not selected_html_function_ids:
            return
            
        try:
            # Get HTML function data
            html_functions_data = []
            for func_id in selected_html_function_ids:
                func_data = self.html_db.get_function_by_id(func_id)
                if func_data:
                    html_functions_data.append(func_data)
            
            # Get mappings
            controller_mappings = self.html_db.get_controller_mappings_for_html(selected_html_function_ids)
            
            # Store for graph generation
            self.selected_html_functions = html_functions_data
            self.html_to_java_mappings = {}
            
            for func_data in html_functions_data:
                func_name = func_data['name']
                html_func_id = f"html_{func_data['function_id']}"
                
                if html_func_id in controller_mappings:
                    java_component = controller_mappings[html_func_id]
                    self.html_to_java_mappings[func_name] = java_component
                    print(f"📱 {func_name} → 🔧 {java_component}")
                    
        except Exception as e:
            print(f"❌ Error adding HTML functions: {e}")
    
    def _generate_dot_content(self):
        """Override để thêm HTML nodes"""
        # Get base DOT content
        content_lines = super()._generate_dot_content().split('\n')
        
        # Find insert position (before closing brace)
        insert_pos = len(content_lines) - 1
        while insert_pos > 0 and content_lines[insert_pos].strip() != '}':
            insert_pos -= 1
        
        # Insert HTML nodes if available
        if hasattr(self, 'selected_html_functions') and self.selected_html_functions:
            html_lines = []
            html_lines.append("")
            html_lines.append("    // HTML Function Nodes")
            
            for html_func in self.selected_html_functions:
                func_name = html_func['name']
                node_name = f"HTML_{func_name.replace(' ', '_').replace('()', '').replace('/', '_')}"
                url = f"javascript:showNodeInfo('{node_name}')"
                html_lines.append(f'    "{node_name}" [label="{func_name}\\n(HTML Function)", URL="{url}", fillcolor="lightgreen", shape="ellipse"];')
                
                # Add edge to Java component
                if hasattr(self, 'html_to_java_mappings') and func_name in self.html_to_java_mappings:
                    java_component = self.html_to_java_mappings[func_name]
                    
                    # Find Java node in existing content
                    java_node = None
                    for line in content_lines:
                        if f'"{java_component}"' in line and '[label=' in line:
                            java_node = java_component
                            break
                    
                    if java_node:
                        url_edge = f"javascript:showEdgeInfo('{node_name}', '{java_node}')"
                        html_lines.append(f'    "{node_name}" -> "{java_node}" [label="calls", URL="{url_edge}", color="green", style="bold"];')
                    else:
                        # Create Java node if not found
                        java_node_name = f"Java_{java_component}"
                        url_java = f"javascript:showNodeInfo('{java_node_name}')"
                        html_lines.append(f'    "{java_node_name}" [label="{java_component}\\n(Java Component)", URL="{url_java}", fillcolor="lightyellow"];')
                        url_edge = f"javascript:showEdgeInfo('{node_name}', '{java_node_name}')"
                        html_lines.append(f'    "{node_name}" -> "{java_node_name}" [label="calls", URL="{url_edge}", color="green", style="bold"];')
            
            # Insert HTML lines before closing brace
            content_lines[insert_pos:insert_pos] = html_lines
        
        return '\n'.join(content_lines)
