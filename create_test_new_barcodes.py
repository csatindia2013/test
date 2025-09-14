#!/usr/bin/env python3
"""
Create Test CSV with New Barcodes
"""
import csv

def create_test_csv():
    """Create a test CSV file with new barcodes"""
    filename = 'test_new_barcodes.csv'
    
    # New test barcodes
    test_data = [
        {'barcode': '8901030865003', 'notes': 'New test barcode 1'},
        {'barcode': '8901030865004', 'notes': 'New test barcode 2'},
        {'barcode': '8901030865005', 'notes': 'New test barcode 3'},
        {'barcode': '8901030865006', 'notes': 'New test barcode 4'},
        {'barcode': '8901030865007', 'notes': 'New test barcode 5'}
    ]
    
    # Write CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['barcode', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in test_data:
            writer.writerow(row)
    
    print(f"✅ Created test CSV file: {filename}")
    print(f"📊 Contains {len(test_data)} new test barcodes")
    
    return filename

if __name__ == "__main__":
    create_test_csv()
