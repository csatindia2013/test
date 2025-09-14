#!/usr/bin/env python3
"""
Test CSV Import Functionality
"""
import requests
import os

def test_csv_import():
    """Test the CSV import endpoint"""
    url = "http://localhost:5000/api/import-barcodes"
    file_path = "sample_barcodes.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} not found")
        return
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_csv_import()
