#!/usr/bin/env python3
import psycopg2

try:
    conn = psycopg2.connect(host='localhost', database='graph', user='postgres', password='123456')
    cursor = conn.cursor()
    
    # Check if html_function table exists and its structure
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'html_function'")
    columns = cursor.fetchall()
    print("HTML Function Table Columns:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    
    # Check all html-related tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '%html%'")
    tables = cursor.fetchall()
    print(f"\nHTML Tables: {[t[0] for t in tables]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
