#!/usr/bin/env python3
"""
Working Flask App with Firebase - Simplified Version
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
import json
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
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

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pos-dashboard-secret-key')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role='admin'):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    user1_username = os.environ.get('USER1_USERNAME', 'user1')
    
    users = {
        admin_username: User(admin_username, admin_username, 'admin'),
        user1_username: User(user1_username, user1_username, 'user')
    }
    return users.get(user_id)

CORS(app)

# Routes
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', generate_password_hash('admin123'))
        user1_username = os.environ.get('USER1_USERNAME', 'user1')
        user1_password_hash = os.environ.get('USER1_PASSWORD_HASH', generate_password_hash('user123'))
        
        users = {
            admin_username: admin_password_hash,
            user1_username: user1_password_hash
        }
        
        if username in users and check_password_hash(users[username], password):
            user = User(username, username)
            login_user(user)
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid username or password'
            }), 401
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({
        'status': 'success',
        'message': 'Logged out successfully'
    })

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    if current_user.is_authenticated:
        return jsonify({
            'status': 'success',
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'role': current_user.role
            }
        })
    else:
        return jsonify({
            'status': 'success',
            'authenticated': False
        })

@app.route('/api/products', methods=['GET'])
@login_required
def get_products():
    """Get all products from Firebase"""
    try:
        print("Getting products from Firebase...")
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
        
        print(f"Retrieved {len(products)} products")
        return jsonify(products)
        
    except Exception as e:
        print(f"Error getting products: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'firebase_status': 'connected',
        'version': '1.0.0'
    })

@app.route('/api/test-products', methods=['GET'])
def test_products():
    """Test products endpoint without authentication"""
    try:
        print("Testing products endpoint...")
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
        
        print(f"Retrieved {len(products)} products for test")
        return jsonify({
            'status': 'success',
            'message': f'Found {len(products)} products',
            'products_count': len(products),
            'sample_products': products[:3]  # Return first 3 products
        })
        
    except Exception as e:
        print(f"Error in test products: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    print("📊 Firebase connection: ✅ Connected")
    print("🔐 Admin credentials: admin / India@123")
    print("🌐 Dashboard: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
