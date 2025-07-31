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
        self.html_file = Path(html_file)
        self.metadata_file = Path(metadata_file) if metadata_file else None
        self.analyzer = analyzer
        self.port = 8000
        
    def start_server(self):
        """Start web server"""
        if not self.html_file.exists():
            print(f"❌ HTML file not found: {self.html_file}")
            return
            
        serve_dir = self.html_file.parent
        
        class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.analyzer = kwargs.pop('analyzer', None)
                super().__init__(*args, directory=str(serve_dir), **kwargs)
            
            def log_message(self, format, *args):
                pass
            
            def do_POST(self):
                if self.path.startswith('/api/'):
                    self.handle_api_request()
                else:
                    self.send_error(404)
            
            def handle_api_request(self):
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    response_data = {"success": False, "message": "Unknown command"}
                    
                    if self.analyzer and self.path == '/api/edit':
                        command = data.get('command')
                        node = data.get('node')
                        source = data.get('source')
                        target = data.get('target')
                        color = data.get('color')
                        classes = data.get('classes')
                        methods = data.get('methods')
                        
                        if command == 'hide_node' and node:
                            self.analyzer.hide_node(node)
                            response_data = {"success": True, "message": f"Node {node} hidden"}
                        elif command == 'show_node' and node:
                            self.analyzer.show_node(node)
                            response_data = {"success": True, "message": f"Node {node} shown"}
                        elif command == 'delete_node' and node:
                            self.analyzer.delete_node(node)
                            response_data = {"success": True, "message": f"Node {node} deleted"}
                        elif command == 'add_node' and node:
                            self.analyzer.add_custom_node(node, classes or [], color or "lightblue")
                            response_data = {"success": True, "message": f"Node {node} added"}
                        elif command == 'add_edge' and source and target:
                            success = self.analyzer.add_edge(source, target, methods or [])
                            response_data = {"success": success, 
                                           "message": f"Edge {source}->{target} added" if success else "Failed to add edge"}
                        elif command == 'delete_edge' and source and target:
                            success = self.analyzer.delete_edge(source, target)
                            response_data = {"success": success, 
                                           "message": f"Edge {source}->{target} deleted" if success else "Failed to delete edge"}
                        elif command == 'update_edge_label' and source and target and methods:
                            success = self.analyzer.update_edge_label(source, target, methods)
                            response_data = {"success": success, 
                                           "message": f"Edge {source}->{target} updated" if success else "Failed to update edge"}
                        elif command == 'hide_edge' and source and target:
                            self.analyzer.hide_edge(source, target)
                            response_data = {"success": True, "message": f"Edge {source}->{target} hidden"}
                        elif command == 'show_edge' and source and target:
                            self.analyzer.show_edge(source, target)
                            response_data = {"success": True, "message": f"Edge {source}->{target} shown"}
                        elif command == 'set_color' and node and color:
                            self.analyzer.set_node_color(node, color)
                            response_data = {"success": True, "message": f"Node {node} color set to {color}"}
                        elif command == 'reset_color' and node:
                            self.analyzer.reset_node_color(node)
                            response_data = {"success": True, "message": f"Node {node} color reset"}
                        elif command == 'regenerate':
                            output_file = str(serve_dir / "dependencies.dot")
                            html_file, metadata_file = self.analyzer.generate_enhanced_graph(output_file)
                            response_data = {"success": True, "message": "Graph regenerated", "reload": True}
                            
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                    
                except Exception as e:
                    self.send_error(500, f"Server error: {str(e)}")
        
        while True:
            try:
                def handler_factory(*args, **kwargs):
                    kwargs['analyzer'] = self.analyzer
                    return CustomHTTPRequestHandler(*args, **kwargs)
                
                with socketserver.TCPServer(("", self.port), handler_factory) as httpd:
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