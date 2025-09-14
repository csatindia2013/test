#!/usr/bin/env python3
"""
Test Unfound Barcodes Creation
"""
import requests
import json

def test_unfound_creation():
    """Test creating unfound barcodes"""
    url = "http://localhost:5000/api/unfound-barcodes"
    
    test_barcode = "8901030865008"
    
    try:
        print(f"📤 Testing unfound barcode creation for: {test_barcode}")
        
        data = {'barcode': test_barcode}
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if response.status_code == 200:
            print(f"✅ Successfully created unfound barcode")
        else:
            print(f"❌ Failed to create unfound barcode")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_unfound_creation()
