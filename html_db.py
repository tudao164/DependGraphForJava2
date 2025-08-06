#!/usr/bin/env python3
"""
Database connector để lấy HTML/JS functions từ PostgreSQL database
"""

import json
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
from typing import List, Dict, Any
import os

# Import config từ file riêng
try:
    from db_config import DB_CONFIG
except ImportError:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'graph'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'schema': os.getenv('DB_SCHEMA', 'public')
    }

class HTMLFunctionDatabase:
    def __init__(self, db_config: Dict[str, str] = None):
        if db_config is None:
            self.db_config = DB_CONFIG
        else:
            self.db_config = db_config
        
        self.test_connection()
    
    def test_connection(self):
        """Test PostgreSQL connection"""
        try:
            conn = psycopg2.connect(**{k: v for k, v in self.db_config.items() if k != 'schema'})
            conn.close()
            print(f"✅ Connected to PostgreSQL database: {self.db_config['database']}")
        except Exception as e:
            print(f"❌ Failed to connect to PostgreSQL: {e}")
            print(f"   Config: {self.db_config}")
            print(f"   💡 Kiểm tra db_config.py hoặc environment variables")
            raise
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**{k: v for k, v in self.db_config.items() if k != 'schema'})
    
    def get_all_functions(self) -> List[Dict[str, Any]]:
        """Lấy tất cả HTML/JS functions từ PostgreSQL database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            schema = self.db_config['schema']
            cursor.execute(f'''
                SELECT function_id, function_name
                FROM {schema}.html_function
                ORDER BY function_name
            ''')
            
            functions = []
            for row in cursor.fetchall():
                functions.append({
                    'id': f'html_{row["function_id"]}',  # Prefix để phân biệt với Java functions
                    'function_id': row['function_id'],
                    'name': row['function_name'],
                    'file': f'Frontend/{row["function_name"]}',  # Giả định đường dẫn
                    'type': 'html',
                    'description': f'HTML/JS function: {row["function_name"]}',
                    'dependencies': 1  # Sẽ có dependency đến Java controller
                })
            
            conn.close()
            print(f"✅ Loaded {len(functions)} HTML functions from database")
            return functions
            
        except Exception as e:
            print(f"❌ Error loading HTML functions: {e}")
            return []
    
    def get_functions_by_ids(self, function_ids: List[str]) -> List[Dict[str, Any]]:
        """Lấy functions theo danh sách IDs"""
        if not function_ids:
            return []
            
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Remove 'html_' prefix nếu có
            clean_ids = [fid.replace('html_', '') for fid in function_ids if 'html_' in fid]
            if not clean_ids:
                return []
            
            schema = self.db_config['schema']
            placeholders = ','.join(['%s'] * len(clean_ids))
            cursor.execute(f'''
                SELECT function_id, function_name
                FROM {schema}.html_function
                WHERE function_id IN ({placeholders})
            ''', clean_ids)
            
            functions = []
            for row in cursor.fetchall():
                functions.append({
                    'id': f'html_{row["function_id"]}',
                    'function_id': row['function_id'],
                    'name': row['function_name'],
                    'file': f'Frontend/{row["function_name"]}',
                    'type': 'html',
                    'description': f'HTML/JS function: {row["function_name"]}',
                    'dependencies': 1
                })
            
            conn.close()
            return functions
            
        except Exception as e:
            print(f"❌ Error loading HTML functions by IDs: {e}")
            return []
    
    def get_function_by_id(self, function_id: str) -> Dict[str, Any]:
        """Lấy function specific"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Remove 'html_' prefix nếu có
            clean_id = function_id.replace('html_', '')
            
            schema = self.db_config['schema']
            cursor.execute(f'''
                SELECT function_id, function_name
                FROM {schema}.html_function
                WHERE function_id = %s
            ''', (clean_id,))
            
            row = cursor.fetchone()
            if row:
                function = {
                    'id': f'html_{row["function_id"]}',
                    'function_id': row['function_id'],
                    'name': row['function_name'],
                    'file': f'Frontend/{row["function_name"]}',
                    'type': 'html',
                    'description': f'HTML/JS function: {row["function_name"]}',
                    'dependencies': 1
                }
            else:
                function = None
            
            conn.close()
            return function
            
        except Exception as e:
            print(f"❌ Error loading HTML function by ID: {e}")
            return None
    
    def add_function(self, function_data: Dict[str, str]) -> bool:
        """Thêm function mới"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            schema = self.db_config['schema']
            cursor.execute(f'''
                INSERT INTO {schema}.html_function (function_id, function_name)
                VALUES (%s, %s)
                ON CONFLICT (function_id) DO UPDATE SET
                function_name = EXCLUDED.function_name
            ''', (
                function_data['function_id'],
                function_data['function_name']
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error adding function: {e}")
            return False
    
    def get_controller_mappings_for_html(self, selected_html_functions: List[str]) -> Dict[str, str]:
        """
        Tạo mapping chính xác từ HTML functions đến Java controllers/services
        Dựa trên Java project structure thực tế
        """
        mappings = {}
        
        for html_func_id in selected_html_functions:
            if html_func_id.startswith('html_'):
                clean_id = html_func_id.replace('html_', '')
                
                # Lấy function name từ database để mapping chính xác
                function_data = self.get_function_by_id(html_func_id)
                if not function_data:
                    continue
                    
                function_name = function_data['name'].lower()
                
                # Mapping logic dựa trên function name thực tế
                if any(keyword in function_name for keyword in ['user', 'login', 'registration', 'profile']):
                    mappings[html_func_id] = 'UserController'
                elif any(keyword in function_name for keyword in ['order', 'cart', 'checkout']):
                    mappings[html_func_id] = 'OrderController'
                elif any(keyword in function_name for keyword in ['product', 'search', 'catalog']):
                    mappings[html_func_id] = 'Product'  # Product model class
                elif any(keyword in function_name for keyword in ['payment', 'billing']):
                    mappings[html_func_id] = 'PaymentService'
                elif any(keyword in function_name for keyword in ['notification', 'alert']):
                    mappings[html_func_id] = 'NotificationService'
                elif any(keyword in function_name for keyword in ['address']):
                    mappings[html_func_id] = 'Address'  # Address model via UserService
                elif any(keyword in function_name for keyword in ['dashboard', 'management', 'admin']):
                    # Dashboard functions map to multiple components
                    if 'user' in function_name:
                        mappings[html_func_id] = 'UserRepository'
                    elif 'order' in function_name:
                        mappings[html_func_id] = 'OrderRepository'
                    elif 'product' in function_name:
                        mappings[html_func_id] = 'ProductRepository'
                    else:
                        mappings[html_func_id] = 'UserController'  # Default for general admin
                else:
                    mappings[html_func_id] = 'UserController'  # Default fallback
        
        return mappings

if __name__ == "__main__":
    # Test database connection
    try:
        db = HTMLFunctionDatabase()
        functions = db.get_all_functions()
        print(f"Found {len(functions)} HTML functions:")
        for func in functions[:5]:  # Show first 5
            print(f"  - {func['name']} (ID: {func['function_id']})")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Make sure PostgreSQL is running and configure connection:")
        print("   Set environment variables: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        print("   Or update db_config in the constructor")
