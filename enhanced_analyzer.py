#!/usr/bin/env python3
"""
Enhanced Java Dependency Analyzer với improved detection cho:
- Interface-Implementation relationships
- Method calls trong conditions (if, switch)
- Method chaining và nested calls
- Field access patterns
"""

import os
import re
import json
import subprocess
from pathlib import Path
from collections import defaultdict
from analyzer import EnhancedJavaDependencyAnalyzer


class SuperEnhancedJavaDependencyAnalyzer(EnhancedJavaDependencyAnalyzer):
    def __init__(self, source_directory: str):
        super().__init__(source_directory)
        
        # Enhanced data structures
        self.interfaces = {}  # interface_name -> file_path
        self.implementations = defaultdict(set)  # interface_name -> {implementation_classes}
        self.field_types = defaultdict(dict)  # file_path -> {field_name: field_type}
        self.conditional_calls = defaultdict(lambda: defaultdict(list))  # file -> target -> conditional_methods
        self.chained_calls = defaultdict(lambda: defaultdict(list))  # file -> target -> chained_methods
        self.annotation_mappings = defaultdict(set)  # file -> {annotation_based_dependencies}
        
    def analyze(self):
        """Enhanced analysis với nhiều phases"""
        print("🔍 Phase 1: Basic class extraction...")
        super().analyze()
        
        print("🔍 Phase 2: Interface-Implementation detection...")
        self._detect_interfaces_and_implementations()
        
        print("🔍 Phase 3: Enhanced dependency analysis...")
        java_files = list(self.source_directory.rglob("*.java"))
        for java_file in java_files:
            self._enhanced_dependency_analysis(java_file)
            
        print("🔍 Phase 4: Cross-reference analysis...")
        self._cross_reference_analysis()
        
    def _detect_interfaces_and_implementations(self):
        """Detect interface-implementation relationships"""
        java_files = list(self.source_directory.rglob("*.java"))
        
        # First pass: identify interfaces
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
                
            # Find interfaces
            interface_pattern = r'(?:public\s+)?interface\s+([A-Z][a-zA-Z0-9_]*)'
            interfaces = re.findall(interface_pattern, content)
            
            for interface_name in interfaces:
                self.interfaces[interface_name] = java_file
                print(f"📋 Found interface: {interface_name}")
        
        # Second pass: find implementations
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
                
            # Find class implementations
            # Pattern: class SomeClass implements Interface1, Interface2
            impl_pattern = r'class\s+([A-Z][a-zA-Z0-9_]*)\s+(?:extends\s+[A-Z][a-zA-Z0-9_]*\s+)?implements\s+([^{]+)'
            impl_matches = re.findall(impl_pattern, content)
            
            for class_name, interfaces_str in impl_matches:
                # Parse multiple interfaces
                implemented_interfaces = [iface.strip() for iface in interfaces_str.split(',')]
                
                for interface_name in implemented_interfaces:
                    interface_name = interface_name.strip()
                    if interface_name in self.interfaces:
                        self.implementations[interface_name].add(class_name)
                        print(f"🔗 {class_name} implements {interface_name}")
                        
                        # Add implicit dependency
                        interface_file = self.interfaces[interface_name]
                        if java_file != interface_file:
                            self.method_calls[java_file][interface_file].append(f"implements {interface_name}")
    
    def _enhanced_dependency_analysis(self, java_file: Path):
        """Enhanced analysis cho một file Java"""
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return
            
        # Analyze fields and their types
        self._analyze_fields(java_file, content)
        
        # Analyze conditional method calls
        self._analyze_conditional_calls(java_file, content)
        
        # Analyze method chaining
        self._analyze_method_chaining(java_file, content)
        
        # Analyze annotation-based dependencies
        self._analyze_annotation_dependencies(java_file, content)
    
    def _analyze_fields(self, java_file: Path, content: str):
        """Analyze field declarations and their types"""
        # Enhanced pattern for field declarations including nested types
        field_patterns = [
            # Standard field declarations
            r'(?:@\w+\s+)?(?:private|protected|public)?\s+([A-Z][a-zA-Z0-9_]*(?:<[^>]+>)?)\s+([a-z][a-zA-Z0-9_]*)\s*[;=]',
            # Method parameters (for better type resolution)
            r'([A-Z][a-zA-Z0-9_]*)\s+([a-z][a-zA-Z0-9_]*)\s*[,)]',
            # Local variable declarations
            r'([A-Z][a-zA-Z0-9_]*)\s+([a-z][a-zA-Z0-9_]*)\s*=',
        ]
        
        for pattern in field_patterns:
            field_matches = re.findall(pattern, content)
            
            for field_type, field_name in field_matches:
                # Clean up generic types
                clean_type = re.sub(r'<.*?>', '', field_type)
                self.field_types[java_file][field_name] = clean_type
                
                # If field type is a known class, add dependency
                if clean_type in self.classes and self.classes[clean_type] != java_file:
                    target_file = self.classes[clean_type]
                    dependency_label = f"field: {field_name}"
                    if dependency_label not in self.method_calls[java_file][target_file]:
                        self.method_calls[java_file][target_file].append(dependency_label)
        
        # Special handling for nested enum types (Order.OrderStatus)
        nested_enum_pattern = r'([A-Z][a-zA-Z0-9_]*)\.([A-Z][a-zA-Z0-9_]*)\s+'
        nested_matches = re.findall(nested_enum_pattern, content)
        
        for parent_class, nested_class in nested_matches:
            if parent_class in self.classes:
                target_file = self.classes[parent_class]
                if target_file != java_file:
                    nested_access = f"nested-type: {parent_class}.{nested_class}"
                    if nested_access not in self.method_calls[java_file][target_file]:
                        self.method_calls[java_file][target_file].append(nested_access)
                        
        print(f"📝 Fields in {java_file.stem}: {len(self.field_types[java_file])}")
    
    def _analyze_conditional_calls(self, java_file: Path, content: str):
        """Analyze method calls within if statements and switch cases"""
        cleaned_content = self._clean_content(content)
        
        # Enhanced pattern for if conditions with method calls
        # if (order.getStatus() == OrderStatus.SHIPPING)
        # if (order.getStatus() == Order.OrderStatus.DELIVERED ||
        if_patterns = [
            r'if\s*\([^)]*?([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)',
            r'if\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*==',
            r'\|\|\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*==',
            r'&&\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*=='
        ]
        
        for pattern in if_patterns:
            if_matches = re.findall(pattern, cleaned_content)
            
            for obj_name, method_name in if_matches:
                # Try to resolve object type from fields
                obj_type = self._resolve_object_type(java_file, obj_name)
                if obj_type and obj_type in self.classes:
                    target_file = self.classes[obj_type]
                    if target_file != java_file:
                        conditional_method = f"if-condition: {obj_name}.{method_name}()"
                        self.conditional_calls[java_file][target_file].append(conditional_method)
                        
                        # Also add to regular method calls if not already there
                        if conditional_method not in self.method_calls[java_file][target_file]:
                            self.method_calls[java_file][target_file].append(conditional_method)
        
        # Enhanced pattern for enum access in conditions
        # order.getStatus() == Order.OrderStatus.SHIPPING
        enum_access_patterns = [
            r'==\s*([A-Z][a-zA-Z0-9_]*)\.([A-Z][a-zA-Z0-9_]*\.)?([A-Z_][A-Z0-9_]*)',
            r'!=\s*([A-Z][a-zA-Z0-9_]*)\.([A-Z][a-zA-Z0-9_]*\.)?([A-Z_][A-Z0-9_]*)',
            r'case\s+([A-Z][a-zA-Z0-9_]*)\.([A-Z_][A-Z0-9_]*)\s*:'
        ]
        
        for pattern in enum_access_patterns:
            enum_matches = re.findall(pattern, cleaned_content)
            
            for match in enum_matches:
                if len(match) == 3:  # (Class, SubClass, Value) format
                    enum_class, subclass, enum_value = match
                    # Handle nested enum like Order.OrderStatus.SHIPPING
                    if subclass:  # Has subclass
                        enum_class = subclass.rstrip('.')  # Remove trailing dot
                else:
                    enum_class, enum_value = match
                
                if enum_class in self.classes:
                    target_file = self.classes[enum_class]
                    if target_file != java_file:
                        enum_access = f"enum-access: {enum_class}.{enum_value}"
                        self.conditional_calls[java_file][target_file].append(enum_access)
                        
                        if enum_access not in self.method_calls[java_file][target_file]:
                            self.method_calls[java_file][target_file].append(enum_access)
        
        # Pattern for switch statements with enum values
        switch_pattern = r'switch\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)'
        switch_matches = re.findall(switch_pattern, cleaned_content)
        
        for switch_var in switch_matches:
            switch_type = self._resolve_object_type(java_file, switch_var)
            if switch_type and switch_type in self.classes:
                target_file = self.classes[switch_type]
                if target_file != java_file:
                    switch_stmt = f"switch({switch_var})"
                    self.conditional_calls[java_file][target_file].append(switch_stmt)
                    
                    if switch_stmt not in self.method_calls[java_file][target_file]:
                        self.method_calls[java_file][target_file].append(switch_stmt)
        
        print(f"🔀 Conditional calls in {java_file.stem}: {len(self.conditional_calls[java_file])}")
    
    def _analyze_method_chaining(self, java_file: Path, content: str):
        """Analyze method chaining patterns"""
        cleaned_content = self._clean_content(content)
        
        # Pattern for method chaining
        # object.method1().method2().method3()
        # order.getOrderItems().stream().map(this::convertToOrderItemDTO)
        chain_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)(?:\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)){2,}'
        chain_matches = re.findall(chain_pattern, cleaned_content)
        
        for obj_name, first_method in chain_matches:
            obj_type = self._resolve_object_type(java_file, obj_name)
            if obj_type and obj_type in self.classes:
                target_file = self.classes[obj_type]
                if target_file != java_file:
                    chained_method = f"chain: {first_method}()..."
                    self.chained_calls[java_file][target_file].append(chained_method)
                    
                    if chained_method not in self.method_calls[java_file][target_file]:
                        self.method_calls[java_file][target_file].append(chained_method)
        
        # Enhanced pattern for complex chaining with stream operations
        stream_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\.(?:stream|parallelStream)\(\)\.(?:map|filter|collect|forEach)'
        stream_matches = re.findall(stream_pattern, cleaned_content)
        
        for obj_name in stream_matches:
            obj_type = self._resolve_object_type(java_file, obj_name)
            if obj_type and obj_type in self.classes:
                target_file = self.classes[obj_type]
                if target_file != java_file:
                    stream_method = f"stream-ops: {obj_name}"
                    self.chained_calls[java_file][target_file].append(stream_method)
                    
                    if stream_method not in self.method_calls[java_file][target_file]:
                        self.method_calls[java_file][target_file].append(stream_method)
        
        print(f"⛓️ Method chains in {java_file.stem}: {len(self.chained_calls[java_file])}")
    
    def _analyze_annotation_dependencies(self, java_file: Path, content: str):
        """Analyze annotation-based dependencies như @Autowired"""
        # @Autowired dependency injection
        autowired_pattern = r'@Autowired[^;]*?([A-Z][a-zA-Z0-9_]*)\s+([a-z][a-zA-Z0-9_]*)\s*[;=]'
        autowired_matches = re.findall(autowired_pattern, content, re.DOTALL)
        
        for service_type, field_name in autowired_matches:
            self.annotation_mappings[java_file].add(service_type)
            
            # Add dependency if class exists
            if service_type in self.classes:
                target_file = self.classes[service_type]
                if target_file != java_file:
                    injection_label = f"@Autowired: {field_name}"
                    if injection_label not in self.method_calls[java_file][target_file]:
                        self.method_calls[java_file][target_file].append(injection_label)
            
            # Also check for implementations (e.g., OrderService -> OrderServiceImpl)
            for impl_class in self.implementations.get(service_type, set()):
                if impl_class in self.classes:
                    impl_file = self.classes[impl_class]
                    if impl_file != java_file:
                        impl_label = f"@Autowired: {field_name} → {impl_class}"
                        if impl_label not in self.method_calls[java_file][impl_file]:
                            self.method_calls[java_file][impl_file].append(impl_label)
        
        print(f"💉 Autowired dependencies in {java_file.stem}: {len(self.annotation_mappings[java_file])}")
    
    def _resolve_object_type(self, java_file: Path, obj_name: str) -> str:
        """Resolve object type from field declarations hoặc local variables"""
        # Check in field types first
        if java_file in self.field_types and obj_name in self.field_types[java_file]:
            return self.field_types[java_file][obj_name]
        
        # Try to read file content and find local variable declarations
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Pattern for local variable declarations
            # Type variableName = ...
            local_var_pattern = rf'([A-Z][a-zA-Z0-9_]*)\s+{re.escape(obj_name)}\s*='
            local_match = re.search(local_var_pattern, content)
            
            if local_match:
                return local_match.group(1)
        except:
            pass
            
        return None
    
    def _cross_reference_analysis(self):
        """Cross-reference analysis để tìm các mối liên hệ bị thiếu"""
        print("🔗 Performing cross-reference analysis...")
        
        # Link interfaces với implementations trong graph
        for interface_name, implementations in self.implementations.items():
            if interface_name in self.interfaces:
                interface_file = self.interfaces[interface_name]
                
                for impl_class in implementations:
                    if impl_class in self.classes:
                        impl_file = self.classes[impl_class]
                        
                        # Add bidirectional relationship
                        # Interface → Implementation
                        interface_to_impl = f"implemented-by: {impl_class}"
                        if interface_to_impl not in self.method_calls[interface_file][impl_file]:
                            self.method_calls[interface_file][impl_file].append(interface_to_impl)
                        
                        # Implementation → Interface
                        impl_to_interface = f"implements: {interface_name}"
                        if impl_to_interface not in self.method_calls[impl_file][interface_file]:
                            self.method_calls[impl_file][interface_file].append(impl_to_interface)
        
        print(f"✅ Cross-reference analysis completed")
        print(f"📋 Interfaces found: {len(self.interfaces)}")
        print(f"🔗 Implementation relationships: {sum(len(impls) for impls in self.implementations.values())}")
    
    def print_enhanced_summary(self):
        """Enhanced summary với thêm thông tin"""
        super().print_summary()
        
        print(f"\n🚀 ENHANCED ANALYSIS SUMMARY")
        print(f"{'='*50}")
        print(f"📋 Interfaces detected: {len(self.interfaces)}")
        print(f"🔗 Implementation relationships: {sum(len(impls) for impls in self.implementations.values())}")
        print(f"📝 Field dependencies: {sum(len(fields) for fields in self.field_types.values())}")
        print(f"🔀 Conditional method calls: {sum(len(targets) for targets in self.conditional_calls.values())}")
        print(f"⛓️ Method chaining detected: {sum(len(targets) for targets in self.chained_calls.values())}")
        print(f"💉 Annotation-based dependencies: {sum(len(deps) for deps in self.annotation_mappings.values())}")
        
        # Top interfaces by implementation count
        if self.implementations:
            print(f"\n📊 Most implemented interfaces:")
            sorted_interfaces = sorted(self.implementations.items(), key=lambda x: len(x[1]), reverse=True)
            for i, (interface_name, implementations) in enumerate(sorted_interfaces[:3], 1):
                impl_names = ', '.join(implementations)
                print(f"  {i}. {interface_name}: {len(implementations)} implementations ({impl_names})")
        
        print(f"{'='*50}")
    
    def generate_enhanced_graph(self, output_file: str = "dependencies.dot"):
        """Override để sử dụng enhanced summary"""
        result = super().generate_enhanced_graph(output_file)
        
        # Print enhanced summary after generation
        self.print_enhanced_summary()
        
        return result


if __name__ == "__main__":
    # Test với project hiện tại
    analyzer = SuperEnhancedJavaDependencyAnalyzer("Api_LTDD_CuoiKy-master/src/main/java")
    analyzer.analyze()
    analyzer.generate_enhanced_graph("enhanced_dependencies.dot")
