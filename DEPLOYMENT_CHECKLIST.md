# Production Deployment Checklist

## Pre-Deployment

### Environment Setup
- [ ] Production server provisioned
- [ ] Domain name configured
- [ ] SSL certificate obtained
- [ ] Firewall rules configured
- [ ] Database server ready (PostgreSQL recommended)

### Application Configuration
- [ ] Update `SECRET_KEY` to strong random value
- [ ] Set `DATABASE_URL` to production database
- [ ] Configure `SMARTSHEET_API_TOKEN` (if using)
- [ ] Set appropriate `FLASK_ENV=production`
- [ ] Disable debug mode
- [ ] Configure logging

### Security Hardening
- [ ] Change all default passwords
- [ ] Enable HTTPS only
- [ ] Configure secure session cookies
- [ ] Implement rate limiting
- [ ] Set up CSRF protection
- [ ] Configure CORS if needed
- [ ] Review file upload restrictions

### Database Setup
- [ ] Install PostgreSQL
- [ ] Create production database
- [ ] Create database user with limited privileges
- [ ] Run migrations
- [ ] Set up automated backups
- [ ] Test backup restoration

## Deployment Steps

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql -y

# Create application user
sudo useradd -m -s /bin/bash volunteer-app
```

### 2. Application Setup
```bash
# Switch to app user
sudo su - volunteer-app

# Clone/copy application
cd /home/volunteer-app
# Upload your application files here

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. Configure Environment
```bash
# Create .env file
nano .env

# Add production settings:
SECRET_KEY=generate-strong-random-key-here
DATABASE_URL=postgresql://user:password@localhost/volunteer_db
FLASK_ENV=production
```

### 4. Initialize Database
```bash
# Initialize database
flask init-db

# Create admin user
flask create-admin
```

### 5. Configure Gunicorn
Create `/home/volunteer-app/gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/volunteer-app/error.log"
accesslog = "/var/log/volunteer-app/access.log"
loglevel = "info"
```

### 6. Create Systemd Service
Create `/etc/systemd/system/volunteer-app.service`:
```ini
[Unit]
Description=Volunteer Evaluation System
After=network.target

[Service]
User=volunteer-app
Group=volunteer-app
WorkingDirectory=/home/volunteer-app/volunteer-eval-system
Environment="PATH=/home/volunteer-app/volunteer-eval-system/venv/bin"
ExecStart=/home/volunteer-app/volunteer-eval-system/venv/bin/gunicorn \
    -c /home/volunteer-app/gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

### 7. Configure Nginx
Create `/etc/nginx/sites-available/volunteer-app`:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/volunteer-app/volunteer-eval-system/static;
        expires 30d;
    }
}
```

### 8. Enable and Start Services
```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/volunteer-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable and start application
sudo systemctl enable volunteer-app
sudo systemctl start volunteer-app
sudo systemctl status volunteer-app
```

## Post-Deployment

### Verification
- [ ] Application accessible via domain
- [ ] HTTPS working correctly
- [ ] Public form loads and submits
- [ ] Login functionality works
- [ ] Dashboard displays correctly
- [ ] API endpoints functional
- [ ] Static files serve correctly

### Monitoring Setup
- [ ] Configure application logging
- [ ] Set up error alerting
- [ ] Monitor disk space
- [ ] Monitor database performance
- [ ] Set up uptime monitoring
- [ ] Configure backup alerts

### Documentation
- [ ] Document server credentials (securely)
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedures
- [ ] Create admin user guide

## Maintenance

### Daily
- [ ] Check application logs
- [ ] Monitor error rates
- [ ] Verify backups completed

### Weekly
- [ ] Review performance metrics
- [ ] Check disk space
- [ ] Review security logs
- [ ] Test backup restoration

### Monthly
- [ ] Apply security updates
- [ ] Review and archive old data
- [ ] Performance optimization
- [ ] Capacity planning review

### Quarterly
- [ ] Full security audit
- [ ] Disaster recovery test
- [ ] Review and update documentation
- [ ] User access review

## Backup Strategy

### Database Backups
```bash
# Daily automated backup
0 2 * * * pg_dump volunteer_db | gzip > /backups/volunteer_db_$(date +\%Y\%m\%d).sql.gz

# Retain 30 days of backups
0 3 * * * find /backups -name "volunteer_db_*.sql.gz" -mtime +30 -delete
```

### Application Backups
```bash
# Weekly application backup
0 3 * * 0 tar -czf /backups/app_$(date +\%Y\%m\%d).tar.gz /home/volunteer-app/volunteer-eval-system
```

### Backup Verification
- [ ] Test restore monthly
- [ ] Verify backup integrity
- [ ] Store off-site copy
- [ ] Document restore procedure

## Rollback Plan

### If Deployment Fails
1. Stop new application: `sudo systemctl stop volunteer-app`
2. Restore previous version
3. Restore database backup if needed
4. Start application: `sudo systemctl start volunteer-app`
5. Verify functionality
6. Investigate and document issue

### Database Rollback
```bash
# Restore from backup
gunzip < /backups/volunteer_db_YYYYMMDD.sql.gz | psql volunteer_db
```

## Scaling Considerations

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes
- Enable query caching

### Horizontal Scaling
- Add more Gunicorn workers
- Set up load balancer
- Implement session storage (Redis)
- Separate database server
- Use CDN for static files

## Security Checklist

- [ ] All passwords are strong and unique
- [ ] SSH key-based authentication only
- [ ] Firewall configured (only 80, 443 open)
- [ ] Regular security updates applied
- [ ] Application logs reviewed regularly
- [ ] Database access restricted
- [ ] Sensitive data encrypted
- [ ] Rate limiting implemented
- [ ] CSRF protection enabled
- [ ] Input validation comprehensive

## Troubleshooting

### Application Won't Start
1. Check logs: `sudo journalctl -u volunteer-app -n 50`
2. Verify environment variables
3. Check database connectivity
4. Verify file permissions

### Database Connection Issues
1. Check PostgreSQL status: `sudo systemctl status postgresql`
2. Verify credentials in .env
3. Check database exists: `psql -l`
4. Review pg_hba.conf settings

### Performance Issues
1. Check server resources: `htop`
2. Review slow query log
3. Check Gunicorn worker count
4. Monitor database connections
5. Review Nginx access logs

## Contact Information

**System Administrator**: [Your Name]
**Email**: [Your Email]
**Phone**: [Your Phone]
**On-Call Schedule**: [Link or Details]

## Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
