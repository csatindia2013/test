#!/usr/bin/env python3
"""
Create Sample CSV File for Barcode Import Testing
"""
import csv

def create_sample_csv():
    """Create a sample CSV file with barcodes for testing"""
    filename = 'sample_barcodes.csv'
    
    # Sample barcodes data
    sample_data = [
        {'barcode': '015000047757', 'notes': 'Yogurt blends snack'},
        {'barcode': '3017620425035', 'notes': 'Nutella'},
        {'barcode': '3175680011480', 'notes': 'Sésame'},
        {'barcode': '1234567890123', 'notes': 'Test barcode - should fail'},
        {'barcode': '8901030865000', 'notes': 'Parle-G Biscuits'},
        {'barcode': '8901030865001', 'notes': 'Another test barcode'}
    ]
    
    # Write CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['barcode', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in sample_data:
            writer.writerow(row)
    
    print(f"✅ Created sample CSV file: {filename}")
    print(f"📊 Contains {len(sample_data)} sample barcodes")
    print(f"📋 Headers: {fieldnames}")
    
    return filename

if __name__ == "__main__":
    create_sample_csv()
