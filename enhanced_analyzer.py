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
        self.service_to_impl = {}  # service_name -> impl_file_path
        self.impl_to_service = {}  # impl_name -> service_name
        self.field_types = defaultdict(dict)  # file_path -> {field_name: field_type}
        self.conditional_calls = defaultdict(lambda: defaultdict(list))  # file -> target -> conditional_methods
        self.chained_calls = defaultdict(lambda: defaultdict(list))  # file -> target -> chained_methods
        self.annotation_mappings = defaultdict(set)  # file -> {annotation_based_dependencies}
        
        # Method-specific analysis for selected functions
        self.selected_functions = set()  # Set of selected function names like 'cancelOrder'
        self.method_specific_dependencies = defaultdict(lambda: defaultdict(set))  # impl_file -> method -> {dependencies}
        
    def analyze(self):
        """Enhanced analysis với nhiều phases"""
        print("🔍 Phase 1: Basic class extraction...")
        super().analyze()
        
        print("🔍 Phase 2: Interface-Implementation detection...")
        self._detect_interfaces_and_implementations()
        
        print("🔍 Phase 3: Service-Implementation mapping...")
        self._detect_service_impl_relationships()
        
        print("🔍 Phase 4: Enhanced dependency analysis...")
        java_files = list(self.source_directory.rglob("*.java"))
        for java_file in java_files:
            self._enhanced_dependency_analysis(java_file)
            
        print("🔍 Phase 5: Cross-reference analysis...")
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
    
    def _detect_service_impl_relationships(self):
        """Detect Service interface to Implementation mapping"""
        import re
        
        java_files = list(self.source_directory.rglob("*.java"))
        
        # Find all Service interfaces and their implementations
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
            
            file_name = java_file.stem
            
            # Check if this is a Service interface
            if file_name.endswith('Service') and 'interface' in content:
                service_name = file_name
                # Look for corresponding implementation
                impl_name = f"{service_name}Impl"
                
                # Find implementation file
                for impl_file in java_files:
                    if impl_file.stem == impl_name:
                        self.service_to_impl[service_name] = impl_file
                        self.impl_to_service[impl_name] = service_name
                        print(f"🔗 Service mapping: {service_name} -> {impl_name}")
                        
                        # Add edge from service to implementation in graph
                        if java_file in self.method_calls:
                            self.method_calls[java_file][impl_file].append("implemented_by")
                        else:
                            self.method_calls[java_file] = defaultdict(list)
                            self.method_calls[java_file][impl_file].append("implemented_by")
                        break
            
            # Check if this is an implementation that implements a service
            elif file_name.endswith('ServiceImpl') and 'implements' in content:
                impl_name = file_name
                service_name = file_name.replace('Impl', '')
                
                # Find corresponding service interface
                for service_file in java_files:
                    if service_file.stem == service_name and 'interface' in content:
                        self.service_to_impl[service_name] = java_file
                        self.impl_to_service[impl_name] = service_name
                        print(f"🔗 Service mapping: {service_name} -> {impl_name}")
                        break
    
    def set_selected_functions(self, function_names):
        """Set selected functions for detailed analysis"""
        self.selected_functions = set(function_names)
        print(f"🎯 Selected functions for detailed analysis: {', '.join(function_names)}")
        
        # Perform method-specific analysis for implementations
        self._analyze_selected_methods_in_implementations()
    
    def _analyze_selected_methods_in_implementations(self):
        """Analyze selected methods in implementation classes for detailed dependencies"""
        for service_name, impl_file in self.service_to_impl.items():
            try:
                with open(impl_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
                
            print(f"🔍 Analyzing methods in {impl_file.stem}...")
            
            # Find selected methods in this implementation
            for method_name in self.selected_functions:
                method_dependencies = self._extract_method_dependencies(content, method_name, impl_file)
                if method_dependencies:
                    self.method_specific_dependencies[impl_file][method_name] = method_dependencies
                    print(f"  📝 {method_name}: found {len(method_dependencies)} dependencies")
                    # Debug: print actual dependencies
                    for dep in method_dependencies:
                        print(f"    → {dep}")
    
    def _extract_method_dependencies(self, content, method_name, impl_file):
        """Extract dependencies for a specific method"""
        import re
        
        dependencies = set()
        
        # Find the method definition and extract its body
        method_pattern = rf'(?:@Override\s+)?(?:public|private|protected)?\s+[\w<>\[\],\s]+\s+{method_name}\s*\([^{{]*\)\s*(?:throws[^{{]*)?\s*\{{([^}}]*(?:\{{[^}}]*\}}[^}}]*)*)\}}'
        method_match = re.search(method_pattern, content, re.DOTALL)
        
        if not method_match:
            # Try simpler pattern
            simple_pattern = rf'{method_name}\s*\([^{{]*\)\s*\{{([^}}]*(?:\{{[^}}]*\}}[^}}]*)*)\}}'
            method_match = re.search(simple_pattern, content, re.DOTALL)
        
        if method_match:
            method_body = method_match.group(1)
            
            # Extract different types of dependencies from method body
            processed_calls = set()  # Track processed method calls to avoid duplicates
            
            # 1. Repository/Service calls (prioritize this pattern)
            repo_service_pattern = r'([a-z][a-zA-Z0-9_]*(?:Repository|Service))\.([a-z][a-zA-Z0-9_]*)\s*\('
            repo_service_calls = re.findall(repo_service_pattern, method_body)
            
            for field_name, method_call in repo_service_calls:
                call_signature = f"{field_name}.{method_call}()"
                processed_calls.add(call_signature)
                
                # Resolve field type to class name
                field_type = self._resolve_field_type(impl_file, field_name)
                if field_type:
                    dependencies.add(f"{field_type}#{method_call}")
                else:
                    dependencies.add(f"{field_name}#{method_call}")
            
            # 2. Constructor calls (new SomeClass())
            constructor_pattern = r'new\s+([A-Z][a-zA-Z0-9_]*)\s*\('
            constructors = re.findall(constructor_pattern, method_body)
            for class_name in constructors:
                dependencies.add(f"{class_name}#constructor")
            
            # 3. Static method calls (only for true static calls like Math.max(), Collections.sort())
            static_pattern = r'([A-Z][a-zA-Z0-9_]*)\.([a-zA-Z][a-zA-Z0-9_]*)\s*\('
            static_calls = re.findall(static_pattern, method_body)
            for class_name, method_call in static_calls:
                call_signature = f"{class_name}.{method_call}()"
                # Skip if already processed, skip common Java classes, and skip Repository/Service classes
                if (call_signature not in processed_calls and 
                    class_name not in ['System', 'Math', 'String', 'Objects', 'Collections', 'Arrays'] and
                    not class_name.endswith('Repository') and 
                    not class_name.endswith('Service') and
                    not any(call_signature.lower().startswith(pc.lower()) for pc in processed_calls)):
                    processed_calls.add(call_signature)
                    dependencies.add(f"{class_name}#static_{method_call}")
            
            # 4. Exception throws
            exception_pattern = r'throw\s+new\s+([A-Z][a-zA-Z0-9_]*Exception[a-zA-Z0-9_]*)\s*\('
            exceptions = re.findall(exception_pattern, method_body)
            for exception_name in exceptions:
                dependencies.add(f"{exception_name}#exception")
            
            # 5. Enum access (Order.OrderStatus)
            enum_pattern = r'([A-Z][a-zA-Z0-9_]*)\.([A-Z][a-zA-Z0-9_]*)\s*(?!\()'
            enum_accesses = re.findall(enum_pattern, method_body)
            for class_name, enum_value in enum_accesses:
                if not enum_value.endswith('()'):  # Not a method call
                    dependencies.add(f"{class_name}#enum_{enum_value}")
            
            # 6. Method calls on local variables or fields (skip already processed)
            local_method_pattern = r'([a-z][a-zA-Z0-9_]*)\.([a-z][a-zA-Z0-9_]*)\s*\('
            local_calls = re.findall(local_method_pattern, method_body)
            for var_name, method_call in local_calls:
                call_signature = f"{var_name}.{method_call}()"
                # Skip if already processed by Repository/Service pattern
                if call_signature not in processed_calls:
                    # Try to resolve variable type
                    var_type = self._resolve_local_variable_type(method_body, var_name)
                    if var_type:
                        dependencies.add(f"{var_type}#method_{method_call}")
                    # Skip the fallback for Repository/Service since it's already handled above
        
        return dependencies
    
    def _resolve_field_type(self, java_file, field_name):
        """Resolve field name to its type/class"""
        if java_file in self.field_types and field_name in self.field_types[java_file]:
            return self.field_types[java_file][field_name]
        
        # Try to find in constructor parameters or field declarations
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for field declaration
            field_pattern = rf'(?:private|protected|public)?\s+([A-Z][a-zA-Z0-9_]*(?:<[^>]+>)?)\s+{field_name}\s*[;=]'
            field_match = re.search(field_pattern, content)
            if field_match:
                return field_match.group(1).split('<')[0]  # Remove generics
                
            # Look for constructor parameter
            constructor_pattern = rf'([A-Z][a-zA-Z0-9_]*)\s+{field_name}[,)]'
            constructor_match = re.search(constructor_pattern, content)
            if constructor_match:
                return constructor_match.group(1)
                
        except:
            pass
            
        return None
    
    def _resolve_local_variable_type(self, method_body, var_name):
        """Resolve local variable type within method body"""
        import re
        
        # Look for variable declaration: Type varName = ...
        var_decl_pattern = rf'([A-Z][a-zA-Z0-9_]*)\s+{var_name}\s*='
        match = re.search(var_decl_pattern, method_body)
        if match:
            return match.group(1)
        
        # Look for assignment from method call: var = someObject.getType()
        assignment_pattern = rf'{var_name}\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\.get([A-Z][a-zA-Z0-9_]*)\s*\('
        match = re.search(assignment_pattern, method_body)
        if match:
            return match.group(2)  # Return the type from getter method
        
        return None
    
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
        
        # Service-Implementation mappings
        print(f"🔧 Service-Implementation mappings: {len(self.service_to_impl)}")
        if self.service_to_impl:
            for service_name, impl_file in self.service_to_impl.items():
                print(f"  • {service_name} → {impl_file.stem}")
        
        # Method-specific analysis results
        print(f"🎯 Method-specific analysis: {len(self.method_specific_dependencies)} implementations")
        if self.method_specific_dependencies:
            total_method_deps = sum(
                len(methods) for methods in self.method_specific_dependencies.values()
            )
            total_deps = sum(
                len(deps) for methods in self.method_specific_dependencies.values() 
                for deps in methods.values()
            )
            print(f"  • Total methods analyzed: {total_method_deps}")
            print(f"  • Total dependencies found: {total_deps}")
            
            for impl_file, methods in self.method_specific_dependencies.items():
                print(f"  • {impl_file.stem}:")
                for method_name, deps in methods.items():
                    print(f"    - {method_name}: {len(deps)} dependencies")
        
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
    
    def _generate_dot_content(self):
        """Override để thêm Service Implementation nodes và method-specific dependencies"""
        # Get base DOT content từ parent class
        base_content = super()._generate_dot_content()
        content_lines = base_content.split('\n')
        
        # Find insert position (before closing brace)
        insert_pos = len(content_lines) - 1
        while insert_pos > 0 and content_lines[insert_pos].strip() != '}':
            insert_pos -= 1
        
        # Prepare additional content
        additional_lines = []
        additional_lines.append("")
        additional_lines.append("    // Service Implementation Nodes")
        
        # Add Service Implementation nodes
        for service_name, impl_file in self.service_to_impl.items():
            impl_name = impl_file.stem
            
            # Check if implementation has method-specific dependencies
            has_method_deps = impl_file in self.method_specific_dependencies
            
            if has_method_deps:
                # Create implementation node with special styling
                url = f"javascript:showNodeInfo('{impl_name}')"
                additional_lines.append(f'    "{impl_name}" [label="{impl_name}\\n(Implementation)", URL="{url}", fillcolor="lightcoral", shape="box"];')
                
                # Add edge from service to implementation
                service_url = f"javascript:showEdgeInfo('{service_name}', '{impl_name}')"
                additional_lines.append(f'    "{service_name}" -> "{impl_name}" [label="implements", URL="{service_url}", color="red", style="dashed"];')
                
                # Add method-specific dependency nodes and edges
                for method_name, dependencies in self.method_specific_dependencies[impl_file].items():
                    if dependencies:
                        additional_lines.append("")
                        additional_lines.append(f"    // {method_name} method dependencies in {impl_name}")
                        
                        for dep in dependencies:
                            if '#' in dep:
                                class_name, method_call = dep.split('#', 1)
                                
                                # Create dependency node if it doesn't exist
                                dep_node_name = f"{class_name}"
                                
                                # Check if this dependency node already exists in base content
                                node_exists = any(f'"{dep_node_name}"' in line and '[label=' in line for line in content_lines)
                                
                                if not node_exists:
                                    # Determine node color based on type
                                    if 'Repository' in class_name:
                                        color = "lightyellow"
                                        shape = "box"
                                    elif 'Service' in class_name:
                                        color = "lightblue"
                                        shape = "box"
                                    elif 'Exception' in class_name:
                                        color = "mistyrose"
                                        shape = "box"
                                    elif method_call == 'enum':
                                        color = "lightgreen"
                                        shape = "diamond"
                                    else:
                                        color = "white"
                                        shape = "box"
                                    
                                    dep_url = f"javascript:showNodeInfo('{dep_node_name}')"
                                    additional_lines.append(f'    "{dep_node_name}" [label="{class_name}", URL="{dep_url}", fillcolor="{color}", shape="{shape}"];')
                                
                                # Add edge from implementation to dependency
                                edge_label = method_call if method_call != 'constructor' else 'new'
                                if method_call == 'exception':
                                    edge_style = ', color="red"'
                                elif 'Repository' in class_name:
                                    edge_style = ', color="orange"'
                                elif 'Service' in class_name:
                                    edge_style = ', color="blue"'
                                else:
                                    edge_style = ''
                                
                                dep_edge_url = f"javascript:showEdgeInfo('{impl_name}', '{dep_node_name}')"
                                additional_lines.append(f'    "{impl_name}" -> "{dep_node_name}" [label="{edge_label} ({method_name})", URL="{dep_edge_url}"{edge_style}];')
        
        # Insert additional content before closing brace
        if additional_lines:
            content_lines[insert_pos:insert_pos] = additional_lines
        
        return '\n'.join(content_lines)


if __name__ == "__main__":
    # Test với project hiện tại
    analyzer = SuperEnhancedJavaDependencyAnalyzer("Api_LTDD_CuoiKy-master/src/main/java")
    analyzer.analyze()
    analyzer.generate_enhanced_graph("enhanced_dependencies.dot")
