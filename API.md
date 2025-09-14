# API Documentation

## Overview
This document describes the REST API endpoints for the Management System.

## Base URL
- Development: `http://localhost:5000`
- Production: `https://yourdomain.com`

## Authentication
Most endpoints require authentication. Include session cookies or use the login endpoint to authenticate.

## Rate Limiting
- Login endpoint: 10 requests per minute
- API endpoints: 1000 requests per hour
- File uploads: 16MB maximum

## Endpoints

### Authentication

#### POST /login
Authenticate user and create session.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response (Success):**
```json
{
    "status": "success",
    "message": "Login successful",
    "user": {
        "id": "string",
        "username": "string",
        "role": "string"
    }
}
```

**Response (Error):**
```json
{
    "status": "error",
    "message": "Invalid username or password"
}
```

#### POST /logout
Logout current user and destroy session.

**Response:**
```json
{
    "status": "success",
    "message": "Logged out successfully"
}
```

#### GET /api/auth/status
Check current authentication status.

**Response (Authenticated):**
```json
{
    "status": "success",
    "authenticated": true,
    "user": {
        "id": "string",
        "username": "string",
        "role": "string"
    }
}
```

**Response (Not Authenticated):**
```json
{
    "status": "success",
    "authenticated": false
}
```

### Health Check

#### GET /health
Application health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00.000Z",
    "firebase_status": "connected",
    "version": "1.0.0"
}
```

### Products

#### GET /api/products
Retrieve all products.

**Query Parameters:**
- `search` (optional): Search term for filtering products
- `category` (optional): Filter by category
- `page` (optional): Page number for pagination
- `limit` (optional): Number of items per page

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": "string",
            "name": "string",
            "barcode": "string",
            "category": "string",
            "price": 0.0,
            "imageUrl": "string",
            "useInFirstStart": true,
            "size": "string",
            "unit": "string",
            "scanCount": 0,
            "syncStatus": "string",
            "sortOrder": 0
        }
    ],
    "total": 0,
    "page": 1,
    "limit": 50
}
```

#### POST /api/products
Create a new product.

**Request Body:**
```json
{
    "name": "string",
    "barcode": "string",
    "category": "string",
    "price": 0.0,
    "imageUrl": "string",
    "useInFirstStart": true,
    "size": "string",
    "unit": "string"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Product created successfully",
    "data": {
        "id": "string",
        "name": "string",
        "barcode": "string",
        "category": "string",
        "price": 0.0,
        "imageUrl": "string",
        "useInFirstStart": true,
        "size": "string",
        "unit": "string",
        "scanCount": 0,
        "syncStatus": "pending",
        "sortOrder": 0
    }
}
```

#### PUT /api/products/{id}
Update an existing product.

**Request Body:**
```json
{
    "name": "string",
    "barcode": "string",
    "category": "string",
    "price": 0.0,
    "imageUrl": "string",
    "useInFirstStart": true,
    "size": "string",
    "unit": "string"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Product updated successfully",
    "data": {
        "id": "string",
        "name": "string",
        "barcode": "string",
        "category": "string",
        "price": 0.0,
        "imageUrl": "string",
        "useInFirstStart": true,
        "size": "string",
        "unit": "string",
        "scanCount": 0,
        "syncStatus": "string",
        "sortOrder": 0
    }
}
```

#### DELETE /api/products/{id}
Delete a product.

**Response:**
```json
{
    "status": "success",
    "message": "Product deleted successfully"
}
```

### Categories

#### GET /api/categories
Retrieve all categories.

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": "string",
            "name": "string",
            "description": "string",
            "imageUrl": "string",
            "sortOrder": 0,
            "isActive": true
        }
    ]
}
```

#### POST /api/categories
Create a new category.

**Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "imageUrl": "string",
    "sortOrder": 0,
    "isActive": true
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Category created successfully",
    "data": {
        "id": "string",
        "name": "string",
        "description": "string",
        "imageUrl": "string",
        "sortOrder": 0,
        "isActive": true
    }
}
```

#### PUT /api/categories/{id}
Update an existing category.

**Request Body:**
```json
{
    "name": "string",
    "description": "string",
    "imageUrl": "string",
    "sortOrder": 0,
    "isActive": true
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Category updated successfully",
    "data": {
        "id": "string",
        "name": "string",
        "description": "string",
        "imageUrl": "string",
        "sortOrder": 0,
        "isActive": true
    }
}
```

#### DELETE /api/categories/{id}
Delete a category.

**Response:**
```json
{
    "status": "success",
    "message": "Category deleted successfully"
}
```

### Barcodes

#### GET /api/barcodes
Retrieve all barcodes.

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": "string",
            "barcode": "string",
            "productName": "string",
            "category": "string",
            "price": 0.0,
            "imageUrl": "string",
            "createdAt": "2024-01-01T00:00:00.000Z",
            "status": "string"
        }
    ]
}
```

#### POST /api/barcodes
Create a new barcode entry.

**Request Body:**
```json
{
    "barcode": "string",
    "productName": "string",
    "category": "string",
    "price": 0.0,
    "imageUrl": "string"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Barcode created successfully",
    "data": {
        "id": "string",
        "barcode": "string",
        "productName": "string",
        "category": "string",
        "price": 0.0,
        "imageUrl": "string",
        "createdAt": "2024-01-01T00:00:00.000Z",
        "status": "active"
    }
}
```

### Unfound Barcodes

#### GET /api/unfound-barcodes
Retrieve all unfound barcodes.

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": "string",
            "barcode": "string",
            "createdAt": "2024-01-01T00:00:00.000Z",
            "status": "pending",
            "attempts": 0,
            "lastAttempt": "2024-01-01T00:00:00.000Z"
        }
    ]
}
```

#### DELETE /api/unfound-barcodes/{id}
Delete an unfound barcode.

**Response:**
```json
{
    "status": "success",
    "message": "Unfound barcode deleted successfully"
}
```

### Background Processor

#### GET /api/background-processor/status
Get background processor status.

**Response:**
```json
{
    "status": "success",
    "data": {
        "running": false,
        "last_run": "2024-01-01T00:00:00.000Z",
        "processed_count": 0,
        "success_count": 0,
        "error_count": 0,
        "current_barcode": "string"
    }
}
```

#### POST /api/background-processor/start
Start background processor.

**Response:**
```json
{
    "status": "success",
    "message": "Background processor started"
}
```

#### POST /api/background-processor/stop
Stop background processor.

**Response:**
```json
{
    "status": "success",
    "message": "Background processor stopped"
}
```

#### GET /api/background-processor/history
Get processed barcodes history.

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "barcode": "string",
            "productName": "string",
            "status": "success",
            "timestamp": "2024-01-01T00:00:00.000Z",
            "result": "string",
            "error": "string"
        }
    ]
}
```

#### POST /api/background-processor/clear-history
Clear processed barcodes history.

**Response:**
```json
{
    "status": "success",
    "message": "History cleared successfully"
}
```

### Recently Added Products

#### GET /api/recently-added-products
Get recently added products.

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": "string",
            "productId": "string",
            "barcode": "string",
            "productName": "string",
            "addedAt": "2024-01-01T00:00:00.000Z",
            "source": "string",
            "originalUnfoundId": "string",
            "verified": false
        }
    ]
}
```

#### POST /api/recently-added-products/verify
Mark products as verified.

**Request Body:**
```json
{
    "productIds": ["string"]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Products verified successfully"
}
```

#### POST /api/recently-added-products/clear
Clear recently added products.

**Request Body:**
```json
{
    "productIds": ["string"]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Products cleared successfully"
}
```

### File Operations

#### POST /api/export/products
Export products to Excel.

**Response:**
```json
{
    "status": "success",
    "message": "Products exported successfully",
    "filename": "products_2024-01-01.xlsx"
}
```

#### POST /api/export/categories
Export categories to Excel.

**Response:**
```json
{
    "status": "success",
    "message": "Categories exported successfully",
    "filename": "categories_2024-01-01.xlsx"
}
```

#### POST /api/export/unfound-barcodes
Export unfound barcodes to Excel.

**Response:**
```json
{
    "status": "success",
    "message": "Unfound barcodes exported successfully",
    "filename": "unfound_barcodes_2024-01-01.xlsx"
}
```

#### POST /api/import/products
Import products from Excel.

**Request Body:** Multipart form data with Excel file.

**Response:**
```json
{
    "status": "success",
    "message": "Products imported successfully",
    "imported_count": 0,
    "errors": []
}
```

#### POST /api/import/categories
Import categories from Excel.

**Request Body:** Multipart form data with Excel file.

**Response:**
```json
{
    "status": "success",
    "message": "Categories imported successfully",
    "imported_count": 0,
    "errors": []
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "error": "Bad request"
}
```

### 401 Unauthorized
```json
{
    "error": "Unauthorized"
}
```

### 403 Forbidden
```json
{
    "error": "Forbidden"
}
```

### 404 Not Found
```json
{
    "error": "Not found"
}
```

### 413 Payload Too Large
```json
{
    "error": "File too large"
}
```

### 429 Too Many Requests
```json
{
    "error": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

### 502 Bad Gateway
```json
{
    "error": "Service temporarily unavailable"
}
```

### 503 Service Unavailable
```json
{
    "error": "Service temporarily unavailable"
}
```

## Examples

### cURL Examples

#### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Get Products
```bash
curl -X GET http://localhost:5000/api/products \
  -H "Cookie: session=your-session-cookie"
```

#### Create Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{
    "name": "Test Product",
    "barcode": "1234567890123",
    "category": "Electronics",
    "price": 99.99,
    "useInFirstStart": true
  }'
```

#### Export Products
```bash
curl -X POST http://localhost:5000/api/export/products \
  -H "Cookie: session=your-session-cookie" \
  -o products.xlsx
```

### JavaScript Examples

#### Login
```javascript
const response = await fetch('/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
});

const data = await response.json();
if (data.status === 'success') {
    console.log('Login successful');
}
```

#### Get Products
```javascript
const response = await fetch('/api/products');
const data = await response.json();
console.log(data.data);
```

#### Create Product
```javascript
const response = await fetch('/api/products', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        name: 'Test Product',
        barcode: '1234567890123',
        category: 'Electronics',
        price: 99.99,
        useInFirstStart: true
    })
});

const data = await response.json();
if (data.status === 'success') {
    console.log('Product created');
}
```

## Notes

- All timestamps are in ISO 8601 format (UTC)
- File uploads are limited to 16MB
- Rate limiting is applied per IP address
- Session cookies are used for authentication
- All endpoints return JSON responses
- Error responses include appropriate HTTP status codes
