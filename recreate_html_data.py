#!/usr/bin/env python3
"""
Script để tạo lại HTML functions data phù hợp với Java project structure
"""

from html_db import HTMLFunctionDatabase
import psycopg2

def clear_and_recreate_data():
    """Clear database và tạo lại HTML functions phù hợp với Java controllers/services"""
    
    try:
        db = HTMLFunctionDatabase()
        
        # Clear existing data
        print("🗑️ Clearing existing HTML functions...")
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM public.html_function")
        conn.commit()
        conn.close()
        print("✅ Cleared existing data")
        
        # Tạo HTML functions dựa trên Java project structure thực tế
        realistic_functions = [
            # User Management - maps to UserController + UserService
            {'function_id': '1', 'function_name': 'User Login Form'},
            {'function_id': '2', 'function_name': 'User Registration Form'},
            {'function_id': '3', 'function_name': 'User Profile Page'},
            {'function_id': '4', 'function_name': 'Edit User Profile'},
            
            # Order Management - maps to OrderController + OrderService
            {'function_id': '5', 'function_name': 'Create New Order'},
            {'function_id': '6', 'function_name': 'View Order List'},
            {'function_id': '7', 'function_name': 'Order Status Tracking'},
            {'function_id': '8', 'function_name': 'Cancel Order'},
            
            # Product related - sẽ map đến các Product classes
            {'function_id': '9', 'function_name': 'Product Search'},
            {'function_id': '10', 'function_name': 'Product Detail View'},
            {'function_id': '11', 'function_name': 'Add to Cart'},
            
            # Payment - maps to PaymentService
            {'function_id': '12', 'function_name': 'Payment Processing'},
            {'function_id': '13', 'function_name': 'Payment History'},
            
            # Notifications - maps to NotificationService  
            {'function_id': '14', 'function_name': 'Notification Settings'},
            {'function_id': '15', 'function_name': 'Push Notifications'},
            
            # Address Management - maps to Address model via UserService
            {'function_id': '16', 'function_name': 'Manage Addresses'},
            {'function_id': '17', 'function_name': 'Add New Address'},
            
            # Admin/Repository functions - maps to Repository classes
            {'function_id': '18', 'function_name': 'User Management Dashboard'},
            {'function_id': '19', 'function_name': 'Order Management Dashboard'},
            {'function_id': '20', 'function_name': 'Product Management Dashboard'}
        ]
        
        print(f"🔄 Inserting {len(realistic_functions)} realistic HTML functions...")
        
        success_count = 0
        for func_data in realistic_functions:
            if db.add_function(func_data):
                success_count += 1
                print(f"   ✅ Added: {func_data['function_name']}")
            else:
                print(f"   ❌ Failed: {func_data['function_name']}")
        
        print(f"\n✅ Successfully inserted {success_count}/{len(realistic_functions)} functions")
        
        # Test lại để xem data
        functions = db.get_all_functions()
        print(f"\n📊 Total functions in database: {len(functions)}")
        print("\n🎯 HTML Functions → Java Mapping Preview:")
        for func in functions[:10]:  # Show first 10
            print(f"   - {func['name']} (ID: {func['function_id']})")
            
    except Exception as e:
        print(f"❌ Error recreating data: {e}")

if __name__ == "__main__":
    clear_and_recreate_data()
