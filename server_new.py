#!/usr/bin/env python3
"""
Module for running a web server to serve the dependency graph UI and handle API requests.
"""

import json
import http.server
import socketserver
import webbrowser
from pathlib import Path


class WebUIServer:
    def __init__(self, html_file: str, metadata_file: str = None, analyzer=None):
        self.html_file = Path(html_file) if html_file else None
        self.metadata_file = Path(metadata_file) if metadata_file else None
        self.analyzer = analyzer
        self.port = 8000
        
    def start_server(self):
        """Start web server for dependency graph"""
        if not self.html_file or not self.html_file.exists():
            print(f"❌ HTML file not found: {self.html_file}")
            return
            
        serve_dir = self.html_file.parent
        self._start_server_with_handlers(serve_dir, 'dependencies.html')
        
    def start_function_selector(self):
        """Start web server for function selection"""
        serve_dir = Path(__file__).parent
        self._start_server_with_handlers(serve_dir, 'function_selector.html')
        
    def _start_server_with_handlers(self, serve_dir, main_file):
        """Start server with proper request handlers"""
        
        class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.analyzer = kwargs.pop('analyzer', None)
                super().__init__(*args, directory=str(serve_dir), **kwargs)
            
            def log_message(self, format, *args):
                pass
            
            def do_GET(self):
                if self.path.startswith('/api/'):
                    self.handle_api_get_request()
                else:
                    super().do_GET()
            
            def do_POST(self):
                if self.path.startswith('/api/'):
                    self.handle_api_post_request()
                else:
                    self.send_error(404)
            
            def handle_api_get_request(self):
                """Handle GET API requests"""
                try:
                    response_data = {"success": False, "message": "Unknown API endpoint"}
                    
                    if self.path == '/api/functions' and self.analyzer:
                        functions = self._get_functions_list()
                        response_data = {
                            "success": True,
                            "functions": functions
                        }
                    
                    self._send_json_response(response_data)
                    
                except Exception as e:
                    self.send_error(500, f"Server error: {str(e)}")
            
            def handle_api_post_request(self):
                """Handle POST API requests"""
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    response_data = {"success": False, "message": "Unknown command"}
                    
                    if self.path == '/api/generate' and self.analyzer:
                        response_data = self._handle_generate_graph(data)
                    elif self.path == '/api/edit' and self.analyzer:
                        response_data = self._handle_edit_graph(data)
                    
                    self._send_json_response(response_data)
                    
                except Exception as e:
                    self.send_error(500, f"Server error: {str(e)}")
            
            def _get_functions_list(self):
                """Get list of all functions for selection"""
                functions = []
                
                # Lấy tất cả classes
                for class_name, file_path in self.analyzer.classes.items():
                    rel_path = str(Path(file_path).relative_to(self.analyzer.source_directory))
                    functions.append({
                        'id': f'class_{class_name}',
                        'name': class_name,
                        'type': 'class',
                        'file': rel_path,
                        'dependencies': len(self.analyzer.imports.get(file_path, set()))
                    })
                
                # Thêm services (classes có tên kết thúc bằng Service) - avoid duplicates
                service_functions = []
                for class_name, file_path in self.analyzer.classes.items():
                    if class_name.endswith('Service'):
                        rel_path = str(Path(file_path).relative_to(self.analyzer.source_directory))
                        # Check if already added as class
                        class_id = f'class_{class_name}'
                        if not any(f['id'] == class_id for f in functions):
                            service_functions.append({
                                'id': f'service_{class_name}',
                                'name': class_name,
                                'type': 'service',
                                'file': rel_path,
                                'dependencies': len(self.analyzer.imports.get(file_path, set()))
                            })
                
                functions.extend(service_functions)
                
                # Thêm methods từ method_calls - limit to avoid too many items
                method_count = 0
                for source_file, targets in self.analyzer.method_calls.items():
                    if method_count >= 50:  # Limit to 50 methods to avoid overwhelming UI
                        break
                    for target_file, methods in targets.items():
                        for method in methods:
                            if method_count >= 50:
                                break
                            source_rel = str(Path(source_file).relative_to(self.analyzer.source_directory))
                            target_rel = str(Path(target_file).relative_to(self.analyzer.source_directory))
                            functions.append({
                                'id': f'method_{method}_{source_rel}_{target_rel}',
                                'name': method,
                                'type': 'method',
                                'file': f'{source_rel} → {target_rel}',
                                'dependencies': 1
                            })
                            method_count += 1
                
                # Remove duplicates
                unique_functions = {}
                for func in functions:
                    if func['id'] not in unique_functions:
                        unique_functions[func['id']] = func
                
                return list(unique_functions.values())
            
            def _handle_generate_graph(self, data):
                """Handle graph generation with selected functions"""
                selected_functions = data.get('selectedFunctions', [])
                
                if not selected_functions:
                    return {"success": False, "message": "Không có function nào được chọn"}
                
                try:
                    # Filter analyzer data dựa trên selection
                    self.analyzer.filter_by_selection(selected_functions)
                    
                    # Tạo graph mới
                    output_file = str(serve_dir / "dependencies.dot")
                    html_file, metadata_file = self.analyzer.generate_enhanced_graph(output_file)
                    
                    if html_file:
                        return {
                            "success": True, 
                            "message": f"Graph đã được tạo với {len(selected_functions)} functions",
                            "html_file": html_file,
                            "metadata_file": metadata_file
                        }
                    else:
                        return {"success": False, "message": "Không thể tạo graph"}
                        
                except Exception as e:
                    return {"success": False, "message": f"Lỗi khi tạo graph: {str(e)}"}
            
            def _handle_edit_graph(self, data):
                """Handle graph editing commands"""
                command = data.get('command')
                node = data.get('node')
                source = data.get('source')
                target = data.get('target')
                color = data.get('color')
                classes = data.get('classes')
                methods = data.get('methods')
                
                if command == 'hide_node' and node:
                    self.analyzer.hide_node(node)
                    return {"success": True, "message": f"Node {node} hidden"}
                elif command == 'show_node' and node:
                    self.analyzer.show_node(node)
                    return {"success": True, "message": f"Node {node} shown"}
                elif command == 'delete_node' and node:
                    self.analyzer.delete_node(node)
                    return {"success": True, "message": f"Node {node} deleted"}
                elif command == 'add_node' and node:
                    self.analyzer.add_custom_node(node, classes or [], color or "lightblue")
                    return {"success": True, "message": f"Node {node} added"}
                elif command == 'add_edge' and source and target:
                    success = self.analyzer.add_edge(source, target, methods or [])
                    return {"success": success, 
                           "message": f"Edge {source}->{target} added" if success else "Failed to add edge"}
                elif command == 'delete_edge' and source and target:
                    success = self.analyzer.delete_edge(source, target)
                    return {"success": success, 
                           "message": f"Edge {source}->{target} deleted" if success else "Failed to delete edge"}
                elif command == 'update_edge_label' and source and target and methods:
                    success = self.analyzer.update_edge_label(source, target, methods)
                    return {"success": success, 
                           "message": f"Edge {source}->{target} updated" if success else "Failed to update edge"}
                elif command == 'hide_edge' and source and target:
                    self.analyzer.hide_edge(source, target)
                    return {"success": True, "message": f"Edge {source}->{target} hidden"}
                elif command == 'show_edge' and source and target:
                    self.analyzer.show_edge(source, target)
                    return {"success": True, "message": f"Edge {source}->{target} shown"}
                elif command == 'set_color' and node and color:
                    self.analyzer.set_node_color(node, color)
                    return {"success": True, "message": f"Node {node} color set to {color}"}
                elif command == 'reset_color' and node:
                    self.analyzer.reset_node_color(node)
                    return {"success": True, "message": f"Node {node} color reset"}
                elif command == 'regenerate':
                    output_file = str(serve_dir / "dependencies.dot")
                    html_file, metadata_file = self.analyzer.generate_enhanced_graph(output_file)
                    return {"success": True, "message": "Graph regenerated", "reload": True}
                
                return {"success": False, "message": "Unknown command"}
            
            def _send_json_response(self, data):
                """Send JSON response"""
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
        
        # Start server loop
        while True:
            try:
                def handler_factory(*args, **kwargs):
                    kwargs['analyzer'] = self.analyzer
                    return CustomHTTPRequestHandler(*args, **kwargs)
                
                with socketserver.TCPServer(("", self.port), handler_factory) as httpd:
                    if main_file == 'function_selector.html':
                        print(f"🌐 Starting function selector at http://localhost:{self.port}")
                        print(f"📂 Serving files from: {serve_dir}")
                        print(f"🎯 Function selector: {main_file}")
                        webbrowser.open(f"http://localhost:{self.port}/{main_file}")
                    else:
                        print(f"🌐 Starting web server at http://localhost:{self.port}")
                        print(f"📂 Serving files from: {serve_dir}")
                        print(f"🌐 HTML file: {self.html_file}")
                        print(f"✏️ Graph editing enabled")
                        webbrowser.open(f"http://localhost:{self.port}/{self.html_file.name}")
                    
                    try:
                        httpd.serve_forever()
                    except KeyboardInterrupt:
                        print(f"\n⏹️ Server stopped")
                        break
            except OSError:
                self.port += 1
                if self.port > 8100:
                    print("Cannot find available port")
                    break
