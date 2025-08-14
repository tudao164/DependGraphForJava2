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
        """Lấy tất cả HTML/JS functions từ PostgreSQL database với controller info"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            schema = self.db_config['schema']
            cursor.execute(f'''
                SELECT function_id, function_name, controller, service
                FROM {schema}.html_function
                ORDER BY function_name
            ''')
            
            functions = []
            for row in cursor.fetchall():
                functions.append({
                    'id': f'html_{row["function_id"]}',  # Prefix để phân biệt với Java functions
                    'function_id': row['function_id'],
                    'name': row['function_name'],
                    'controller': row.get('controller', 'Unknown'),
                    'service': row.get('service', 'Unknown'),
                    'file': f'Frontend/{row["function_name"]} -> {row.get("controller", "Unknown")} -> {row.get("service", "Unknown")}',
                    'type': 'html',
                    'description': f'HTML/JS function: {row["function_name"]} → {row.get("controller", "Unknown")} → {row.get("service", "Unknown")}',
                    'dependencies': 2  # Sẽ có dependency đến Java controller và service
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
        """Lấy function specific với controller info"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Remove 'html_' prefix nếu có
            clean_id = function_id.replace('html_', '')
            
            schema = self.db_config['schema']
            cursor.execute(f'''
                SELECT function_id, function_name, controller
                FROM {schema}.html_function
                WHERE function_id = %s
            ''', (clean_id,))
            
            row = cursor.fetchone()
            if row:
                function = {
                    'id': f'html_{row["function_id"]}',
                    'function_id': row['function_id'],
                    'name': row['function_name'],
                    'controller': row.get('controller', 'Unknown'),
                    'file': f'Frontend/{row["function_name"]} -> {row.get("controller", "Unknown")}',
                    'type': 'html',
                    'description': f'HTML/JS function: {row["function_name"]} calls {row.get("controller", "Unknown")}',
                    'dependencies': 1
                }
            else:
                function = None
            
            conn.close()
            return function
            
        except Exception as e:
            print(f"❌ Error loading HTML function by ID: {e}")
            return None
    
    def get_controller_mappings_for_html(self, selected_html_functions: List[str]) -> Dict[str, str]:
        """
        Lấy mapping chính xác từ HTML functions đến Java controllers từ database
        """
        mappings = {}
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            for html_func_id in selected_html_functions:
                if html_func_id.startswith('html_'):
                    clean_id = html_func_id.replace('html_', '')
                    
                    # Lấy controller từ database
                    schema = self.db_config['schema']
                    cursor.execute(f'''
                        SELECT controller, function_name
                        FROM {schema}.html_function
                        WHERE function_id = %s
                    ''', (clean_id,))
                    
                    row = cursor.fetchone()
                    if row and row['controller']:
                        mappings[html_func_id] = row['controller']
                        print(f"🔗 {html_func_id} → {row['controller']} (from {row['function_name']})")
                    else:
                        print(f"⚠️ No controller mapping found for {html_func_id}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error getting controller mappings: {e}")
        
        return mappings

    def clear_all_functions(self):
        """Clear all HTML functions from database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            schema = self.db_config['schema']
            
            # Clear functions
            cursor.execute(f'DELETE FROM {schema}.html_function')
            print("   🧹 Cleared HTML functions")
            
            conn.commit()
            conn.close()
            print("✅ Database cleared successfully")
            
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            
    def add_function(self, name: str, file: str, func_type: str, description: str) -> bool:
        """Add HTML function to database with existing schema"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            schema = self.db_config['schema']
            
            # Get next function_id
            cursor.execute(f'SELECT COALESCE(MAX(function_id), 0) + 1 FROM {schema}.html_function')
            next_id = cursor.fetchone()[0]
            
            # Insert with existing schema (function_id, function_name only)
            cursor.execute(f'''
                INSERT INTO {schema}.html_function (function_id, function_name)
                VALUES (%s, %s)
            ''', (next_id, f"{name} - {description}"))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error adding function {name}: {e}")
            return False
            
    def add_controller_mapping(self, html_func_id: str, controller_name: str) -> bool:
        """Skip controller mapping as table doesn't exist yet"""
        # For now, just return True since the table doesn't exist
        # The mapping will be handled in the analyzer logic
        return True

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
