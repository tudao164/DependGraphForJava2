#!/usr/bin/env python3
"""
Script để thêm HTML functions từ ecommerce_frontend.html vào PostgreSQL database
"""

import psycopg2
from html_db import HTMLFunctionDatabase

def add_ecommerce_html_functions():
    """Thêm các HTML functions từ ecommerce frontend vào database"""
    
    try:
        html_db = HTMLFunctionDatabase()
        
        # Clear existing data
        print("🧹 Clearing existing HTML functions...")
        html_db.clear_all_functions()
        
        # Define HTML functions based on ecommerce_frontend.html
        html_functions = [
            # User Management Functions
            {
                'name': 'User Registration Form',
                'file': 'Frontend/User Registration',
                'type': 'html',
                'description': 'HTML/JS function: User registration with email, password, fullname validation',
                'java_controller': 'UserController'
            },
            {
                'name': 'User Login Form', 
                'file': 'Frontend/User Login',
                'type': 'html',
                'description': 'HTML/JS function: User authentication and login',
                'java_controller': 'UserController'
            },
            {
                'name': 'Forgot Password Form',
                'file': 'Frontend/Password Recovery',
                'type': 'html', 
                'description': 'HTML/JS function: Send OTP for password recovery',
                'java_controller': 'UserController'
            },
            {
                'name': 'Get User Info Function',
                'file': 'Frontend/User Profile',
                'type': 'html',
                'description': 'HTML/JS function: Retrieve user information by ID',
                'java_controller': 'UserController'
            },
            
            # Product Management Functions
            {
                'name': 'Product List Display',
                'file': 'Frontend/Product Catalog',
                'type': 'html',
                'description': 'HTML/JS function: Display all products with pagination',
                'java_controller': 'ProductController'
            },
            {
                'name': 'Product Search Function',
                'file': 'Frontend/Product Search',
                'type': 'html',
                'description': 'HTML/JS function: Search products by name with filters',
                'java_controller': 'ProductController'
            },
            {
                'name': 'Category Products Display',
                'file': 'Frontend/Category Browse',
                'type': 'html',
                'description': 'HTML/JS function: Show products filtered by category',
                'java_controller': 'ProductController'
            },
            
            # Category Management Functions  
            {
                'name': 'Category Navigation Menu',
                'file': 'Frontend/Category Menu',
                'type': 'html',
                'description': 'HTML/JS function: Display hierarchical category navigation',
                'java_controller': 'CategoryController'
            },
            {
                'name': 'Root Categories Display',
                'file': 'Frontend/Main Categories',
                'type': 'html',
                'description': 'HTML/JS function: Show main category sections',
                'java_controller': 'CategoryController'
            },
            
            # Cart Management Functions
            {
                'name': 'Shopping Cart View',
                'file': 'Frontend/Shopping Cart',
                'type': 'html',
                'description': 'HTML/JS function: Display user shopping cart with items',
                'java_controller': 'CartController'
            },
            {
                'name': 'Add to Cart Function',
                'file': 'Frontend/Cart Actions',
                'type': 'html',
                'description': 'HTML/JS function: Add products to shopping cart',
                'java_controller': 'CartController'
            },
            {
                'name': 'Remove from Cart Function',
                'file': 'Frontend/Cart Management',
                'type': 'html',
                'description': 'HTML/JS function: Remove items from shopping cart',
                'java_controller': 'CartController'
            },
            
            # Order Management Functions
            {
                'name': 'User Order History',
                'file': 'Frontend/Order History',
                'type': 'html',
                'description': 'HTML/JS function: Display user order history and status',
                'java_controller': 'OrderController'
            },
            {
                'name': 'Order Details View',
                'file': 'Frontend/Order Details',
                'type': 'html',
                'description': 'HTML/JS function: Show detailed order information',
                'java_controller': 'OrderController'
            },
            {
                'name': 'Checkout Process',
                'file': 'Frontend/Checkout',
                'type': 'html',
                'description': 'HTML/JS function: Handle order checkout and payment',
                'java_controller': 'OrderController'
            },
            
            # Review Management Functions
            {
                'name': 'Product Reviews Display',
                'file': 'Frontend/Product Reviews',
                'type': 'html',
                'description': 'HTML/JS function: Show product reviews and ratings',
                'java_controller': 'ReviewController'
            },
            {
                'name': 'User Reviews Display',
                'file': 'Frontend/User Reviews',
                'type': 'html',
                'description': 'HTML/JS function: Display reviews written by user',
                'java_controller': 'ReviewController'
            },
            {
                'name': 'Create Review Form',
                'file': 'Frontend/Review Form',
                'type': 'html',
                'description': 'HTML/JS function: Submit product review and rating',
                'java_controller': 'ReviewController'
            },
            
            # Additional E-commerce Functions
            {
                'name': 'Product Detail View',
                'file': 'Frontend/Product Details',
                'type': 'html',
                'description': 'HTML/JS function: Display detailed product information',
                'java_controller': 'ProductController'
            },
            {
                'name': 'User Profile Management',
                'file': 'Frontend/Profile Settings',
                'type': 'html',
                'description': 'HTML/JS function: Update user profile information',
                'java_controller': 'UserController'
            }
        ]
        
        print(f"📝 Adding {len(html_functions)} HTML functions to database...")
        
        # Add each function to database
        for idx, func in enumerate(html_functions, 1):
            try:
                html_db.add_function(
                    name=func['name'],
                    file=func['file'],
                    func_type=func['type'],
                    description=func['description']
                )
                print(f"  ✅ Added: {func['name']}")
            except Exception as e:
                print(f"  ❌ Error adding {func['name']}: {e}")
        
        print(f"\n🔗 Setting up HTML→Java controller mappings...")
        
        # Setup controller mappings
        controller_mappings = [
            # UserController mappings
            ('html_1', 'UserController'),   # User Registration Form
            ('html_2', 'UserController'),   # User Login Form  
            ('html_3', 'UserController'),   # Forgot Password Form
            ('html_4', 'UserController'),   # Get User Info Function
            ('html_20', 'UserController'),  # User Profile Management
            
            # ProductController mappings
            ('html_5', 'ProductController'),  # Product List Display
            ('html_6', 'ProductController'),  # Product Search Function
            ('html_7', 'ProductController'),  # Category Products Display
            ('html_19', 'ProductController'), # Product Detail View
            
            # CategoryController mappings
            ('html_8', 'CategoryController'), # Category Navigation Menu
            ('html_9', 'CategoryController'), # Root Categories Display
            
            # CartController mappings
            ('html_10', 'CartController'),   # Shopping Cart View
            ('html_11', 'CartController'),   # Add to Cart Function
            ('html_12', 'CartController'),   # Remove from Cart Function
            
            # OrderController mappings
            ('html_13', 'OrderController'),  # User Order History
            ('html_14', 'OrderController'),  # Order Details View
            ('html_15', 'OrderController'),  # Checkout Process
            
            # ReviewController mappings
            ('html_16', 'ReviewController'), # Product Reviews Display
            ('html_17', 'ReviewController'), # User Reviews Display
            ('html_18', 'ReviewController'), # Create Review Form
        ]
        
        for html_func_id, controller in controller_mappings:
            try:
                html_db.add_controller_mapping(html_func_id, controller)
                print(f"  🔗 Mapped: {html_func_id} → {controller}")
            except Exception as e:
                print(f"  ❌ Error mapping {html_func_id}: {e}")
        
        print(f"\n✅ Successfully added {len(html_functions)} HTML functions!")
        print(f"🔗 Successfully mapped {len(controller_mappings)} HTML→Java relationships!")
        
        # Verify the data
        all_functions = html_db.get_all_functions()
        print(f"\n📊 Database now contains {len(all_functions)} HTML functions:")
        for func in all_functions[:5]:  # Show first 5
            print(f"  - {func['name']} (ID: {func['id']})")
        if len(all_functions) > 5:
            print(f"  ... và {len(all_functions) - 5} functions khác")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_ecommerce_html_functions()
