set -e

echo "Starting AWS EC2 deployment setup..."

echo "Updating system packages..."
sudo yum update -y

echo "Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "Installing Git..."
sudo yum install -y git

echo "Creating application directory..."
mkdir -p /home/ec2-user/jwt-auth-api
cd /home/ec2-user/jwt-auth-api

echo "Cloning repository..."

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

echo "Building and starting Docker containers..."
docker-compose up -d --build

echo "Waiting for services to start..."
sleep 30

echo "Running database migrations..."
docker-compose exec web python manage.py migrate

echo "Creating superuser..."
docker-compose exec web python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

echo "Showing running containers..."
docker-compose ps

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