# Production Deployment Guide

## Overview
This guide covers deploying the Management System to production environments with security, scalability, and monitoring considerations.

## Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- Redis server (for rate limiting)
- SSL certificates (for HTTPS)
- Domain name and DNS configuration

## Environment Setup

### 1. Environment Variables
Create a `.env.production` file with the following variables:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-change-this-in-production

# User Authentication (generate hashes using generate_password_hashes.py)
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=pbkdf2:sha256:600000$your-hash-here
USER1_USERNAME=user1
USER1_PASSWORD_HASH=pbkdf2:sha256:600000$your-hash-here

# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour-private-key-here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id

# Redis Configuration (for rate limiting)
REDIS_URL=redis://localhost:6379

# Background Processing
BACKGROUND_PROCESSOR_ENABLED=true
BACKGROUND_PROCESSOR_INTERVAL=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# CORS (comma-separated list of allowed origins)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Rate Limiting
RATELIMIT_DEFAULT=1000 per hour
```

### 2. Generate Password Hashes
Run the password generator script to create secure password hashes:

```bash
python generate_password_hashes.py
```

## Deployment Options

### Option 1: Docker Deployment (Recommended)

1. **Build and Run with Docker Compose:**
```bash
# Copy environment variables
cp .env.production .env

# Build and start services
docker-compose up -d

# Check logs
docker-compose logs -f easybill-admin
```

2. **Health Check:**
```bash
curl http://localhost/health
```

### Option 2: Manual Deployment

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create Directories:**
```bash
mkdir -p logs uploads
```

3. **Run with Gunicorn:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app:app
```

### Option 3: Render Deployment

1. **Connect GitHub Repository:**
   - Link your GitHub repository to Render
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`

2. **Environment Variables:**
   - Add all required environment variables in Render dashboard
   - Ensure `FLASK_ENV=production`

3. **Custom Domain (Optional):**
   - Add your domain in Render dashboard
   - Update DNS records to point to Render

## Security Configuration

### 1. SSL/TLS Setup
- Obtain SSL certificates from Let's Encrypt or your certificate provider
- Configure nginx to use HTTPS
- Enable HSTS headers
- Redirect HTTP to HTTPS

### 2. Firewall Configuration
```bash
# Allow only necessary ports
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable
```

### 3. Database Security
- Use Firebase security rules
- Enable audit logging
- Regular security updates

### 4. Application Security
- Change default passwords
- Enable rate limiting
- Use strong secret keys
- Regular security audits

## Monitoring and Logging

### 1. Application Logs
- Logs are stored in `logs/app.log`
- Rotating logs (10MB max, 10 backups)
- Different log levels: DEBUG, INFO, WARNING, ERROR

### 2. Health Monitoring
- Health check endpoint: `/health`
- Monitor Firebase connection status
- Track background processor status

### 3. Performance Monitoring
- Monitor response times
- Track error rates
- Monitor resource usage

## Backup and Recovery

### 1. Data Backup
- Firebase data is automatically backed up
- Export critical data regularly
- Test restore procedures

### 2. Application Backup
- Version control with Git
- Regular deployments
- Rollback procedures

## Scaling Considerations

### 1. Horizontal Scaling
- Use load balancer (nginx)
- Multiple application instances
- Shared Redis for rate limiting

### 2. Vertical Scaling
- Increase server resources
- Optimize database queries
- Cache frequently accessed data

## Maintenance

### 1. Regular Updates
- Update dependencies regularly
- Security patches
- Monitor for vulnerabilities

### 2. Performance Optimization
- Database query optimization
- Caching strategies
- CDN for static assets

## Troubleshooting

### Common Issues:

1. **Firebase Connection Issues:**
   - Check environment variables
   - Verify service account permissions
   - Check network connectivity

2. **Authentication Problems:**
   - Verify password hashes
   - Check user credentials
   - Review login logs

3. **Performance Issues:**
   - Monitor resource usage
   - Check database performance
   - Review application logs

### Log Locations:
- Application logs: `logs/app.log`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`

## Support

For issues and questions:
1. Check application logs
2. Review this documentation
3. Check GitHub issues
4. Contact system administrator

## Security Checklist

- [ ] Strong secret keys configured
- [ ] Password hashes generated securely
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Firewall rules applied
- [ ] Regular security updates
- [ ] Monitoring enabled
- [ ] Backup procedures tested
- [ ] Access logs reviewed
- [ ] Security audit completed
