#!/usr/bin/env python3
"""
Create Test Unfound Barcodes for Scraping Demo
"""
import requests
import json

def create_test_unfound_barcodes():
    """Create some test unfound barcodes"""
    test_barcodes = [
        "1234567890123",  # This should fail
        "8901030865000",  # Parle-G - should work
        "8901030865001",  # Another test
        "9999999999999",  # Invalid barcode
        "8901030865002"   # Another valid one
    ]
    
    created_count = 0
    for barcode in test_barcodes:
        try:
            data = {
                "barcode": barcode,
                "createdAt": "2025-01-14T23:50:00",
                "lastRetry": None,
                "retryCount": 0
            }
            
            response = requests.post('http://localhost:5000/api/unfound-barcodes', json=data)
            if response.status_code == 200:
                created_count += 1
                print(f"✅ Created unfound barcode: {barcode}")
            else:
                print(f"❌ Failed to create barcode {barcode}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating barcode {barcode}: {e}")
    
    print(f"\n📊 Created {created_count} test unfound barcodes")
    return created_count

if __name__ == "__main__":
    create_test_unfound_barcodes()
