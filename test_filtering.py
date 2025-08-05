#!/usr/bin/env python3
"""
Test script để demo selective filtering với Function Selector
"""

import json
import requests
import time

def test_selective_filtering():
    """Test các scenarios selective filtering"""
    
    print("🧪 Testing Function Selector - Selective Filtering")
    print("="*60)
    
    base_url = "http://localhost:8001"
    
    # Test 1: Lấy danh sách functions
    print("\n1️⃣ Getting functions list...")
    try:
        response = requests.get(f"{base_url}/api/functions")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                functions = data["functions"]
                print(f"✅ Found {len(functions)} functions")
                
                # Phân loại
                classes = [f for f in functions if f["type"] == "class"]
                services = [f for f in functions if f["type"] == "service"]
                methods = [f for f in functions if f["type"] == "method"]
                
                print(f"   📊 Classes: {len(classes)}")
                print(f"   🔧 Services: {len(services)}")
                print(f"   ⚙️ Methods: {len(methods)}")
                
                # Test 2: Select only services
                print("\n2️⃣ Testing Service-only selection...")
                service_ids = [f["id"] for f in services[:3]]  # Top 3 services
                test_generate_graph(base_url, service_ids, "Services only")
                
                time.sleep(2)
                
                # Test 3: Select Order-related classes
                print("\n3️⃣ Testing Order-related selection...")
                order_classes = [f["id"] for f in classes if "Order" in f["name"]]
                test_generate_graph(base_url, order_classes, "Order-related classes")
                
                time.sleep(2)
                
                # Test 4: Select User-related classes
                print("\n4️⃣ Testing User-related selection...")
                user_classes = [f["id"] for f in classes if "User" in f["name"]]
                test_generate_graph(base_url, user_classes, "User-related classes")
                
            else:
                print(f"❌ API Error: {data['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure Function Selector server is running!")

def test_generate_graph(base_url, selected_ids, description):
    """Test graph generation với selected functions"""
    try:
        payload = {"selectedFunctions": selected_ids}
        response = requests.post(f"{base_url}/api/generate", 
                               json=payload,
                               headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print(f"   ✅ {description}: {data['message']}")
            else:
                print(f"   ❌ {description}: {data['message']}")
        else:
            print(f"   ❌ {description}: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ {description}: {e}")

if __name__ == "__main__":
    print("🎯 Make sure Function Selector is running at http://localhost:8001")
    input("Press Enter when ready...")
    test_selective_filtering()
