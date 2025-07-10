# JWT Authentication API

A secure, production-ready JWT authentication API built with Django REST Framework and PostgreSQL, containerized with Docker for easy deployment.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **RESTful API**: Clean, well-documented endpoints following REST principles
- **Docker Support**: Fully containerized application with Docker Compose
- **PostgreSQL Database**: Robust database backend with health checks
- **Comprehensive Testing**: 100+ test cases covering security, performance, and edge cases
- **Production Ready**: Configured for AWS EC2 deployment with proper security measures

## 📋 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login/` | User login with credentials | No |
| POST | `/api/auth/verify/` | Verify JWT token validity | No |
| GET | `/api/auth/validate/` | Validate token and get user info | Yes |

### Sample Responses

**Login Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires": "2025-07-08T10:30:00Z"
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
  "expires": "2025-07-08T10:30:00Z"
}
```

## 🛠️ Technology Stack

- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL 13
- **Authentication**: JWT (PyJWT)
- **Containerization**: Docker & Docker Compose
- **Testing**: Django Test Framework with comprehensive test suite
- **Deployment**: AWS EC2 with automated deployment scripts

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- Python 3.11+ (for local development)

### 1. Clone the Repository

```bash
git clone https://github.com/RAKSAurum/JWT-Authentication-API
cd jwt-auth-api
```

### 2. Environment Setup

Create a `.env` file:

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your settings (Optional)
nano .env
```

Required environment variables:
```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1,your-domain.com
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=3600
DB_NAME=jwt_auth_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### 3. Start the Application

```bash
# Make the quick start script executable
chmod +x quick_start.sh

# Run the setup script
./quick_start.sh
```

This will:
- Build and start Docker containers
- Run database migrations
- Create a superuser account
- Test the API endpoints

### 4. Access the API

- **API Base URL**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin/`
- **Default Credentials**: `admin` / `admin123`

## 🧪 Testing the API

### Using the Test Script

```bash
chmod +x test_api.sh
./test_api.sh
```

### Manual Testing with cURL

**1. Login to get a token:**
```bash
curl -X POST "http://localhost:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**2. Verify the token:**
```bash
curl -X POST "http://localhost:8000/api/auth/verify/" \
  -H "Content-Type: application/json" \
  -d '{"token":"YOUR_TOKEN_HERE"}'
```

**3. Validate with Authorization header:**
```bash
curl -X GET "http://localhost:8000/api/auth/validate/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🏗️ Project Structure

```
jwt-auth-api/
├── auth_app/                    # Main authentication application
│   ├── management/
│   │   └── commands/
│   │       └── wait_for_db.py   # Database readiness check
│   ├── authentication.py       # Custom JWT authentication class
│   ├── models.py               # Database models
│   ├── views.py                # API endpoints
│   ├── urls.py                 # URL routing
│   ├── utils.py                # JWT utility functions
│   └── tests.py                # Comprehensive test suite
├── jwt_auth_api/               # Django project settings
│   ├── settings.py             # Project configuration
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI application
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── quick_start.sh             # Quick setup script
├── test_api.sh                # API testing script
├── aws_deploy.sh              # AWS deployment script
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

# Run development server
python manage.py runserver
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
python manage.py test --verbosity=2

# Run specific test class
python manage.py test auth_app.tests.LoginEndpointTests
```

## 🚀 Deployment

### AWS EC2 Deployment

1. **Launch EC2 Instance**:
   - AMI: Amazon Linux 2
   - Instance Type: t2.micro (free tier eligible)
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22), and Custom TCP (8000)

2. **Deploy using the script**:
   ```bash
   chmod +x aws_deploy.sh
   ./aws_deploy.sh
   ```

3. **Update environment variables**:
   ```bash
   # Edit .env file with your production settings
   nano .env
   
   # Restart containers
   docker-compose down
   docker-compose up -d
   ```

### Docker Commands

```bash
# Build and start services
docker-compose up -d --build

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

## 🔒 Security Features

- **JWT Token Security**: Configurable expiration, unique JTI (JWT ID)
- **SQL Injection Protection**: Django ORM with parameterized queries
- **XSS Protection**: Proper response sanitization
- **CSRF Protection**: Django's built-in CSRF middleware
- **Input Validation**: Comprehensive request validation
- **Rate Limiting Ready**: Structured for easy rate limiting implementation

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
  "error": "Error message description",
  "details": "Additional error details (if applicable)"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing/invalid parameters)
- `401`: Unauthorized (invalid credentials/token)
- `405`: Method Not Allowed
- `500`: Internal Server Error

## 🧪 Testing

The project includes comprehensive test coverage:
- **Unit Tests**: 40+ test methods
- **Integration Tests**: Complete authentication flow testing
- **Security Tests**: SQL injection, XSS, token tampering
- **Performance Tests**: Concurrent operations testing
- **Edge Cases**: Error handling, malformed requests

Run tests with:
```bash
python manage.py test auth_app.tests
```

## 📈 Performance

- **Database**: PostgreSQL with connection pooling
- **Caching**: Ready for Redis integration
- **Scalability**: Stateless JWT design for horizontal scaling
- **Monitoring**: Structured logging for production monitoring

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

---
**Live API URL**: `http://your-ec2-public-ip:8000`
**Sample Credentials**: `admin` / `admin123`