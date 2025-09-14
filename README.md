# POS Management Dashboard

A minimal Flask-based dashboard to manage your POS Flutter app with Firebase integration.

## Features

- **Dashboard**: Overview of products, categories, orders, and sales
- **Products Management**: Add, edit, delete products with stock tracking
- **Categories Management**: Organize products by categories
- **Orders Management**: View recent orders and sales
- **Low Stock Alerts**: Automatic alerts for products running low
- **Firebase Integration**: Real-time data sync with your Flutter app

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have `firebase-service-account.json` in the project root

## Running the Application

```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`

## Firebase Collections

The dashboard uses these Firebase collections:
- `products`: Product inventory
- `categories`: Product categories
- `orders`: Sales orders from your Flutter app

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create new category

### Orders
- `GET /api/orders` - Get recent orders

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

## Project Structure

```
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Dashboard template
├── requirements.txt       # Python dependencies
├── firebase-service-account.json  # Firebase credentials
└── README.md
```

## Technologies Used

- **Backend**: Flask, Firebase Firestore
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: Firebase Firestore