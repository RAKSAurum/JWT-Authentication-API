# Step-by-Step Deployment Guide

## Phase 1: Local Development & Testing

### Step 1: Set Up Local Environment

1. **Create your project directory**
   ```bash
   mkdir jwt-auth-api
   cd jwt-auth-api
   ```

2. **Copy all the generated files to your project directory**
   - Copy all files from the generated project structure
   - Ensure directory structure matches the layout above

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your settings
   ```

4. **Build and run locally**
   ```bash
   docker compose up -d --build
   ```

5. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create admin user**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Test the API**
   ```bash
   chmod +x test_api.sh
   ./test_api.sh
   ```

### Step 2: Version Control

1. **Initialize Git repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: JWT Authentication API"
   ```

2. **Create GitHub repository**
   - Go to GitHub and create a new repository
   - Push your code:
   ```bash
   git remote add origin https://github.com/your-username/jwt-auth-api.git
   git push -u origin main
   ```

## Phase 2: AWS EC2 Deployment

### Step 3: Launch EC2 Instance

1. **Access AWS Console**
   - Log in to AWS Management Console
   - Navigate to EC2 Dashboard

2. **Launch Instance**
   - Click "Launch Instance"
   - **Name**: jwt-auth-api-server
   - **AMI**: Amazon Linux 2 (free tier eligible)
   - **Instance Type**: t2.micro (free tier)
   - **Key Pair**: Create new or use existing
   - **Security Group**: Create new with these rules:
     - SSH (22) - Your IP
     - HTTP (80) - Anywhere
     - Custom TCP (8000) - Anywhere
   - **Storage**: 8 GB (default)
   - Click "Launch Instance"

3. **Connect to Instance**
   ```bash
   chmod 400 your-key.pem
   ssh -i your-key.pem ec2-user@your-ec2-public-ip
   ```

### Step 4: Deploy on EC2

1. **Clone your repository**
   ```bash
   git clone https://github.com/your-username/jwt-auth-api.git
   cd jwt-auth-api
   ```

2. **Run deployment script**
   ```bash
   chmod +x aws_deploy.sh
   ./aws_deploy.sh
   ```

3. **Configure environment**
   ```bash
   nano .env
   # Update ALLOWED_HOSTS with your EC2 public IP
   # Update SECRET_KEY and JWT_SECRET_KEY
   ```

4. **Restart services**
   ```bash
   docker-compose restart
   ```

### Step 5: Test Production Deployment

1. **Test API endpoints**
   ```bash
   # Update test script with your EC2 IP
   sed -i 's/localhost/your-ec2-public-ip/g' test_api.sh
   ./test_api.sh
   ```

2. **Access admin panel**
   ```
   http://your-ec2-public-ip:8000/admin/
   ```

## Phase 3: Submit Your Assignment

### Step 6: Prepare Submission

1. **Document your deployment**
   - Update README.md with your EC2 public IP
   - Include sample credentials
   - Document any changes made

2. **Create submission email**
   ```
   Subject: JWT Authentication API - Technical Assignment Submission

   Dear Hiring Team,

   I have successfully completed the JWT Authentication API technical assignment. 

   🔗 GitHub Repository: https://github.com/your-username/jwt-auth-api
   🌐 Live API URL: http://your-ec2-public-ip:8000

   📋 API Endpoints:
   - POST /api/auth/login/
   - POST /api/auth/verify/
   - GET /api/auth/validate/

   🔐 Sample Credentials:
   - Username: admin
   - Password: admin123

   🛠️ Technical Stack:
   - Django + Django REST Framework
   - JWT Authentication (PyJWT)
   - Docker + Docker Compose
   - PostgreSQL Database
   - AWS EC2 Deployment

   📝 Testing:
   You can test the API using the provided Postman collection or the test script.

   Best regards,
   [Your Name]
   ```

3. **Send submission to**: vismay@sharpstakes.ca

### Step 7: Post-Deployment Checklist

- [ ] API responds to all three endpoints
- [ ] JWT tokens are generated and validated correctly
- [ ] Docker containers are running properly
- [ ] Database migrations completed
- [ ] Admin user created and accessible
- [ ] Security group configured correctly
- [ ] GitHub repository is public and complete
- [ ] Documentation is clear and complete
- [ ] Submission email sent

## Troubleshooting Common Issues

### Docker Issues
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs web
docker-compose logs db

# Restart services
docker-compose restart
```

### Database Issues
```bash
# Reset database
docker-compose exec web python manage.py migrate --fake-initial
docker-compose exec web python manage.py migrate
```

### Permission Issues
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

### API Issues
```bash
# Check if API is accessible
curl http://localhost:8000/admin/
curl http://your-ec2-ip:8000/admin/
```

## Security Considerations

1. **Change default credentials**
   - Update SECRET_KEY and JWT_SECRET_KEY
   - Change admin password
   - Use strong database passwords

2. **Network security**
   - Configure proper security groups
   - Use HTTPS in production
   - Restrict SSH access to your IP

3. **Environment variables**
   - Never commit .env files
   - Use AWS Secrets Manager for production
   - Rotate secrets regularly

## Performance Optimization

1. **For production use**
   - Use AWS RDS for database
   - Implement Redis for caching
   - Use AWS ECS or EKS for scaling
   - Set up load balancer

2. **Monitoring**
   - Set up CloudWatch logs
   - Monitor API response times
   - Track error rates

Remember: This is a technical test environment. For production, additional security measures and optimizations would be needed.