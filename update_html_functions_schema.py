#!/usr/bin/env python3
"""
Script để cập nhật database schema và thêm HTML functions với controller mapping
"""

import psycopg2

def update_database_schema():
    """Update database schema để thêm controller column"""
    try:
        conn = psycopg2.connect(host='localhost', database='graph', user='postgres', password='123456')
        cursor = conn.cursor()
        
        print("🔧 Updating database schema...")
        
        # Add controller column to html_function table
        try:
            cursor.execute("ALTER TABLE html_function ADD COLUMN controller VARCHAR(100)")
            print("✅ Added controller column")
        except Exception as e:
            if "already exists" in str(e):
                print("ℹ️ Controller column already exists")
            else:
                print(f"❌ Error adding controller column: {e}")
        
        # Clear existing data
        cursor.execute("DELETE FROM html_function")
        print("🧹 Cleared existing HTML functions")
        
        conn.commit()
        conn.close()
        print("✅ Database schema updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating schema: {e}")

def add_html_functions_with_controllers():
    """Add HTML functions với controller mapping chính xác"""
    try:
        conn = psycopg2.connect(host='localhost', database='graph', user='postgres', password='123456')
        cursor = conn.cursor()
        
        # HTML functions với controller mapping chính xác
        html_functions = [
            # User Management Functions - UserController
            (1, 'registerUser()', 'UserController'),
            (2, 'loginUser()', 'UserController'), 
            (3, 'forgotPassword()', 'UserController'),
            (4, 'getUserInfo()', 'UserController'),
            
            # Product Management Functions - ProductController
            (5, 'getAllProducts()', 'ProductController'),
            (6, 'searchProducts()', 'ProductController'),
            (7, 'getProductsByCategory()', 'ProductController'),
            
            # Category Management Functions - CategoryController
            (8, 'getAllCategories()', 'CategoryController'),
            (9, 'getRootCategories()', 'CategoryController'),
            
            # Cart Management Functions - CartController
            (10, 'getCartByUser()', 'CartController'),
            (11, 'addToCart()', 'CartController'),
            (12, 'removeFromCart()', 'CartController'),
            
            # Order Management Functions - OrderController
            (13, 'getUserOrders()', 'OrderController'),
            (14, 'getOrderById()', 'OrderController'),
            (15, 'checkout()', 'OrderController'),
            
            # Review Management Functions - ReviewController
            (16, 'getProductReviews()', 'ReviewController'),
            (17, 'getUserReviews()', 'ReviewController'),
            (18, 'createReview()', 'ReviewController'),
        ]
        
        print(f"📝 Adding {len(html_functions)} HTML functions with controller mapping...")
        
        for func_id, function_name, controller in html_functions:
            cursor.execute("""
                INSERT INTO html_function (function_id, function_name, controller)
                VALUES (%s, %s, %s)
            """, (func_id, function_name, controller))
            print(f"  ✅ Added: {function_name} → {controller}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Successfully added {len(html_functions)} HTML functions!")
        
        # Verify the data
        conn = psycopg2.connect(host='localhost', database='graph', user='postgres', password='123456')
        cursor = conn.cursor()
        cursor.execute("SELECT function_id, function_name, controller FROM html_function ORDER BY function_id")
        results = cursor.fetchall()
        
        print(f"\n📊 Database now contains {len(results)} HTML functions:")
        for func_id, func_name, controller in results:
            print(f"  {func_id}. {func_name} → {controller}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_database_schema()
    add_html_functions_with_controllers()
