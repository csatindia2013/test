#!/usr/bin/env python3
"""
Test UI Display Issue
"""
import requests
import json

def test_ui_display():
    """Test if the UI is displaying unfound barcodes correctly"""
    
    print("🔍 Testing UI Display Issue...")
    
    # Test 1: Check API response
    try:
        response = requests.get('http://localhost:5000/api/unfound-barcodes')
        unfound = response.json()
        
        print(f"✅ API Response: {len(unfound)} unfound barcodes")
        print(f"📊 Barcodes: {[b.get('barcode') for b in unfound]}")
        print(f"🏷️ Sources: {[b.get('source', 'unknown') for b in unfound]}")
        
        if len(unfound) > 0:
            print(f"\n🎯 UI Should Show:")
            print(f"   - {len(unfound)} unfound barcodes")
            print(f"   - Sources: {set([b.get('source', 'unknown') for b in unfound])}")
            print(f"   - Latest barcode: {unfound[-1].get('barcode')}")
            
            print(f"\n💡 Troubleshooting:")
            print(f"   1. Check if you're on the 'Unfound Barcodes' tab")
            print(f"   2. Try refreshing the page (F5)")
            print(f"   3. Check browser console for errors")
            print(f"   4. Clear browser cache")
            
        else:
            print(f"❌ No unfound barcodes found - this might be the issue!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ui_display()
