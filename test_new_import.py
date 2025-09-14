#!/usr/bin/env python3
"""
Test New Import Functionality
"""
import requests
import os

def test_new_import():
    """Test the new import functionality"""
    url = "http://localhost:5000/api/import-barcodes"
    file_path = "test_new_barcodes.csv"
    
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} not found")
        return
    
    try:
        print(f"📤 Testing import of {file_path}...")
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if response.status_code == 200:
            print(f"\n📊 Import Results:")
            print(f"✅ Processed: {result['processed_count']} barcodes")
            print(f"📝 Added to unfound: {result['scraped_count']} barcodes")
            print(f"⏭️ Skipped: {result['skipped_count']} existing")
            
            if result.get('errors'):
                print(f"⚠️ Errors: {result['errors']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_new_import()
