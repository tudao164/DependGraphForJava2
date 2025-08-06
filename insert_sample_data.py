#!/usr/bin/env python3
"""
Script để thêm sample data vào PostgreSQL database
"""

from html_db import HTMLFunctionDatabase

def insert_sample_data():
    """Thêm sample HTML functions vào database"""
    
    try:
        db = HTMLFunctionDatabase()
        
        # Sample data phù hợp với Java controllers trong project
        sample_functions = [
            {'function_id': '1', 'function_name': 'loginForm()'},
            {'function_id': '2', 'function_name': 'userRegistration()'},
            {'function_id': '3', 'function_name': 'userProfile()'},
            {'function_id': '4', 'function_name': 'orderSubmit()'},
            {'function_id': '5', 'function_name': 'orderList()'},
            {'function_id': '6', 'function_name': 'orderStatus()'},
            {'function_id': '7', 'function_name': 'productSearch()'},
            {'function_id': '8', 'function_name': 'productDetail()'},
            {'function_id': '9', 'function_name': 'paymentProcess()'},
            {'function_id': '10', 'function_name': 'addressManagement()'}
        ]
        
        print("🔄 Inserting sample HTML functions...")
        
        success_count = 0
        for func_data in sample_functions:
            if db.add_function(func_data):
                success_count += 1
                print(f"   ✅ Added: {func_data['function_name']}")
            else:
                print(f"   ❌ Failed: {func_data['function_name']}")
        
        print(f"\n✅ Successfully inserted {success_count}/{len(sample_functions)} functions")
        
        # Test lại để xem data
        functions = db.get_all_functions()
        print(f"\n📊 Total functions in database: {len(functions)}")
        for func in functions:
            print(f"   - {func['name']} (ID: {func['function_id']})")
            
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")

if __name__ == "__main__":
    insert_sample_data()
