# JWT Authentication API

A Django REST Framework API implementing JWT authentication with Docker deployment support for AWS EC2.

## Features

- JWT token-based authentication
- Three main endpoints: login, verify, and validate
- Docker containerization with Docker Compose
- AWS EC2 deployment ready
- PostgreSQL database support
- Production-ready security settings

## API Endpoints

### 1. Login
- **URL**: `POST /api/auth/login/`
- **Body**: `{"username": "user", "password": "pass"}`
- **Response**: `{"token": "jwt_token", "expires": "2025-07-08T10:30:00Z"}`

### 2. Verify Token
- **URL**: `POST /api/auth/verify/`
- **Body**: `{"token": "jwt_token"}`
- **Response**: `{"valid": true, "message": "Token is valid"}`

### 3. Validate Token
- **URL**: `GET /api/auth/validate/`
- **Headers**: `Authorization: Bearer jwt_token`
- **Response**: `{"valid": true, "user": "username", "expires": "2025-07-08T10:30:00Z"}`

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd jwt-auth-api
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Update environment variables**
   Edit `.env` file with your settings:
   ```env
   SECRET_KEY=your-super-secret-key
   DEBUG=True
   JWT_SECRET_KEY=your-jwt-secret-key
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up -d --build
   ```

5. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Test the API**
   ```bash
   chmod +x test_api.sh
   ./test_api.sh
   ```

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Choose Amazon Linux 2 AMI
   - Instance type: t2.micro (free tier)
   - Security group: Allow SSH (22), HTTP (80), and custom port (8000)

2. **Connect to EC2**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-public-ip
   ```

3. **Run deployment script**
   ```bash
   chmod +x aws_deploy.sh
   ./aws_deploy.sh
   ```

4. **Update environment variables**
   ```bash
   nano .env
   # Update ALLOWED_HOSTS with your EC2 public IP
   ```

5. **Restart services**
   ```bash
   docker-compose restart
   ```

## Sample API Usage

### Using curl

```bash
# Login
curl -X POST http://your-server:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Verify token
curl -X POST http://your-server:8000/api/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{"token":"your-jwt-token"}'

# Validate token
curl -X GET http://your-server:8000/api/auth/validate/ \
  -H "Authorization: Bearer your-jwt-token"
```

### Using Python requests

```python
import requests

# Login
response = requests.post('http://your-server:8000/api/auth/login/', {
    'username': 'admin',
    'password': 'admin123'
})
token = response.json()['token']

# Verify token
response = requests.post('http://your-server:8000/api/auth/verify/', {
    'token': token
})
print(response.json())

# Validate token
response = requests.get('http://your-server:8000/api/auth/validate/', 
    headers={'Authorization': f'Bearer {token}'}
)
print(response.json())
```

## Project Structure

```
jwt-auth-api/
├── authentication/           # Django app for JWT authentication
│   ├── authentication.py   # Custom JWT authentication class
│   ├── utils.py            # JWT utility functions
│   ├── views.py            # API views
│   └── urls.py             # URL patterns
├── jwt_auth_api/           # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── aws_deploy.sh          # AWS deployment script
├── test_api.sh            # API testing script
└── README.md              # This file
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `JWT_SECRET_KEY` | JWT signing key | Same as SECRET_KEY |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_DELTA` | Token expiry (seconds) | `3600` |
| `DB_NAME` | Database name | `jwt_auth_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `DB_HOST` | Database host | `db` |
| `DB_PORT` | Database port | `5432` |

### Security Notes

- Change default SECRET_KEY and JWT_SECRET_KEY in production
- Use strong passwords for database and admin users
- Configure proper firewall rules on AWS EC2
- Enable HTTPS in production
- Regularly rotate JWT secrets

## Troubleshooting

### Common Issues

1. **Docker permission denied**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Port already in use**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Database connection errors**
   ```bash
   docker-compose logs db
   docker-compose restart db
   ```

4. **Migration issues**
   ```bash
   docker-compose exec web python manage.py migrate --fake-initial
   ```

### Health Check

```bash
# Check if services are running
docker-compose ps

# Check logs
docker-compose logs web
docker-compose logs db

# Test API health
curl http://localhost:8000/admin/
```

## Sample Credentials

**Default Admin User:**
- Username: `admin`
- Password: `admin123`

**Note**: Change these credentials in production!

## Testing

Run the test script to verify all endpoints:

```bash
chmod +x test_api.sh
./test_api.sh
```

## Deployment Checklist

- [ ] EC2 instance launched with proper security groups
- [ ] Docker and Docker Compose installed
- [ ] Application code deployed
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Superuser created
- [ ] API endpoints tested
- [ ] Security settings reviewed
- [ ] Backup strategy implemented

## Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.

## License

This project is licensed under the MIT License.