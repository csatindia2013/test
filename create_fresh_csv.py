#!/usr/bin/env python3
"""
Create Fresh Test CSV
"""
import csv

def create_fresh_csv():
    """Create a fresh test CSV file"""
    filename = 'fresh_test_barcodes.csv'
    
    # Fresh test barcodes
    test_data = [
        {'barcode': '8901030865009', 'notes': 'Fresh test barcode 1'},
        {'barcode': '8901030865010', 'notes': 'Fresh test barcode 2'},
        {'barcode': '8901030865011', 'notes': 'Fresh test barcode 3'}
    ]
    
    # Write CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['barcode', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in test_data:
            writer.writerow(row)
    
    print(f"✅ Created fresh test CSV file: {filename}")
    print(f"📊 Contains {len(test_data)} fresh test barcodes")
    
    return filename

if __name__ == "__main__":
    create_fresh_csv()
