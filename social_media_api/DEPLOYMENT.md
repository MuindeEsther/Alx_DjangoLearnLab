# Social Media API - Deployment Guide

This guide covers multiple deployment options for the Social Media API. Choose the one that best fits your infrastructure and requirements.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Deployment (Recommended)](#docker-deployment-recommended)
3. [Heroku Deployment](#heroku-deployment)
4. [Self-Hosted VPS (DigitalOcean, AWS, Azure)](#self-hosted-vps-digitalocean-aws-azure)
5. [PythonAnywhere](#pythonanywhere)
6. [Production Checklist](#production-checklist)

---

## Prerequisites

Before deploying, ensure you have:
- Code pushed to GitHub repository
- All dependencies listed in `requirements.txt`
- `.env.example` file for environment variables
- `.gitignore` configured to exclude sensitive files
- Django migrations ready
- Static files configuration done

---

## Docker Deployment (Recommended)

Docker makes deployment consistent across different environments.

### Requirements
- Docker installed (https://docs.docker.com/get-docker/)
- Docker Compose installed

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/social_media_api.git
cd social_media_api
```

2. **Create .env file**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

4. **Run migrations**
```bash
docker-compose exec web python manage.py migrate
```

5. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Access the application**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f web

# Stop containers
docker-compose down

# Remove volumes (caution: deletes database)
docker-compose down -v

# Rebuild image
docker-compose up -d --build

# Access web container shell
docker-compose exec web sh
```

### Production with Docker

For production, create a `.env.prod` file:

```bash
DEBUG=False
SECRET_KEY=your-very-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db:5432/social_media_db
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

Then run:
```bash
docker-compose -f docker-compose.yml --env-file .env.prod up -d
```

---

## Heroku Deployment

### Requirements
- Heroku account (free or paid)
- Heroku CLI installed
- Git repository

### Steps

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. **Set environment variables**
```bash
heroku config:set SECRET_KEY='your-secret-key-here'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

4. **Deploy to Heroku**
```bash
git push heroku main
```

5. **Run migrations**
```bash
heroku run python manage.py migrate
```

6. **Create superuser**
```bash
heroku run python manage.py createsuperuser
```

7. **View logs**
```bash
heroku logs --tail
```

### Heroku-Specific Notes
- `Procfile` handles web server startup
- `runtime.txt` specifies Python version
- PostgreSQL is automatically configured via `DATABASE_URL`
- WhiteNoise handles static files

### Custom Domain on Heroku
```bash
heroku domains:add www.yourdomain.com
heroku domains:add yourdomain.com
```

---

## Self-Hosted VPS (DigitalOcean, AWS, Azure)

### Requirements
- Linux server (Ubuntu 20.04 or newer)
- Root or sudo access
- Domain name with DNS configured

### Step 1: Server Setup

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3.10 python3-pip python3-venv
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y nginx supervisor

# Create application user
sudo useradd -m -s /bin/bash social_media
sudo -u social_media mkdir -p /home/social_media/app
```

### Step 2: Clone and Setup Application

```bash
sudo -u social_media git clone https://github.com/yourusername/social_media_api.git /home/social_media/app
cd /home/social_media/app

# Create virtual environment
sudo -u social_media python3 -m venv venv
sudo -u social_media venv/bin/pip install --upgrade pip
sudo -u social_media venv/bin/pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
sudo -u postgres psql << EOF
CREATE DATABASE social_media_db;
CREATE USER social_media_user WITH PASSWORD 'strong_password_here';
ALTER ROLE social_media_user SET client_encoding TO 'utf8';
ALTER ROLE social_media_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE social_media_user SET default_transaction_deferrable TO on;
ALTER ROLE social_media_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;
\q
EOF
```

### Step 4: Configure Django

Create `/home/social_media/app/.env`:

```
SECRET_KEY=your-very-secure-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://social_media_user:strong_password_here@localhost:5432/social_media_db
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Step 5: Collect Static Files

```bash
cd /home/social_media/app
sudo -u social_media venv/bin/python manage.py migrate
sudo -u social_media venv/bin/python manage.py collectstatic --noinput
```

### Step 6: Configure Supervisor

Create `/etc/supervisor/conf.d/social_media_api.conf`:

```ini
[program:social_media_api]
directory=/home/social_media/app
command=/home/social_media/app/venv/bin/gunicorn social_media_api.wsgi --bind 127.0.0.1:8000 --workers 4
user=social_media
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/social_media_api.log
```

Then:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start social_media_api
```

### Step 7: Configure Nginx

Copy content from `nginx.conf.example` to `/etc/nginx/sites-available/social_media_api` and update:
- Replace `yourdomain.com` with your domain
- Update paths to `/home/social_media/app/staticfiles` and `/home/social_media/app/media`

```bash
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### Step 9: Monitoring and Logs

```bash
# Application logs
tail -f /var/log/social_media_api.log

# Nginx logs
tail -f /var/log/nginx/social_media_api_access.log
tail -f /var/log/nginx/social_media_api_error.log

# Supervisor status
sudo supervisorctl status
```

---

## PythonAnywhere

### Steps

1. **Sign up** at https://www.pythonanywhere.com/
2. **Upload code** via Git or Web interface
3. **Configure virtual environment**:
   - Go to Web tab
   - Create new virtualenv with Python 3.10
   - Install packages: `pip install -r requirements.txt`

4. **Configure WSGI**:
   - Update WSGI file with correct path to `social_media_api.wsgi`

5. **Set environment variables**:
   - Add to `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['DEBUG'] = 'False'
```

6. **Run migrations**:
   - Use Web tab > Bash console:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

7. **Reload web app** from Web tab

---

## Production Checklist

Before going live, complete this checklist:

### Security
- [ ] Change `SECRET_KEY` to a unique, random value
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS/SSL certificate
- [ ] Enable CSRF protection
- [ ] Configure secure cookies (HTTPS only)
- [ ] Set up Content Security Policy headers
- [ ] Remove or restrict admin panel access

### Database
- [ ] Use PostgreSQL (not SQLite) in production
- [ ] Set strong database password
- [ ] Configure regular backups
- [ ] Enable database encryption
- [ ] Configure database user permissions

### Performance
- [ ] Enable caching (Redis/Memcached)
- [ ] Configure CDN for static/media files
- [ ] Enable gzip compression
- [ ] Set up database connection pooling
- [ ] Configure appropriate worker count

### Monitoring & Logging
- [ ] Set up error tracking (Sentry, New Relic)
- [ ] Configure logging to file/service
- [ ] Set up uptime monitoring
- [ ] Configure email alerts
- [ ] Monitor resource usage

### Deployment
- [ ] All code committed and pushed to repository
- [ ] `.env` file created with production values
- [ ] `.env` added to `.gitignore`
- [ ] `.gitignore` includes `__pycache__`, `*.pyc`, `db.sqlite3`
- [ ] `manage.py migrate` executed
- [ ] `collectstatic` executed
- [ ] Superuser account created

### API Security
- [ ] Rate limiting configured
- [ ] Input validation in place
- [ ] CORS configured for your domain only
- [ ] Token expiration configured
- [ ] Sensitive data not logged
- [ ] API versioning implemented

### Maintenance
- [ ] Backup strategy documented
- [ ] Disaster recovery plan
- [ ] Update schedule for dependencies
- [ ] Staff contact list
- [ ] Runbooks for common issues

---

## Troubleshooting

### Application won't start
```bash
# Check logs
docker-compose logs -f web
# or
heroku logs --tail
# or
tail -f /var/log/social_media_api.log
```

### Database migration errors
```bash
# Reset migrations (development only)
python manage.py migrate --fake posts zero
python manage.py migrate
```

### Static files not loading
```bash
# Recollect static files
python manage.py collectstatic --noinput --clear
```

### Port already in use
```bash
# Change port in docker-compose.yml or gunicorn command
gunicorn social_media_api.wsgi --bind 127.0.0.1:8001
```

### CORS errors
- Check `CORS_ALLOWED_ORIGINS` in `.env`
- Ensure frontend URL matches exactly (including protocol)

### 502 Bad Gateway
- Check if Gunicorn is running
- Check Nginx/proxy configuration
- Check application logs for errors

---

## Maintenance

### Regular Tasks

```bash
# Backup database (PostgreSQL)
pg_dump -U username database_name > backup.sql

# Update dependencies
pip install -r requirements.txt --upgrade

# Check for security issues
pip check
pip install safety
safety check

# Monitor server resources
htop  # or: docker stats
```

### Scaling

As traffic grows:
1. Increase Gunicorn workers
2. Add caching layer (Redis)
3. Use CDN for static files
4. Database optimization and indexing
5. Load balancing across multiple servers

---

## Support & Resources

- [Django Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [DRF Production Guide](https://www.django-rest-framework.org/#deployment)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)

---

**Last Updated**: December 2024
**Django Version**: 5.2.7
**Python Version**: 3.10+
