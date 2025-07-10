# JWT Authentication API

A secure, production-ready JWT authentication API built with Django REST Framework and PostgreSQL, containerized with Docker for easy deployment on AWS EC2.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **RESTful API**: Clean, well-documented endpoints following REST principles
- **Docker Support**: Fully containerized application with Docker Compose
- **PostgreSQL Database**: Robust database backend with health checks
- **Comprehensive Testing**: 41 test cases covering security, performance, and edge cases
- **Production Ready**: Configured for AWS EC2 deployment with proper security measures
- **Static File Serving**: WhiteNoise integration for production static file handling
- **Postman Collection**: Ready-to-use Postman collection for API testing

## 📋 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
| :-- | :-- | :-- | :-- |
| POST | `/api/auth/login/` | User login with credentials | No |
| POST | `/api/auth/verify/` | Verify JWT token validity | No |
| GET | `/api/auth/validate/` | Validate token and get user info | Yes |
| GET | `/admin/` | Django admin interface | Yes |

### Sample Responses

**Login Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires": "2025-07-11T04:16:00.000Z"
}
```

**Verify Response:**
```json
{
  "valid": true,
  "message": "Token is valid"
}
```

**Validate Response:**
```json
{
  "valid": true,
  "user": "admin",
  "expires": "2025-07-11T04:16:00.000Z"
}
```

## 🛠️ Technology Stack
- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL 13
- **Authentication**: JWT (PyJWT)
- **Static Files**: WhiteNoise for production static file serving
- **Containerization**: Docker \& Docker Compose
- **Testing**: Django Test Framework with comprehensive test suite
- **Deployment**: AWS EC2 with automated deployment scripts

## 🚀 Quick Start

### Prerequisites
- Docker \& Docker Compose
- Git
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/RAKSAurum/JWT-Authentication-API
cd JWT-Authentication-API
```

### 2. Environment Setup

Create a `.env` file:
```bash
# Copy the example environment file
cp .env.example .env

# Or create a new .env file
nano .env
```

Required environment variables:
```env
# Django Configuration
SECRET_KEY=your-secret-django-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DB_NAME=jwt_auth_db
DB_USER=jwt_user
DB_PASSWORD=secure_password_123
DB_HOST=db
DB_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_EXPIRATION_DELTA=3600
```

### 3. Start the Application
```bash
# Build and start containers
docker-compose up --build -d

# Run database migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

This will:
- Build and start Docker containers
- Run database migrations
- Create a superuser account
- Test the API endpoints

### 4. Access the API
- **API Base URL**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin/`
- **Default Credentials**: Create during setup

## ☁️ AWS EC2 Deployment

### Prerequisites for AWS Deployment

- AWS Account with Free Tier access
- Basic understanding of AWS EC2
- SSH key pair for secure access

### Step 1: Launch EC2 Instance
1. **Log into AWS Console**
    - Navigate to EC2 service
    - Click "Launch Instance"

2. **Configure Instance**
```
Name: django-jwt-api
AMI: Ubuntu Server 22.04 LTS (Free tier eligible)
Instance Type: t2.micro (Free tier eligible)
Key Pair: Create new or use existing
```

3. **Security Group Configuration**
```
Inbound Rules:
- SSH (Port 22): My IP
- HTTP (Port 80): Anywhere (0.0.0.0/0)
- HTTPS (Port 443): Anywhere (0.0.0.0/0)
- Custom TCP (Port 8000): Anywhere (0.0.0.0/0)
```

4. **Storage Configuration**
```
Storage: 8 GiB gp3 (Free tier: up to 30 GiB)
```


### Step 2: Connect to EC2 Instance
```bash
# Make key file secure (Linux/Mac)
chmod 400 your-key-pair.pem

# Connect to instance
ssh -i your-key-pair.pem ubuntu@YOUR_PUBLIC_IP
```


### Step 3: Server Setup and Dependencies
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install -y git
```


### Step 4: Deploy Application
```bash
# Create application directory
mkdir -p /home/ubuntu/jwt_auth_api
cd /home/ubuntu/jwt_auth_api

# Clone your repository
git clone https://github.com/RAKSAurum/JWT-Authentication-API.git
cd JWT-Authentication-API

# Create environment file
nano .env
```

**Add your production environment variables:**
```env
# Django Configuration
SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,YOUR_EC2_PUBLIC_IP

# Database Configuration
DB_NAME=jwt_auth_db
DB_USER=jwt_user
DB_PASSWORD=secure_password_123
DB_HOST=db
DB_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=your-generated-jwt-secret-key
JWT_EXPIRATION_DELTA=3600
```

**Generate Secure Keys** 
(For "your-generated-secret-key" & "your-generated-jwt-secret-key")
```bash
# Generate Django SECRET_KEY
openssl rand -base64 32

# Generate JWT SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Step 5: Start Application
```bash
# Build and start containers
docker-compose up --build -d

# Run database migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Step 7: Verify Deployment

```bash
# Check container status
docker-compose ps

# Test API endpoint
curl -I http://YOUR_PUBLIC_IP:8000/

# Test admin interface
curl -I http://YOUR_PUBLIC_IP:8000/admin/
```

### AWS Free Tier Considerations

**Staying Within Free Tier:**
- **EC2 Usage**: 750 hours/month (24/7 for one t2.micro instance)
- **Storage**: Keep under 30 GB total
- **Data Transfer**: Monitor outbound data transfer (15 GB/month free)

**Set Up Billing Alerts:**
1. Go to AWS Billing Dashboard
2. Enable "Receive Free Tier Usage Alerts"
3. Set up CloudWatch billing alarms for \$1, \$5, \$10 thresholds

## 🧪 Testing the API

### Running Django Test Suite
```bash
# Run all 41 tests
docker-compose exec web python manage.py test auth_app

# Run specific test classes
docker-compose exec web python manage.py test auth_app.tests.LoginEndpointTests
```


### 📮 Postman Collection

A Postman collection is included for easy API testing:
**File**: `JWT_Auth_API.postman_collection.json`

**Environment Variables**:
- `base_url`: `http://your-server-ip:8000`
- `jwt_token`: Auto-populated after login

**Import Instructions**:
1. Open Postman
2. Click "Import" button
3. Select the `JWT_Auth_API.postman_collection.json` file
4. Update the `base_url` variable with your server IP

### Manual Testing with cURL

**1. Login to get a token:**
```bash
curl -X POST "http://YOUR_SERVER_IP:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
}'
```

**2. Verify the token:**
```bash
curl -X POST "http://YOUR_SERVER_IP:8000/api/auth/verify/" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_TOKEN_HERE"
}'
```

**3. Validate with Authorization header:**
```bash
curl -X GET "http://YOUR_SERVER_IP:8000/api/auth/validate/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```


## 🏗️ Project Structure
```
JWT-Authentication-API/
├── auth_app/                    # Main authentication application
│   ├── management/
│   │   └── commands/
│   │       └── wait_for_db.py   # Database readiness check
│   ├── authentication.py       # Custom JWT authentication class
│   ├── models.py               # Database models
│   ├── views.py                # API endpoints
│   ├── urls.py                 # URL routing
│   ├── utils.py                # JWT utility functions
│   └── tests.py                # Comprehensive test suite (41 tests)
├── jwt_auth_api/               # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # Main URL configuration with static files
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── staticfiles/                # Collected static files
│   ├── admin/                  # Django admin static files
│   └── rest_framework/         # DRF static files
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── JWT_Auth_API.postman_collection.json  # Postman collection
├── quick_start.sh             # Quick setup script
├── test_api.sh                # API testing script
├── aws_deploy.sh              # AWS deployment script
├── manage.py                  # Django management script
└── README.md                  # This file
```


## 🔧 Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```


### Running Tests
```bash
# Run all tests
python manage.py test auth_app

# Run with coverage
python manage.py test auth_app --verbosity=2

# Run specific test class
python manage.py test auth_app.tests.LoginEndpointTests

# Run tests in parallel
python manage.py test auth_app --parallel
```


## 🔧 Environment Variables

### Required Environment Variables

| Variable | Description | Example |
| :-- | :-- | :-- |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1,your-ip` |
| `DB_NAME` | Database name | `jwt_auth_db` |
| `DB_USER` | Database user | `jwt_user` |
| `DB_PASSWORD` | Database password | `secure_password` |
| `DB_HOST` | Database host | `db` |
| `DB_PORT` | Database port | `5432` |
| `JWT_SECRET_KEY` | JWT signing key | `your-jwt-secret` |
| `JWT_EXPIRATION_DELTA` | Token expiration (seconds) | `3600` |

## 🚀 Deployment Commands

### Docker Commands
```bash
# Build and start services
docker-compose up -d --build

# View logs
docker-compose logs -f web
docker-compose logs -f db

# Stop services
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Restart specific service
docker-compose restart web
```


### Maintenance Commands
```bash
# Update application
git pull origin main
docker-compose build
docker-compose up -d

# Database backup
docker-compose exec db pg_dump -U jwt_user jwt_auth_db > backup.sql

# View container stats
docker stats

# Clean up Docker
docker system prune -a
```


## 🔒 Security Features
- **JWT Token Security**: Configurable expiration, unique JTI (JWT ID)
- **SQL Injection Protection**: Django ORM with parameterized queries
- **XSS Protection**: Proper response sanitization
- **CSRF Protection**: Django's built-in CSRF middleware
- **Input Validation**: Comprehensive request validation
- **Static File Security**: WhiteNoise with secure headers
- **Production Settings**: DEBUG=False, secure middleware configuration


## 📊 API Documentation

### Authentication Flow
1. **Login**: Send credentials to `/api/auth/login/`
2. **Receive Token**: Get JWT token and expiration time
3. **Use Token**: Include in Authorization header as `Bearer <token>`
4. **Verify/Validate**: Use verify or validate endpoints as needed

### Error Responses

All endpoints return consistent error formats:
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing/invalid parameters)
- `401`: Unauthorized (invalid credentials/token)
- `405`: Method Not Allowed
- `500`: Internal Server Error


## 🧪 Testing

The project includes comprehensive test coverage with 41 test cases:
### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Complete authentication flow testing
- **Security Tests**: SQL injection, XSS, token tampering
- **Performance Tests**: Concurrent operations testing
- **Edge Cases**: Error handling, malformed requests

### Test Classes
- `LoginEndpointTests`: Login functionality testing
- `VerifyTokenEndpointTests`: Token verification testing
- `ValidateTokenEndpointTests`: Token validation testing
- `JWTUtilityTests`: JWT utility function testing
- `IntegrationTests`: End-to-end workflow testing
- `SecurityTests`: Security vulnerability testing
- `ErrorHandlingTests`: Error scenario testing
- `PerformanceTests`: Performance and concurrency testing


## 📈 Performance
- **Database**: PostgreSQL with connection pooling
- **Static Files**: WhiteNoise with compression and caching
- **Scalability**: Stateless JWT design for horizontal scaling
- **Monitoring**: Structured logging for production monitoring
- **Caching**: Ready for Redis integration


## 🆘 Troubleshooting

### Common Issues

**Container Connection Issues:**
```bash
# Check container status
docker-compose ps

# Restart containers
docker-compose restart

# View logs
docker-compose logs web
```

**Static Files Not Loading:**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check WhiteNoise configuration in settings.py
```

**Database Connection Issues:**
```bash
# Check database health
docker-compose exec db pg_isready -U jwt_user

# Restart database
docker-compose restart db
```

**EC2 Instance Issues:**
```bash
# Check security group settings
# Ensure port 8000 is open
# Verify instance is running
# Check public IP address
```


## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

For support and questions:
- **Issues**: Create an issue on GitHub
- **Documentation**: Check the code comments and tests
- **AWS Support**: Refer to AWS documentation for EC2 issues

---

**Live Demo**: Deploy on your own AWS EC2 instance following the guide above
**Test Credentials**: Create during setup process
**API Documentation**: Available at `/admin/` after deployment

---