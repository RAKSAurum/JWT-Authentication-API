#!/bin/bash

# Quick Start Script for JWT Authentication API
# This script sets up the project locally for development

set -e

echo "🚀 Starting JWT Authentication API setup..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file from example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your settings."
fi

# Build and start containers
echo "🔨 Building and starting Docker containers..."
docker-compose up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
docker-compose exec web python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('ℹ️  Superuser already exists')
EOF

# Show status
echo "📊 Container status:"
docker-compose ps

# Test the API
echo "🧪 Testing API endpoints..."
sleep 5

# Test login endpoint
echo "Testing login endpoint..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/auth/login/"   -H "Content-Type: application/json"   -d '{"username":"admin","password":"admin123"}' || echo "Error")

if echo "$LOGIN_RESPONSE" | grep -q "token"; then
    echo "✅ Login endpoint working"
else
    echo "❌ Login endpoint failed"
    echo "Response: $LOGIN_RESPONSE"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Your JWT Authentication API is now running:"
echo "🌐 API Base URL: http://localhost:8000"
echo "👨‍💼 Admin Panel: http://localhost:8000/admin/"
echo "📋 API Endpoints:"
echo "   - POST /api/auth/login/"
echo "   - POST /api/auth/verify/"
echo "   - GET /api/auth/validate/"
echo ""
echo "🔐 Sample Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🧪 To test the API:"
echo "   chmod +x test_api.sh && ./test_api.sh"
echo ""
echo "📖 View logs:"
echo "   docker-compose logs -f web"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"