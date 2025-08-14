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
            
            # Enhanced: Also check for implementations (e.g., OrderService -> OrderServiceImpl)
            for impl_class in self.implementations.get(service_type, set()):
                if impl_class in self.classes:
                    impl_file = self.classes[impl_class]
                    if impl_file != java_file:
                        impl_label = f"@Autowired: {field_name} → {impl_class}"
                        if impl_label not in self.method_calls[java_file][impl_file]:
                            self.method_calls[java_file][impl_file].append(impl_label)
            
            # NEW: Auto-detect implementation classes by naming convention
            self._auto_detect_service_implementations(java_file, service_type, field_name)
        
        print(f"💉 Autowired dependencies in {java_file.stem}: {len(self.annotation_mappings[java_file])}")
    
    def _auto_detect_service_implementations(self, java_file: Path, service_type: str, field_name: str):
        """Auto-detect service implementations by naming convention"""
        # Common naming patterns for implementations
        impl_patterns = [
            f"{service_type}Impl",
            f"{service_type}Implementation", 
            f"{service_type.replace('Service', '')}ServiceImpl",
            f"{service_type.replace('Repository', '')}RepositoryImpl"
        ]
        
        for impl_name in impl_patterns:
            if impl_name in self.classes:
                impl_file = self.classes[impl_name]
                if impl_file != java_file:
                    # Add dependency from current file to implementation
                    impl_label = f"@Service→Impl: {field_name} → {impl_name}"
                    if impl_label not in self.method_calls[java_file][impl_file]:
                        self.method_calls[java_file][impl_file].append(impl_label)
                    
                    # Also track this as an implementation relationship
                    self.implementations[service_type].add(impl_name)
                    print(f"🔍 Auto-detected implementation: {service_type} → {impl_name}")
                    
                    # NEW: Analyze method calls from service interface to implementation
                    self._analyze_service_to_impl_methods(service_type, impl_name, field_name)
                    break
    
    def _analyze_service_to_impl_methods(self, service_interface: str, impl_class: str, field_name: str):
        """Analyze specific method calls from service interface to implementation"""
        if service_interface not in self.classes or impl_class not in self.classes:
            return
            
        service_file = self.classes[service_interface]
        impl_file = self.classes[impl_class]
        
        try:
            # Read service interface to get method signatures
            with open(service_file, 'r', encoding='utf-8') as f:
                service_content = f.read()
            
            # Read implementation to get method implementations
            with open(impl_file, 'r', encoding='utf-8') as f:
                impl_content = f.read()
            
            # Extract interface method signatures
            interface_methods = self._extract_interface_methods(service_content)
            
            # Extract implementation method details
            impl_methods = self._extract_implementation_methods(impl_content)
            
            # Map interface methods to implementation methods
            for method_name in interface_methods:
                if method_name in impl_methods:
                    method_label = f"service-method: {method_name}()"
                    if method_label not in self.method_calls[service_file][impl_file]:
                        self.method_calls[service_file][impl_file].append(method_label)
                    
                    # NEW: Analyze dependencies within the implementation method
                    self._analyze_implementation_method_dependencies(impl_file, method_name, impl_content)
            
            print(f"🔗 Mapped {len(interface_methods)} interface methods to {impl_class}")
            
        except Exception as e:
            print(f"❌ Error analyzing service-to-impl methods: {e}")
    
    def _extract_interface_methods(self, content: str) -> set:
        """Extract method names from interface content"""
        methods = set()
        
        # Pattern for interface method declarations
        # public ReturnType methodName(params);
        interface_method_pattern = r'(?:public|protected)?\s+(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*;'
        
        matches = re.findall(interface_method_pattern, content)
        for method_name in matches:
            # Filter out constructors and common non-methods
            if (not method_name[0].isupper() and 
                method_name not in ['class', 'interface', 'enum', 'import', 'package']):
                methods.add(method_name)
        
        return methods
    
    def _extract_implementation_methods(self, content: str) -> set:
        """Extract method names from implementation class content"""
        methods = set()
        
        # Pattern for implementation method declarations
        # @Override public ReturnType methodName(params) {
        impl_method_patterns = [
            r'@Override\s+(?:public|protected|private)?\s+(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{',
            r'(?:public|protected|private)\s+(?:\w+\s+)*(\w+)\s*\([^)]*\)\s*\{'
        ]
        
        for pattern in impl_method_patterns:
            matches = re.findall(pattern, content)
            for method_name in matches:
                # Filter out constructors and common non-methods
                if (not method_name[0].isupper() and 
                    method_name not in ['class', 'interface', 'enum', 'import', 'package']):
                    methods.add(method_name)
        
        return methods
    
    def _analyze_implementation_method_dependencies(self, impl_file: Path, method_name: str, content: str):
        """Analyze dependencies within a specific implementation method"""
        try:
            # Extract the specific method content
            method_content = self._extract_method_content(content, method_name)
            if not method_content:
                return
            
            # Analyze method calls within this specific method
            method_call_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            method_calls = re.findall(method_call_pattern, method_content)
            
            # Analyze service/repository calls within the method
            service_call_pattern = r'([a-z][a-zA-Z0-9_]*(?:Service|Repository))\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            service_calls = re.findall(service_call_pattern, method_content)
            
            for obj_name, called_method in method_calls + service_calls:
                # Try to resolve the object type
                obj_type = self._resolve_object_type(impl_file, obj_name)
                if obj_type and obj_type in self.classes:
                    target_file = self.classes[obj_type]
                    if target_file != impl_file:
                        dependency_label = f"in-{method_name}: {obj_name}.{called_method}()"
                        if dependency_label not in self.method_calls[impl_file][target_file]:
                            self.method_calls[impl_file][target_file].append(dependency_label)
                
                # Also handle service variable naming (orderService -> OrderService)
                if obj_name.endswith('Service') or obj_name.endswith('Repository'):
                    service_class = obj_name[0].upper() + obj_name[1:]
                    if service_class in self.classes:
                        target_file = self.classes[service_class]
                        if target_file != impl_file:
                            dependency_label = f"in-{method_name}: {service_class}.{called_method}()"
                            if dependency_label not in self.method_calls[impl_file][target_file]:
                                self.method_calls[impl_file][target_file].append(dependency_label)
            
            print(f"🔍 Analyzed method '{method_name}' in {impl_file.stem}: found {len(method_calls + service_calls)} calls")
            
        except Exception as e:
            print(f"❌ Error analyzing method {method_name}: {e}")
    
    def _extract_method_content(self, content: str, method_name: str) -> str:
        """Extract the content of a specific method"""
        try:
            # Pattern to find method start
            method_start_pattern = rf'(?:@Override\s+)?(?:public|protected|private)\s+[^{{]*{re.escape(method_name)}\s*\([^)]*\)\s*\{{'
            
            match = re.search(method_start_pattern, content)
            if not match:
                return ""
            
            start_pos = match.end() - 1  # Position of opening brace
            
            # Find matching closing brace
            brace_count = 1
            pos = start_pos + 1
            
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            if brace_count == 0:
                return content[start_pos:pos]
            
        except Exception as e:
            print(f"❌ Error extracting method {method_name}: {e}")
        
        return ""
    
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
        
        # NEW: Enhanced service-to-implementation analysis
        self._enhance_service_impl_relationships()
        
        print(f"✅ Cross-reference analysis completed")
        print(f"📋 Interfaces found: {len(self.interfaces)}")
        print(f"🔗 Implementation relationships: {sum(len(impls) for impls in self.implementations.values())}")
    
    def _enhance_service_impl_relationships(self):
        """Enhanced analysis for service-implementation relationships"""
        print("🔍 Enhancing service-implementation analysis...")
        
        # Find all service classes and their potential implementations
        service_classes = {name: path for name, path in self.classes.items() 
                          if name.endswith('Service') and not name.endswith('Impl')}
        
        impl_classes = {name: path for name, path in self.classes.items() 
                       if name.endswith('Impl') or name.endswith('Implementation')}
        
        print(f"🔍 Found {len(service_classes)} service classes and {len(impl_classes)} implementation classes")
        
        # Match services with implementations
        for service_name, service_file in service_classes.items():
            # Look for corresponding implementation
            potential_impls = [
                f"{service_name}Impl",
                f"{service_name}Implementation",
                f"{service_name.replace('Service', '')}ServiceImpl"
            ]
            
            for impl_name in potential_impls:
                if impl_name in impl_classes:
                    impl_file = impl_classes[impl_name]
                    
                    # Add to implementations mapping
                    self.implementations[service_name].add(impl_name)
                    
                    # Add service → implementation relationship
                    service_to_impl = f"service→impl: {impl_name}"
                    if service_to_impl not in self.method_calls[service_file][impl_file]:
                        self.method_calls[service_file][impl_file].append(service_to_impl)
                    
                    print(f"🔗 Enhanced mapping: {service_name} → {impl_name}")
                    
                    # Analyze method mappings between service and implementation
                    self._deep_analyze_service_impl_methods(service_name, impl_name)
                    break
    
    def _deep_analyze_service_impl_methods(self, service_name: str, impl_name: str):
        """Deep analysis of method calls between service interface and implementation"""
        if service_name not in self.classes or impl_name not in self.classes:
            return
            
        service_file = self.classes[service_name]
        impl_file = self.classes[impl_name]
        
        try:
            # Read both files
            with open(service_file, 'r', encoding='utf-8') as f:
                service_content = f.read()
            with open(impl_file, 'r', encoding='utf-8') as f:
                impl_content = f.read()
            
            # Get interface methods
            interface_methods = self._extract_interface_methods(service_content)
            
            # For each interface method, analyze its implementation
            for method_name in interface_methods:
                self._analyze_specific_impl_method(impl_file, method_name, impl_content)
            
            print(f"🔍 Deep analyzed {len(interface_methods)} methods in {impl_name}")
            
        except Exception as e:
            print(f"❌ Error in deep analysis of {service_name}→{impl_name}: {e}")
    
    def _analyze_specific_impl_method(self, impl_file: Path, method_name: str, content: str):
        """Analyze a specific implementation method for dependencies"""
        method_content = self._extract_method_content(content, method_name)
        if not method_content:
            return
        
        # Enhanced patterns for method calls within the implementation
        patterns = [
            # Direct method calls: object.method()
            r'([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            # Repository/Service calls: this.userRepository.findById()
            r'this\.([a-zA-Z_][a-zA-Z0-9_]*(?:Repository|Service))\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            # Static method calls: SomeClass.staticMethod()
            r'([A-Z][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            # Constructor calls: new SomeClass()
            r'new\s+([A-Z][a-zA-Z0-9_]*)\s*\('
        ]
        
        dependencies_found = 0
        
        for pattern in patterns:
            matches = re.findall(pattern, method_content)
            
            for match in matches:
                if len(match) == 2:
                    obj_name, called_method = match
                    
                    # Resolve object type
                    obj_type = self._resolve_object_type(impl_file, obj_name)
                    if not obj_type:
                        # Try to match by naming convention
                        if obj_name.endswith('Service') or obj_name.endswith('Repository'):
                            obj_type = obj_name[0].upper() + obj_name[1:]
                    
                    if obj_type and obj_type in self.classes:
                        target_file = self.classes[obj_type]
                        if target_file != impl_file:
                            dependency_label = f"in-{method_name}: {called_method}()"
                            if dependency_label not in self.method_calls[impl_file][target_file]:
                                self.method_calls[impl_file][target_file].append(dependency_label)
                                dependencies_found += 1
                else:  # Constructor call
                    class_name = match[0] if isinstance(match, tuple) else match
                    if class_name in self.classes:
                        target_file = self.classes[class_name]
                        if target_file != impl_file:
                            dependency_label = f"in-{method_name}: new {class_name}()"
                            if dependency_label not in self.method_calls[impl_file][target_file]:
                                self.method_calls[impl_file][target_file].append(dependency_label)
                                dependencies_found += 1
        
        if dependencies_found > 0:
            print(f"  🔍 Method '{method_name}' → {dependencies_found} dependencies")
    
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
        
        # Service-Implementation analysis summary
        service_impl_count = 0
        for interface_name, implementations in self.implementations.items():
            if interface_name.endswith('Service') or interface_name.endswith('Repository'):
                service_impl_count += len(implementations)
        
        print(f"🔧 Service→Implementation mappings: {service_impl_count}")
        
        # Top interfaces by implementation count
        if self.implementations:
            print(f"\n📊 Most implemented interfaces:")
            sorted_interfaces = sorted(self.implementations.items(), key=lambda x: len(x[1]), reverse=True)
            for i, (interface_name, implementations) in enumerate(sorted_interfaces[:3], 1):
                impl_names = ', '.join(implementations)
                print(f"  {i}. {interface_name}: {len(implementations)} implementations ({impl_names})")
        
        # Service-Implementation specific summary
        services_with_impl = {name: impls for name, impls in self.implementations.items() 
                             if name.endswith('Service') or name.endswith('Repository')}
        
        if services_with_impl:
            print(f"\n🔧 Service→Implementation Details:")
            for service_name, implementations in services_with_impl.items():
                for impl_name in implementations:
                    print(f"  🔗 {service_name} → {impl_name}")
        
        print(f"{'='*50}")
    
    def generate_enhanced_graph(self, output_file: str = "dependencies.dot"):
        """Override để sử dụng enhanced summary"""
        result = super().generate_enhanced_graph(output_file)
        
        # Print enhanced summary after generation
        self.print_enhanced_summary()
        
        return result
    
    def analyze_selected_function_flow(self, function_name: str):
        """
        Phân tích flow của một function cụ thể từ interface/service đến implementation
        Ví dụ: cancelOrder từ OrderService đến OrderServiceImpl và các dependencies
        """
        print(f"🎯 Analyzing flow for function: {function_name}")
        
        # Tìm tất cả classes chứa function này
        classes_with_function = self._find_classes_with_function(function_name)
        
        if not classes_with_function:
            print(f"❌ Function '{function_name}' not found in any class")
            return
        
        print(f"🔍 Found '{function_name}' in {len(classes_with_function)} classes")
        
        # Phân tích từng class
        for class_name, file_path in classes_with_function.items():
            print(f"\n📋 Analyzing {function_name} in {class_name}:")
            
            # Nếu đây là service interface, tìm implementation
            if class_name.endswith('Service') and not class_name.endswith('Impl'):
                impl_classes = self.implementations.get(class_name, set())
                for impl_class in impl_classes:
                    if impl_class in self.classes:
                        impl_file = self.classes[impl_class]
                        print(f"  🔗 Found implementation: {impl_class}")
                        
                        # Phân tích chi tiết function trong implementation
                        self._analyze_function_in_implementation(impl_file, function_name, impl_class)
            
            # Nếu đây là implementation class, phân tích trực tiếp
            elif class_name.endswith('Impl') or class_name.endswith('Implementation'):
                print(f"  🔧 Analyzing implementation directly")
                self._analyze_function_in_implementation(file_path, function_name, class_name)
    
    def _find_classes_with_function(self, function_name: str) -> dict:
        """Tìm tất cả classes chứa function với tên cụ thể"""
        classes_with_function = {}
        
        for class_name, file_path in self.classes.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Pattern để tìm function declaration
                function_patterns = [
                    rf'(?:public|protected|private)\s+[^{{]*\s+{re.escape(function_name)}\s*\([^)]*\)\s*[{{;]',
                    rf'@Override\s+(?:public|protected|private)\s+[^{{]*\s+{re.escape(function_name)}\s*\([^)]*\)\s*\{{',
                    rf'{re.escape(function_name)}\s*\([^)]*\)\s*;'  # Interface method
                ]
                
                for pattern in function_patterns:
                    if re.search(pattern, content):
                        classes_with_function[class_name] = file_path
                        break
                        
            except Exception as e:
                continue
        
        return classes_with_function
    
    def _analyze_function_in_implementation(self, impl_file: Path, function_name: str, class_name: str):
        """Phân tích chi tiết một function trong implementation class"""
        try:
            with open(impl_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract method content
            method_content = self._extract_method_content(content, function_name)
            if not method_content:
                print(f"    ❌ Could not extract method content for {function_name}")
                return
            
            print(f"    ✅ Extracted method content ({len(method_content)} chars)")
            
            # Analyze dependencies within this function
            dependencies = self._analyze_function_dependencies(impl_file, function_name, method_content)
            
            # Add these dependencies to the graph with special labels
            for dep_type, dep_target, dep_method in dependencies:
                if dep_target in self.classes:
                    target_file = self.classes[dep_target]
                    if target_file != impl_file:
                        special_label = f"🎯{function_name}: {dep_method}"
                        if special_label not in self.method_calls[impl_file][target_file]:
                            self.method_calls[impl_file][target_file].append(special_label)
            
            print(f"    📊 Found {len(dependencies)} dependencies in {function_name}")
            
            # Tìm và phân tích các service calls trong function này
            self._analyze_service_calls_in_function(impl_file, function_name, method_content)
            
        except Exception as e:
            print(f"    ❌ Error analyzing {function_name} in {class_name}: {e}")
    
    def _analyze_function_dependencies(self, file_path: Path, function_name: str, method_content: str) -> list:
        """Phân tích dependencies trong một function cụ thể"""
        dependencies = []
        
        # Enhanced patterns for different types of calls
        patterns = [
            (r'([a-zA-Z_][a-zA-Z0-9_]*(?:Service|Repository))\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', 'service_call'),
            (r'([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', 'method_call'),
            (r'new\s+([A-Z][a-zA-Z0-9_]*)\s*\(', 'constructor'),
            (r'([A-Z][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', 'static_call'),
            (r'this\.([a-zA-Z_][a-zA-Z0-9_]*(?:Service|Repository))\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', 'this_service')
        ]
        
        for pattern, dep_type in patterns:
            matches = re.findall(pattern, method_content)
            
            for match in matches:
                if dep_type == 'constructor':
                    # Constructor call: new SomeClass()
                    class_name = match
                    dependencies.append((dep_type, class_name, f"new {class_name}()"))
                    
                elif dep_type == 'this_service':
                    # this.serviceField.method() calls
                    service_field, method = match
                    # Convert field name to class name (userService -> UserService)
                    service_class = service_field[0].upper() + service_field[1:]
                    dependencies.append((dep_type, service_class, f"{service_field}.{method}()"))
                    
                elif len(match) == 2:
                    # Regular method calls
                    obj_name, method = match
                    
                    # Try to resolve object type
                    obj_type = self._resolve_object_type(file_path, obj_name)
                    if obj_type:
                        dependencies.append((dep_type, obj_type, f"{obj_name}.{method}()"))
                    elif obj_name.endswith('Service') or obj_name.endswith('Repository'):
                        # Handle service naming convention
                        service_class = obj_name[0].upper() + obj_name[1:]
                        dependencies.append((dep_type, service_class, f"{obj_name}.{method}()"))
        
        return dependencies
    
    def _analyze_service_calls_in_function(self, impl_file: Path, function_name: str, method_content: str):
        """Phân tích đặc biệt các service calls trong function"""
        # Pattern cho các autowired service calls
        service_patterns = [
            r'this\.([a-zA-Z_][a-zA-Z0-9_]*(?:Service|Repository))\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            r'([a-zA-Z_][a-zA-Z0-9_]*(?:Service|Repository))\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        ]
        
        service_calls_found = []
        
        for pattern in service_patterns:
            matches = re.findall(pattern, method_content)
            for service_field, method_called in matches:
                # Convert service field to class name
                if service_field.startswith('this.'):
                    service_field = service_field[5:]
                
                service_class = service_field[0].upper() + service_field[1:]
                
                # Check if this service has implementation
                if service_class in self.implementations:
                    for impl_class in self.implementations[service_class]:
                        if impl_class in self.classes:
                            impl_file_target = self.classes[impl_class]
                            
                            # Add enhanced dependency label
                            enhanced_label = f"🎯{function_name}→{service_class}: {method_called}()"
                            if enhanced_label not in self.method_calls[impl_file][impl_file_target]:
                                self.method_calls[impl_file][impl_file_target].append(enhanced_label)
                                service_calls_found.append(f"{service_class}.{method_called}()")
                            
                            # Recursively analyze the called method in the service implementation
                            print(f"    🔄 Recursively analyzing {method_called} in {impl_class}")
                            self._analyze_function_in_implementation(impl_file_target, method_called, impl_class)
        
        if service_calls_found:
            print(f"    🔗 Service calls in {function_name}: {', '.join(service_calls_found)}")
    
    def enhance_with_selected_functions(self, selected_functions):
        """
        Enhance analysis with selected functions, automatically analyzing service-to-impl flow
        """
        if not selected_functions:
            return
            
        print(f"🎯 Enhancing analysis with {len(selected_functions)} selected functions")
        
        # Extract function names from selected function IDs
        function_names = set()
        for func_id in selected_functions:
            if func_id.startswith('method_'):
                # Extract method name from method_<method_name>_<source>_<target>
                parts = func_id.split('_', 3)
                if len(parts) >= 2:
                    method_name = parts[1]
                    function_names.add(method_name)
            elif func_id.startswith('html_'):
                # For HTML functions, try to extract or map to Java function names
                # This could be enhanced with mapping logic
                func_name = func_id.replace('html_', '').replace('_', '')
                function_names.add(func_name)
        
        # Analyze flow for each selected function
        for function_name in function_names:
            print(f"\n🔍 Enhanced flow analysis for: {function_name}")
            self.analyze_selected_function_flow(function_name)
        
        print(f"✅ Enhanced analysis completed for {len(function_names)} functions")
    
    def filter_by_selection(self, selected_functions):
        """
        Override parent method to add enhanced function flow analysis
        """
        # Call parent filter method
        super().filter_by_selection(selected_functions)
        
        # Add enhanced function analysis
        self.enhance_with_selected_functions(selected_functions)


if __name__ == "__main__":
    # Test với project hiện tại
    analyzer = SuperEnhancedJavaDependencyAnalyzer("Api_LTDD_CuoiKy-master/src/main/java")
    analyzer.analyze()
    
    # Test function flow analysis
    print("\n" + "="*60)
    print("🎯 TESTING FUNCTION FLOW ANALYSIS")
    print("="*60)
    analyzer.analyze_selected_function_flow("cancelOrder")
    
    analyzer.generate_enhanced_graph("enhanced_dependencies.dot")
