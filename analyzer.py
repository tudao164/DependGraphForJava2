#!/usr/bin/env python3
"""
Module for analyzing Java dependencies and generating dependency graphs.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from collections import defaultdict


class EnhancedJavaDependencyAnalyzer:
    def __init__(self, source_directory: str):
        self.source_directory = Path(source_directory)
        self.classes = {}  # class_name -> file_path
        self.file_to_classes = defaultdict(set)  # file_path -> class names
        self.imports = defaultdict(set)  # file -> imported classes
        self.method_calls = defaultdict(lambda: defaultdict(list))  # source_file -> target_file -> method_list
        self.hidden_nodes = set()  # nodes to hide from graph
        self.hidden_edges = set()  # edges to hide from graph (source_file, target_file)
        self.custom_colors = {}  # node -> color mapping
        self.custom_nodes = {}  # custom nodes with their properties
        self.custom_edges = defaultdict(lambda: defaultdict(list))  # custom edges: source -> target -> methods
        
    def analyze(self):
        """Phân tích tất cả file Java"""
        java_files = list(self.source_directory.rglob("*.java"))
        
        for java_file in java_files:
            self._extract_classes(java_file)
            
        for java_file in java_files:
            self._analyze_dependencies(java_file)
            
    def _extract_classes(self, java_file: Path):
        """Trích xuất tên class từ file Java"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return
            
        package_match = re.search(r'package\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s*;', content)
        package_name = package_match.group(1) if package_match else ""
        
        class_pattern = r'(?:public\s+)?(?:class|interface|enum)\s+([A-Z][a-zA-Z0-9_]*)'
        class_matches = re.findall(class_pattern, content)
        
        for class_name in class_matches:
            full_name = f"{package_name}.{class_name}" if package_name else class_name
            self.classes[class_name] = java_file
            self.classes[full_name] = java_file
            self.file_to_classes[java_file].add(class_name)
            
    def _analyze_dependencies(self, java_file: Path):
        """Phân tích dependencies và method calls"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return
            
        cleaned_content = self._clean_content(content)
        
        import_pattern = r'import\s+([a-zA-Z_][a-zA-Z0-9_.*]*)\s*;'
        imports = re.findall(import_pattern, content)
        
        imported_classes = set()
        for imp in imports:
            if not imp.startswith('java.'):
                class_name = imp.split('.')[-1]
                imported_classes.add(class_name)
                self.imports[java_file].add(class_name)
        
        method_call_pattern = r'([A-Z][a-zA-Z0-9_]*|[a-z][a-zA-Z0-9_]*)\.([a-z][a-zA-Z0-9_]*)\s*\('
        method_calls = re.findall(method_call_pattern, cleaned_content)
        
        constructor_pattern = r'new\s+([A-Z][a-zA-Z0-9_]*)\s*\('
        constructors = re.findall(constructor_pattern, cleaned_content)
        
        for caller, method_name in method_calls:
            if caller in self.classes and self.classes[caller] != java_file:
                target_file = self.classes[caller]
                self.method_calls[java_file][target_file].append(method_name)
        
        for class_name in constructors:
            if class_name in self.classes and self.classes[class_name] != java_file:
                target_file = self.classes[class_name]
                self.method_calls[java_file][target_file].append(f"new {class_name}()")
                
    def _clean_content(self, content: str) -> str:
        """Loại bỏ comments và strings"""
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'"[^"]*"', '""', content)
        return content
    
    def delete_node(self, node_name: str):
        """Xóa hoàn toàn một node và các liên kết của nó"""
        if node_name in self.custom_nodes:
            del self.custom_nodes[node_name]
        
        for source_file in list(self.method_calls.keys()):
            source_node = self._get_simple_node_name(source_file)
            if source_node == node_name:
                del self.method_calls[source_file]
                continue
            if node_name in [self._get_simple_node_name(target) for target in self.method_calls[source_file].keys()]:
                del self.method_calls[source_file][list(self.method_calls[source_file].keys())[
                    [self._get_simple_node_name(t) for t in self.method_calls[source_file].keys()].index(node_name)]]
        
        for source_file in list(self.custom_edges.keys()):
            source_node = self._get_simple_node_name(source_file)
            if source_node == node_name:
                del self.custom_edges[source_file]
                continue
            if node_name in [self._get_simple_node_name(target) for target in self.custom_edges[source_file].keys()]:
                del self.custom_edges[source_file][list(self.custom_edges[source_file].keys())[
                    [self._get_simple_node_name(t) for t in self.custom_edges[source_file].keys()].index(node_name)]]
                
        self.hidden_nodes.discard(node_name)
        self.hidden_edges = {(s, t) for s, t in self.hidden_edges if s != node_name and t != node_name}
        self.custom_colors.pop(node_name, None)
    
    def add_custom_node(self, node_name: str, classes: list = None, color: str = "lightblue"):
        """Thêm node tùy ý"""
        if not node_name:
            return False
        self.custom_nodes[node_name] = {
            "classes": classes or [],
            "color": color
        }
        return True
    
    def add_edge(self, source_node: str, target_node: str, methods: list = None):
        """Thêm một đường nối mới - FIXED VERSION"""
        if source_node in self.hidden_nodes or target_node in self.hidden_nodes:
            return False
        
        # Kiểm tra xem node có tồn tại không
        source_exists = source_node in self.custom_nodes or any(
            self._get_simple_node_name(f) == source_node for f in self.file_to_classes.keys())
        target_exists = target_node in self.custom_nodes or any(
            self._get_simple_node_name(f) == target_node for f in self.file_to_classes.keys())
        
        if not (source_exists and target_exists):
            return False
        
        # Tìm source_file và target_file
        # Nếu là custom node, dùng chính tên node đó
        if source_node in self.custom_nodes:
            source_file = source_node
        else:
            source_file = next((f for f in self.file_to_classes.keys() 
                            if self._get_simple_node_name(f) == source_node), None)
            
        if target_node in self.custom_nodes:
            target_file = target_node
        else:
            target_file = next((f for f in self.file_to_classes.keys() 
                            if self._get_simple_node_name(f) == target_node), None)
        
        if not source_file or not target_file:
            return False
        
        # Thêm vào custom_edges thay vì method_calls
        if source_file not in self.custom_edges:
            self.custom_edges[source_file] = defaultdict(list)
        self.custom_edges[source_file][target_file].extend(methods or [])
        return True
    
    def delete_edge(self, source_node: str, target_node: str):
        """Xóa hoàn toàn một đường nối - FIXED VERSION"""
        deleted = False
        
        # Xóa từ method_calls
        for source_file in list(self.method_calls.keys()):
            if self._get_simple_node_name(source_file) == source_node:
                for target_file in list(self.method_calls[source_file].keys()):
                    if self._get_simple_node_name(target_file) == target_node:
                        del self.method_calls[source_file][target_file]
                        deleted = True
                        break
                break
        
        # Xóa từ custom_edges
        for source_file in list(self.custom_edges.keys()):
            source_name = self._get_simple_node_name(source_file) if hasattr(source_file, 'stem') else source_file
            if source_name == source_node:
                for target_file in list(self.custom_edges[source_file].keys()):
                    target_name = self._get_simple_node_name(target_file) if hasattr(target_file, 'stem') else target_file
                    if target_name == target_node:
                        del self.custom_edges[source_file][target_file]
                        # Nếu không còn target nào, xóa luôn source
                        if not self.custom_edges[source_file]:
                            del self.custom_edges[source_file]
                        deleted = True
                        break
                break
        
        # Xóa khỏi hidden_edges
        self.hidden_edges.discard((source_node, target_node))
        return deleted
    
    def update_edge_label(self, source_node: str, target_node: str, new_methods: list):
        """Cập nhật nhãn (method calls) của một đường nối - FIXED VERSION"""
        updated = False
        
        # Cập nhật trong method_calls
        for source_file in self.method_calls.keys():
            if self._get_simple_node_name(source_file) == source_node:
                for target_file in self.method_calls[source_file].keys():
                    if self._get_simple_node_name(target_file) == target_node:
                        self.method_calls[source_file][target_file] = new_methods
                        updated = True
                        break
                break
        
        # Cập nhật trong custom_edges
        for source_file in self.custom_edges.keys():
            source_name = self._get_simple_node_name(source_file) if hasattr(source_file, 'stem') else source_file
            if source_name == source_node:
                for target_file in self.custom_edges[source_file].keys():
                    target_name = self._get_simple_node_name(target_file) if hasattr(target_file, 'stem') else target_file
                    if target_name == target_node:
                        self.custom_edges[source_file][target_file] = new_methods
                        updated = True
                        break
                break
        
        return updated
    
    def hide_node(self, node_name: str):
        """Ẩn một node khỏi graph"""
        self.hidden_nodes.add(node_name)
    
    def show_node(self, node_name: str):
        """Hiển thị lại một node đã ẩn"""
        self.hidden_nodes.discard(node_name)
    
    def hide_edge(self, source_node: str, target_node: str):
        """Ẩn một edge khỏi graph"""
        self.hidden_edges.add((source_node, target_node))
    
    def show_edge(self, source_node: str, target_node: str):
        """Hiển thị lại một edge đã ẩn"""
        self.hidden_edges.discard((source_node, target_node))
    
    def set_node_color(self, node_name: str, color: str):
        """Đặt màu cho một node"""
        self.custom_colors[node_name] = color
        if node_name in self.custom_nodes:
            self.custom_nodes[node_name]["color"] = color
    
    def reset_node_color(self, node_name: str):
        """Reset màu node về mặc định"""
        self.custom_colors.pop(node_name, None)
        if node_name in self.custom_nodes:
            self.custom_nodes[node_name]["color"] = "lightblue"
        
    def generate_enhanced_graph(self, output_file: str = "dependencies.dot"):
        """Tạo Graphviz DOT file và HTML với image map"""
        dot_content = self._generate_dot_content()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(dot_content)
        
        metadata = self._generate_metadata()
        metadata_file = output_file.replace('.dot', '_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        image_file = output_file.replace('.dot', '.png')
        map_file = output_file.replace('.dot', '.map')
        html_file = output_file.replace('.dot', '.html')
        
        success_img = self._generate_image(output_file, image_file)
        success_map = self._generate_image_map(output_file, map_file)
        
        if success_img and success_map:
            self._generate_html_with_map(image_file, map_file, html_file, metadata)
            print(f"✅ Enhanced dependency graph generated:")
            print(f"  📄 DOT file: {output_file}")
            print(f"  🖼️  Image: {image_file}")
            print(f"  🗺️  Image map: {map_file}")
            print(f"  🌐 HTML: {html_file}")
            print(f"  📊 Metadata: {metadata_file}")
            
            return html_file, metadata_file
        else:
            print(f"❌ Error generating image or map files")
            return None, None
            
    def _generate_dot_content(self):
        """Generate DOT content với URL attributes cho image map - FIXED VERSION"""
        content = []
        content.append("digraph JavaDependencies {")
        content.append("    rankdir=LR;")
        content.append('    node [shape=box, style=filled, fillcolor=lightblue, fontname="Arial"];')
        content.append('    edge [fontname="Arial", fontsize=9, color=darkblue];')
        content.append('    graph [fontname="Arial Bold", fontsize=14, label="Java Dependency Graph"];')
        content.append("")
        
        # Tập hợp tất cả các file và node cần hiển thị
        all_files = set()
        
        # Thêm từ method_calls
        for source_file in self.method_calls.keys():
            all_files.add(source_file)
            for target_file in self.method_calls[source_file].keys():
                all_files.add(target_file)
        
        # Thêm từ custom_edges
        for source_file in self.custom_edges.keys():
            all_files.add(source_file)
            for target_file in self.custom_edges[source_file].keys():
                all_files.add(target_file)
        
        # Thêm custom nodes
        for node_name in self.custom_nodes.keys():
            all_files.add(node_name)
        
        # Tạo các node
        processed_files = set()
        for file_item in all_files:
            node_name = self._get_simple_node_name(file_item)
            if node_name in self.hidden_nodes:
                continue
                
            if file_item not in processed_files:
                # Kiểm tra xem có phải custom node không
                if node_name in self.custom_nodes:
                    node_info = self.custom_nodes[node_name]
                    class_names = ', '.join(node_info["classes"]) if node_info["classes"] else "Custom Node"
                    fill_color = node_info.get("color", "lightblue")
                else:
                    # Node thường từ file
                    if file_item in self.file_to_classes:
                        class_names = ', '.join(self.file_to_classes[file_item])
                    else:
                        class_names = "Unknown"
                    fill_color = self.custom_colors.get(node_name, "lightblue")
                
                url = f"javascript:showNodeInfo('{node_name}')"
                content.append(f'    "{node_name}" [label="{node_name}\\n({class_names})", URL="{url}", fillcolor="{fill_color}"];')
                processed_files.add(file_item)
        
        content.append("")
        content.append("    // Dependencies with method calls")
        
        # Các đường nối từ method_calls
        for source_file, targets in self.method_calls.items():
            source_node = self._get_simple_node_name(source_file)
            if source_node in self.hidden_nodes:
                continue
            
            for target_file, methods in targets.items():
                target_node = self._get_simple_node_name(target_file)
                if target_node in self.hidden_nodes or (source_node, target_node) in self.hidden_edges:
                    continue
                
                if methods:
                    unique_methods = sorted(list(set(methods)))
                    method_label = '\\n'.join(unique_methods[:3]) + (f'\\n+ {len(unique_methods)-3} more' if len(unique_methods) > 3 else '')
                    url = f"javascript:showEdgeInfo('{source_node}', '{target_node}')"
                    content.append(f'    "{source_node}" -> "{target_node}" [label="{method_label}", URL="{url}"];')
                else:
                    url = f"javascript:showEdgeInfo('{source_node}', '{target_node}')"
                    content.append(f'    "{source_node}" -> "{target_node}" [label="dependency", URL="{url}"];')
        
        # Các đường nối tùy chỉnh
        for source_file, targets in self.custom_edges.items():
            source_node = self._get_simple_node_name(source_file)
            if source_node in self.hidden_nodes:
                continue
            
            for target_file, methods in targets.items():
                target_node = self._get_simple_node_name(target_file)
                if target_node in self.hidden_nodes or (source_node, target_node) in self.hidden_edges:
                    continue
                
                if methods:
                    unique_methods = sorted(list(set(methods)))
                    method_label = '\\n'.join(unique_methods[:3]) + (f'\\n+ {len(unique_methods)-3} more' if len(unique_methods) > 3 else '')
                    url = f"javascript:showEdgeInfo('{source_node}', '{target_node}')"
                    content.append(f'    "{source_node}" -> "{target_node}" [label="{method_label}", URL="{url}", style=dashed, color=red];')
                else:
                    url = f"javascript:showEdgeInfo('{source_node}', '{target_node}')"
                    content.append(f'    "{source_node}" -> "{target_node}" [label="custom dependency", URL="{url}", style=dashed, color=red];')
        
        content.append("}")
        return '\n'.join(content)
    
    def _generate_image(self, dot_file: str, image_file: str) -> bool:
        """Generate PNG image using Graphviz"""
        try:
            cmd = ['dot', '-Tpng', dot_file, '-o', image_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Graphviz error: {result.stderr}")
                return False
            return True
        except FileNotFoundError:
            print("❌ Graphviz not found. Please install Graphviz: https://graphviz.org/download/")
            return False
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return False
    
    def _generate_image_map(self, dot_file: str, map_file: str) -> bool:
        """Generate HTML image map using Graphviz"""
        try:
            cmd = ['dot', '-Tcmapx', dot_file, '-o', map_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Graphviz map error: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"❌ Error generating image map: {e}")
            return False
    
    def _generate_html_with_map(self, image_file: str, map_file: str, html_file: str, metadata: dict):
        """Generate HTML file with image map"""
        try:
            template_path = Path(__file__).parent / "dependency_template3.html"
            if not template_path.exists():
                print(f"❌ Template file not found: {template_path}")
                print("Please ensure 'dependency_template3.html' is in the same directory as this script.")
                return False
                
            with open(template_path, 'r', encoding='utf-8') as f:
                html_template = f.read()
            
            with open(map_file, 'r', encoding='utf-8') as f:
                map_content = f.read()
            
            map_name_match = re.search(r'<map[^>]+name="([^"]*)"', map_content)
            map_name = map_name_match.group(1) if map_name_match else "dependency_map"
            
            image_filename = Path(image_file).name
            metadata_json = json.dumps(metadata, indent=2, default=str)
            
            html_content = html_template.replace('{IMAGE_FILENAME}', image_filename)
            html_content = html_content.replace('{MAP_NAME}', map_name)
            html_content = html_content.replace('{MAP_CONTENT}', map_content)
            html_content = html_content.replace('{METADATA_JSON}', metadata_json)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
        except Exception as e:
            print(f"❌ Error generating HTML: {e}")
            return False
        
    def _generate_metadata(self):
        """Generate metadata for web UI - FIXED VERSION"""
        metadata = {
            "project_info": {
                "source_directory": str(self.source_directory),
                "total_files": len(set(list(self.method_calls.keys()) + 
                                [f for targets in self.method_calls.values() for f in targets.keys()] + 
                                list(self.custom_edges.keys()) + 
                                [f for targets in self.custom_edges.values() for f in targets.keys()])),
                "total_classes": len(self.classes),
                "analysis_date": str(Path.cwd()),
                "custom_nodes": len(self.custom_nodes),
                "custom_edges": sum(len(targets) for targets in self.custom_edges.values())
            },
            "files": {},
            "statistics": {
                "most_connected_files": [],
                "method_call_summary": {}
            },
            "editing": {
                "hidden_nodes": list(self.hidden_nodes),
                "hidden_edges": [{"source": s, "target": t} for s, t in self.hidden_edges],
                "custom_colors": dict(self.custom_colors),
                "custom_nodes": dict(self.custom_nodes),
                "custom_edges": {}
            }
        }
        
        # Xử lý custom_edges một cách an toàn
        for source_file, targets in self.custom_edges.items():
            source_name = self._get_simple_node_name(source_file)
            metadata["editing"]["custom_edges"][source_name] = {}
            for target_file, methods in targets.items():
                target_name = self._get_simple_node_name(target_file)
                # Đảm bảo methods là list và có thể serialize được
                safe_methods = list(methods) if methods else []
                metadata["editing"]["custom_edges"][source_name][target_name] = safe_methods
        
        # Xử lý files metadata
        all_files = set()
        
        # Thu thập từ method_calls
        for file_path in self.method_calls.keys():
            all_files.add(file_path)
        for targets in self.method_calls.values():
            for file_path in targets.keys():
                all_files.add(file_path)
        
        # Thu thập từ custom_edges
        for file_path in self.custom_edges.keys():
            all_files.add(file_path)
        for targets in self.custom_edges.values():
            for file_path in targets.keys():
                all_files.add(file_path)
        
        # Thu thập từ custom_nodes
        for node_name in self.custom_nodes.keys():
            all_files.add(node_name)
        
        # Tạo metadata cho từng file
        for file_item in all_files:
            file_name = self._get_simple_node_name(file_item)
            
            # Khởi tạo file info
            file_info = {
                "classes": [],
                "outgoing_calls": {},
                "incoming_calls": {},
                "is_custom": False
            }
            
            # Nếu là custom node
            if file_name in self.custom_nodes:
                file_info["classes"] = list(self.custom_nodes[file_name].get("classes", []))
                file_info["is_custom"] = True
            elif file_item in self.file_to_classes:
                file_info["classes"] = list(self.file_to_classes[file_item])
            
            # Xử lý outgoing calls từ method_calls
            if file_item in self.method_calls:
                for target_file, methods in self.method_calls[file_item].items():
                    target_name = self._get_simple_node_name(target_file)
                    file_info["outgoing_calls"][target_name] = list(methods) if methods else []
            
            # Xử lý outgoing calls từ custom_edges
            if file_item in self.custom_edges:
                for target_file, methods in self.custom_edges[file_item].items():
                    target_name = self._get_simple_node_name(target_file)
                    # Nếu đã có trong outgoing_calls từ method_calls, thì extend
                    if target_name in file_info["outgoing_calls"]:
                        existing_methods = file_info["outgoing_calls"][target_name]
                        all_methods = list(set(existing_methods + list(methods)))
                        file_info["outgoing_calls"][target_name] = all_methods
                    else:
                        file_info["outgoing_calls"][target_name] = list(methods) if methods else []
            
            # Xử lý incoming calls từ method_calls
            for source_file, targets in self.method_calls.items():
                if file_item in targets:
                    source_name = self._get_simple_node_name(source_file)
                    methods = targets[file_item]
                    file_info["incoming_calls"][source_name] = list(methods) if methods else []
            
            # Xử lý incoming calls từ custom_edges
            for source_file, targets in self.custom_edges.items():
                if file_item in targets:
                    source_name = self._get_simple_node_name(source_file)
                    methods = targets[file_item]
                    # Nếu đã có trong incoming_calls từ method_calls, thì extend
                    if source_name in file_info["incoming_calls"]:
                        existing_methods = file_info["incoming_calls"][source_name]
                        all_methods = list(set(existing_methods + list(methods)))
                        file_info["incoming_calls"][source_name] = all_methods
                    else:
                        file_info["incoming_calls"][source_name] = list(methods) if methods else []
            
            metadata["files"][file_name] = file_info
        
        return metadata
        
    def _get_simple_node_name(self, java_file) -> str:
        """Lấy tên node đơn giản - FIXED VERSION"""
        if isinstance(java_file, Path):
            return java_file.stem
        elif isinstance(java_file, str):
            # Nếu là string và có thể là path
            if '/' in java_file or '\\' in java_file:
                return Path(java_file).stem
            # Nếu là string đơn giản (tên node), trả về như cũ
            return java_file
        else:
            return str(java_file)
        
    def print_summary(self):
        """In summary"""
        total_files = len(set(list(self.method_calls.keys()) + 
                           [f for targets in self.method_calls.values() for f in targets.keys()] + 
                           list(self.custom_edges.keys()) + 
                           [f for targets in self.custom_edges.values() for f in targets.keys()]))
        total_calls = sum(len(methods) for targets in self.method_calls.values() 
                         for methods in targets.values()) + \
                     sum(len(methods) for targets in self.custom_edges.values() 
                         for methods in targets.values())
        
        print(f"\n{'='*50}")
        print(f"🔍 JAVA DEPENDENCY ANALYSIS SUMMARY")
        print(f"{'='*50}")
        print(f"📁 Source Directory: {self.source_directory}")
        print(f"📄 Total files analyzed: {total_files}")
        print(f"🔗 Total method calls found: {total_calls}")
        print(f"🏗️ Total classes found: {len(self.classes)}")
        print(f"🆕 Custom nodes: {len(self.custom_nodes)}")
        print(f"🔗 Custom edges: {sum(len(targets) for targets in self.custom_edges.values())}")
        
        if self.hidden_nodes or self.hidden_edges or self.custom_nodes or self.custom_edges:
            print(f"\n🎨 Graph Editing:")
            print(f"  Hidden nodes: {len(self.hidden_nodes)}")
            print(f"  Hidden edges: {len(self.hidden_edges)}")
            print(f"  Custom colors: {len(self.custom_colors)}")
            print(f"  Custom nodes: {len(self.custom_nodes)}")
            print(f"  Custom edges: {sum(len(targets) for targets in self.custom_edges.values())}")
        
        file_call_counts = []
        for source_file, targets in self.method_calls.items():
            call_count = sum(len(methods) for methods in targets.values())
            if call_count > 0:
                file_call_counts.append((source_file.stem, call_count))
        
        for source_file, targets in self.custom_edges.items():
            call_count = sum(len(methods) for methods in targets.values())
            if call_count > 0:
                file_call_counts.append((self._get_simple_node_name(source_file), call_count))
        
        file_call_counts.sort(key=lambda x: x[1], reverse=True)
        
        if file_call_counts:
            print(f"\n📊 Files making most method calls:")
            for i, (file_name, count) in enumerate(file_call_counts[:5], 1):
                print(f"  {i}. {file_name}: {count} calls")
        
        print(f"{'='*50}")
    
    def filter_by_selection(self, selected_functions):
        """Filter the analyzer data based on selected functions"""
        
        # Nếu không có gì được chọn, không filter
        if not selected_functions:
            print("⚠️ No functions selected, keeping all data")
            return
            
        print(f"🔍 Processing {len(selected_functions)} selected functions...")
        
        # Parse selected function IDs
        selected_classes = set()
        selected_methods = set()
        selected_services = set()
        
        for func_id in selected_functions:
            if func_id.startswith('class_'):
                class_name = func_id[6:]  # Remove 'class_' prefix
                selected_classes.add(class_name)
            elif func_id.startswith('method_'):
                # Parse method_<method_name>_<source_file>_<target_file>
                parts = func_id.split('_', 3)  # Split max 3 times
                if len(parts) >= 4:
                    method_name = parts[1]
                    source_rel = parts[2]
                    target_rel = parts[3]
                    method_info = f"{method_name}_{source_rel}_{target_rel}"
                    selected_methods.add(method_info)
        
        print(f"📊 Selected: {len(selected_classes)} classes, {len(selected_methods)} methods")
        
        # Nếu chọn quá nhiều (có thể là "select all"), chỉ filter nhẹ
        total_classes = len(self.classes)
        if len(selected_classes) >= total_classes * 0.8:  # Nếu chọn >= 80% classes
            print("🎯 Selected most/all classes, keeping full graph with minimal filtering")
            # Chỉ clear hidden nodes/edges, giữ nguyên data gốc
            self.hidden_nodes.clear()
            self.hidden_edges.clear()
            print(f"✅ Keeping full graph: {len(self.classes)} classes and {len(self.method_calls)} file dependencies")
            return
        
        # Filter classes - keep only selected classes and their dependencies
        filtered_classes = {}
        filtered_file_to_classes = {}
        
        # Thêm tất cả selected classes
        for class_name, file_path in self.classes.items():
            if class_name in selected_classes:
                filtered_classes[class_name] = file_path
                if file_path in self.file_to_classes:
                    filtered_file_to_classes[file_path] = self.file_to_classes[file_path]
        
        # Filter method calls - keep calls involving selected classes
        filtered_method_calls = defaultdict(lambda: defaultdict(list))
        
        for source_file, targets in self.method_calls.items():
            # Check if source file contains selected classes
            source_classes = self.file_to_classes.get(source_file, set())
            source_has_selected = any(cls in selected_classes for cls in source_classes)
            
            # Nếu source không được chọn, nhưng có methods cụ thể được chọn từ source này
            if not source_has_selected and selected_methods:
                source_rel = str(Path(source_file).relative_to(self.source_directory))
                for method_info in selected_methods:
                    if source_rel in method_info:
                        source_has_selected = True
                        break
            
            if source_has_selected:
                for target_file, methods in targets.items():
                    # Check if target file contains selected classes
                    target_classes = self.file_to_classes.get(target_file, set())
                    target_has_selected = any(cls in selected_classes for cls in target_classes)
                    
                    # Hoặc target được tham chiếu trong selected methods
                    if not target_has_selected and selected_methods:
                        target_rel = str(Path(target_file).relative_to(self.source_directory))
                        for method_info in selected_methods:
                            if target_rel in method_info:
                                target_has_selected = True
                                break
                    
                    if target_has_selected:
                        # Nếu có method cụ thể được chọn, filter methods
                        if selected_methods:
                            source_rel = str(Path(source_file).relative_to(self.source_directory))
                            target_rel = str(Path(target_file).relative_to(self.source_directory))
                            
                            filtered_methods = []
                            for method in methods:
                                method_key = f"{method}_{source_rel}_{target_rel}"
                                if method_key in selected_methods:
                                    filtered_methods.append(method)
                            
                            # Nếu không có method cụ thể nào được chọn cho edge này,
                            # nhưng cả source và target classes được chọn, thì giữ tất cả methods
                            if not filtered_methods:
                                source_cls_selected = any(cls in selected_classes for cls in source_classes)
                                target_cls_selected = any(cls in selected_classes for cls in target_classes)
                                if source_cls_selected and target_cls_selected:
                                    filtered_methods = methods
                                
                            if filtered_methods:
                                filtered_method_calls[source_file][target_file] = filtered_methods
                                
                                # Đảm bảo cả source và target classes được add
                                for cls in source_classes:
                                    if cls not in filtered_classes and source_file in self.file_to_classes:
                                        filtered_classes[cls] = source_file
                                        filtered_file_to_classes[source_file] = self.file_to_classes[source_file]
                                        
                                for cls in target_classes:
                                    if cls not in filtered_classes and target_file in self.file_to_classes:
                                        filtered_classes[cls] = target_file
                                        filtered_file_to_classes[target_file] = self.file_to_classes[target_file]
                        else:
                            # No specific method filtering, include all methods for selected classes
                            filtered_method_calls[source_file][target_file] = methods
                            
                            # Add related classes
                            for cls in source_classes:
                                if cls not in filtered_classes:
                                    filtered_classes[cls] = source_file
                                    filtered_file_to_classes[source_file] = self.file_to_classes[source_file]
                                    
                            for cls in target_classes:
                                if cls not in filtered_classes:
                                    filtered_classes[cls] = target_file  
                                    filtered_file_to_classes[target_file] = self.file_to_classes[target_file]
        
        # Update analyzer data
        self.classes = filtered_classes
        self.file_to_classes = filtered_file_to_classes
        self.method_calls = filtered_method_calls
        
        # Clear hidden nodes/edges to show filtered results
        self.hidden_nodes.clear()
        self.hidden_edges.clear()
        
        print(f"✅ Filtered to {len(filtered_classes)} classes and {len(filtered_method_calls)} file dependencies")