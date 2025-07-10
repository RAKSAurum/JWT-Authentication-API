#!/bin/bash

# AWS EC2 Deployment Script for JWT Authentication API
# This script sets up Docker and deploys the application on EC2

set -e

echo "Starting AWS EC2 deployment setup..."

# Update system packages
echo "Updating system packages..."
sudo yum update -y

# Install Docker
echo "Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install Git
echo "Installing Git..."
sudo yum install -y git

# Create application directory
echo "Creating application directory..."
mkdir -p /home/ec2-user/jwt-auth-api
cd /home/ec2-user/jwt-auth-api

# Clone repository (replace with your actual repository)
echo "Cloning repository..."
# git clone https://github.com/your-username/jwt-auth-api.git .

# Create environment file
echo "Creating environment file..."
cat > .env << EOL
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1,your-ec2-public-ip-here

JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=3600

DB_NAME=jwt_auth_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
EOL

# Build and start containers
echo "Building and starting Docker containers..."
docker-compose up -d --build

# Wait for services to start
echo "Waiting for services to start..."
sleep 30

# Run migrations
echo "Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
docker-compose exec web python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

# Show running containers
echo "Showing running containers..."
docker-compose ps

# Show logs
echo "Showing recent logs..."
docker-compose logs --tail=50

echo "Deployment completed successfully!"
echo "Your API should be accessible at: http://your-ec2-public-ip:8000"
echo "API endpoints:"
echo "- POST /api/auth/login/"
echo "- POST /api/auth/verify/"
echo "- GET /api/auth/validate/"
echo ""
echo "Sample credentials:"
echo "Username: admin"
echo "Password: admin123"