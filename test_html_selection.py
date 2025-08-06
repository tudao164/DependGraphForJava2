#!/usr/bin/env python3
"""
Test script để demo HTML-only selection
"""

import requests
import json

def test_html_only_selection():
    """Test chọn chỉ HTML functions và auto-map đến Java"""
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Lấy danh sách functions
        print("📋 Getting functions list...")
        response = requests.get(f"{base_url}/api/functions")
        if response.status_code == 200:
            data = response.json()
            functions = data.get('functions', [])
            
            # Filter chỉ HTML functions
            html_functions = [f for f in functions if f['type'] == 'html']
            print(f"✅ Found {len(html_functions)} HTML functions:")
            
            for func in html_functions[:5]:  # Show first 5
                print(f"   - {func['name']} (ID: {func['id']})")
            
            # 2. Test chọn một vài HTML functions
            test_selections = [
                # User-related functions
                [func['id'] for func in html_functions if 'user' in func['name'].lower()][:2],
                # Order-related functions  
                [func['id'] for func in html_functions if 'order' in func['name'].lower()][:2],
                # Single function test
                [html_functions[0]['id']] if html_functions else []
            ]
            
            for i, selected_functions in enumerate(test_selections, 1):
                if not selected_functions:
                    continue
                    
                print(f"\n🧪 Test {i}: Selecting {len(selected_functions)} HTML functions")
                for func_id in selected_functions:
                    func = next((f for f in html_functions if f['id'] == func_id), None)
                    if func:
                        print(f"   📱 {func['name']}")
                
                # Generate graph
                payload = {"selectedFunctions": selected_functions}
                response = requests.post(f"{base_url}/api/generate", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"   ✅ {result.get('message')}")
                        print(f"   🌐 Graph available at: {base_url}/dependencies.html")
                    else:
                        print(f"   ❌ Failed: {result.get('message')}")
                else:
                    print(f"   ❌ HTTP Error: {response.status_code}")
                
                print("   " + "-"*50)
        else:
            print(f"❌ Failed to get functions: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing HTML-only selection with auto Java mapping...")
    print("🔄 Make sure server is running at http://localhost:8000")
    print()
    test_html_only_selection()
