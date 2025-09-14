#!/usr/bin/env python3
"""
Test Unfound Barcodes Scraping
"""
import requests
import json

def test_scrape_unfound_barcodes():
    """Test scraping unfound barcodes"""
    try:
        # First, get the unfound barcodes
        response = requests.get('http://localhost:5000/api/unfound-barcodes')
        unfound_barcodes = response.json()
        
        if not unfound_barcodes:
            print("No unfound barcodes to scrape")
            return
        
        print(f"Found {len(unfound_barcodes)} unfound barcodes")
        
        # Take first 2 barcodes for testing
        test_barcodes = unfound_barcodes[:2]
        barcode_ids = [b['id'] for b in test_barcodes]
        
        print(f"Testing scraping for barcodes: {[b['barcode'] for b in test_barcodes]}")
        
        # Scrape them
        scrape_data = {'barcode_ids': barcode_ids}
        scrape_response = requests.post('http://localhost:5000/api/unfound-barcodes/scrape', json=scrape_data)
        
        if scrape_response.status_code == 200:
            result = scrape_response.json()
            print(f"✅ Scraping completed!")
            print(f"📊 Processed: {result['processed_count']}")
            print(f"✅ Scraped: {result['scraped_count']}")
            print(f"❌ Failed: {result['failed_count']}")
            if result.get('errors'):
                print(f"⚠️ Errors: {result['errors']}")
        else:
            print(f"❌ Scraping failed: {scrape_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_scrape_unfound_barcodes()
