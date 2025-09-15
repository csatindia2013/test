#!/bin/bash
# Production Deployment Script for EasyBill Admin Dashboard

set -e  # Exit on any error

echo "🚀 Starting EasyBill Admin Dashboard Production Deployment..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p backups

# Set proper permissions
echo "🔐 Setting proper permissions..."
chmod 755 logs
chmod 755 uploads
chmod 755 backups

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️ Warning: .env file not found. Please create one based on production.env.example"
    echo "   Copy production.env.example to .env and update the values"
fi

# Check if Firebase service account file exists
if [ ! -f "firebase-service-account.json" ]; then
    echo "⚠️ Warning: firebase-service-account.json not found."
    echo "   Please ensure Firebase credentials are properly configured"
fi

# Run database migrations/initialization (if needed)
echo "🗄️ Checking database connection..."
python -c "
import sys
sys.path.append('.')
from app import init_firebase_global
if init_firebase_global():
    print('✅ Database connection successful')
else:
    print('❌ Database connection failed')
    sys.exit(1)
"

# Test the application
echo "🧪 Testing application..."
python -c "
import sys
sys.path.append('.')
from app import app
with app.test_client() as client:
    response = client.get('/health')
    if response.status_code == 200:
        print('✅ Application health check passed')
    else:
        print('❌ Application health check failed')
        sys.exit(1)
"

echo "✅ Production deployment preparation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your .env file with production values"
echo "2. Ensure Firebase credentials are properly set up"
echo "3. Start the application with: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:application"
echo "4. Or use: python app.py (for development)"
echo ""
echo "🔍 Monitoring:"
echo "- Check logs in: logs/app.log"
echo "- Check errors in: logs/error.log"
echo "- Health check: http://your-domain/health"
echo ""
echo "🛡️ Security reminders:"
echo "- Change default passwords"
echo "- Use HTTPS in production"
echo "- Configure proper CORS origins"
echo "- Set up Redis for rate limiting"
