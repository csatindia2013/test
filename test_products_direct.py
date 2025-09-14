#!/usr/bin/env python3
"""
Quick Fix: Direct Firebase Test and Product Retrieval
"""
import firebase_admin
from firebase_admin import credentials, firestore
import json

def get_products_direct():
    """Get products directly from Firebase"""
    try:
        # Initialize Firebase if not already done
        try:
            existing_app = firebase_admin.get_app()
            print("Using existing Firebase app")
        except ValueError:
            print("Initializing Firebase...")
            cred = credentials.Certificate('firebase-service-account.json')
            firebase_admin.initialize_app(cred)
            print("Firebase initialized")
        
        # Get Firestore client
        db = firestore.client()
        
        # Get products from barcode_cache
        products_ref = db.collection('barcode_cache')
        docs = products_ref.stream()
        
        products = []
        for doc in docs:
            product_data = doc.to_dict()
            mapped_product = {
                'id': doc.id,
                'name': product_data.get('name', 'Unnamed Product'),
                'brand': product_data.get('brand', ''),
                'category': product_data.get('category', ''),
                'barcode': doc.id,
                'mrp': product_data.get('mrp', 0),
                'salePrice': product_data.get('salePrice', 0),
                'stock': product_data.get('stockQuantity', 0),
                'isActive': product_data.get('isActive', True),
                'useInFirstStart': product_data.get('useInFirstStart', False),
                'imageUrl': product_data.get('photoPath', ''),
                'description': product_data.get('description', ''),
                'createdAt': product_data.get('createdAt', ''),
                'updatedAt': product_data.get('updatedAt', ''),
                'size': product_data.get('size', ''),
                'unit': product_data.get('unit', ''),
                'scanCount': product_data.get('scanCount', 0),
                'syncStatus': product_data.get('syncStatus', ''),
                'sortOrder': product_data.get('sortOrder', 0)
            }
            products.append(mapped_product)
        
        print(f"✅ Successfully retrieved {len(products)} products")
        return products
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    print("🔍 Testing direct product retrieval...")
    products = get_products_direct()
    
    if products:
        print(f"\n📦 Found {len(products)} products:")
        for i, product in enumerate(products[:3]):  # Show first 3
            print(f"{i+1}. {product['name']} (Barcode: {product['barcode']})")
        
        print(f"\n✅ SUCCESS: Products are available in Firebase!")
        print("🔧 The issue is with Flask app Firebase initialization, not the data.")
    else:
        print("\n❌ FAILED: No products found")
