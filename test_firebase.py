#!/usr/bin/env python3
"""
Firebase Connection Test Script
"""
import firebase_admin
from firebase_admin import credentials, firestore
import json

def test_firebase_connection():
    print("Testing Firebase connection...")
    
    try:
        # Try to initialize Firebase
        try:
            existing_app = firebase_admin.get_app()
            print("Firebase app already initialized")
        except ValueError:
            print("Initializing Firebase...")
            cred = credentials.Certificate('firebase-service-account.json')
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully")
        
        # Get Firestore client
        db = firestore.client()
        print("Firestore client created")
        
        # Test getting collections
        collections = list(db.collections())
        print(f"Found {len(collections)} collections:")
        for collection in collections:
            print(f"  - {collection.id}")
        
        # Test barcode_cache collection
        barcode_cache_ref = db.collection('barcode_cache')
        sample_docs = list(barcode_cache_ref.limit(5).stream())
        print(f"Found {len(sample_docs)} documents in barcode_cache")
        
        if sample_docs:
            print("Sample document:")
            doc = sample_docs[0]
            print(f"  ID: {doc.id}")
            print(f"  Data: {doc.to_dict()}")
        else:
            print("No documents found in barcode_cache collection")
        
        return True
        
    except Exception as e:
        print(f"Firebase test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_firebase_connection()
    if success:
        print("\n✅ Firebase connection test PASSED")
    else:
        print("\n❌ Firebase connection test FAILED")
