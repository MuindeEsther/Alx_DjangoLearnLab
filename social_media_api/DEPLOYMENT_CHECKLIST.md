# ✅ Deployment Checklist

## Pre-Deployment (Complete Today)

### Code Preparation
- [ ] All code committed to Git
- [ ] No uncommitted changes
- [ ] `.env` file NOT in repository
- [ ] `__pycache__` directories in `.gitignore`
- [ ] `*.pyc` files in `.gitignore`
- [ ] `db.sqlite3` in `.gitignore`
- [ ] Verify `.gitignore` is working: `git status`

### Environment Setup
- [ ] Create `.env` file from `.env.example`
- [ ] Generate new `SECRET_KEY` (see below)
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set `CORS_ALLOWED_ORIGINS` for your frontend
- [ ] Never commit `.env` file

**Generate SECRET_KEY:**
```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# Copy output and paste into .env
exit()
```

### Local Testing
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Run `python manage.py check --deploy` (see warnings)
- [ ] Test with `python manage.py runserver`
- [ ] Access `http://localhost:8000/api/`
- [ ] Verify admin panel works

### Code Quality
- [ ] No hardcoded secrets in code
- [ ] No TODO comments left unresolved
- [ ] Settings only use environment variables
- [ ] Static files properly configured
- [ ] Media files directory exists
- [ ] No sensitive data in logs

---

## Deployment Checklist

### Choose Deployment Method
- [ ] Decide between Docker, Heroku, VPS, or PythonAnywhere
- [ ] Read deployment guide in `DEPLOYMENT.md`
- [ ] Prepare domain name (if using)
- [ ] Have DNS credentials ready

### Database Configuration
- [ ] For PostgreSQL: Create database and user
- [ ] Set `DATABASE_URL` in `.env`
- [ ] Or leave as SQLite for small projects
- [ ] Ensure database is accessible from app

### Security Configuration
- [ ] Generate new unique `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure CORS correctly
- [ ] Review `SECURITY.md` for hardening

### Docker Deployment (If Chosen)
- [ ] Install Docker and Docker Compose
- [ ] Create `.env` file with all variables
- [ ] Build image: `docker-compose build`
- [ ] Start services: `docker-compose up -d`
- [ ] Run migrations: `docker-compose exec web python manage.py migrate`
- [ ] Create superuser: `docker-compose exec web python manage.py createsuperuser`
- [ ] Verify at `http://localhost:8000`
- [ ] Push to production server

### Heroku Deployment (If Chosen)
- [ ] Install Heroku CLI
- [ ] Login: `heroku login`
- [ ] Create app: `heroku create your-app-name`
- [ ] Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
- [ ] Set config vars: `heroku config:set SECRET_KEY=...`
- [ ] Deploy: `git push heroku main`
- [ ] Run migrations: `heroku run python manage.py migrate`
- [ ] Create superuser: `heroku run python manage.py createsuperuser`

### VPS Deployment (If Chosen)
- [ ] Server provisioned and accessible
- [ ] Python 3.10+ installed
- [ ] PostgreSQL installed (if using)
- [ ] Nginx installed
- [ ] Supervisor installed
- [ ] Application code cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Migrations applied
- [ ] Nginx configured
- [ ] SSL certificate installed
- [ ] Supervisor configured and started

---

## Post-Deployment Verification

### Immediate (First 5 minutes)
- [ ] Application is running
- [ ] Check application logs for errors
- [ ] API endpoint responds: `GET /api/`
- [ ] Admin panel accessible: `/admin/`
- [ ] Database connection working

### Functionality Tests (First 30 minutes)
- [ ] User registration works
- [ ] User login works
- [ ] Create post works
- [ ] View posts works
- [ ] Pagination works
- [ ] Comments work
- [ ] Likes work
- [ ] Follow/unfollow works

### Performance & Monitoring (First hour)
- [ ] Response times acceptable (< 200ms)
- [ ] Database queries optimized
- [ ] Static files loading
- [ ] No 500 errors in logs
- [ ] No secrets in logs
- [ ] HTTPS working (if configured)
- [ ] CORS headers present

### Security Verification
- [ ] HTTPS enforced (if configured)
- [ ] CSRF protection working
- [ ] CORS headers correct
- [ ] No debug information exposed
- [ ] Error messages don't leak info
- [ ] Token auth working
- [ ] Admin panel accessible only to superuser

---

## Daily Maintenance

### Log Monitoring
```bash
# Docker
docker-compose logs -f web

# Heroku
heroku logs --tail

# VPS
tail -f /var/log/social_media_api.log
```

### Weekly Tasks
- [ ] Check error logs
- [ ] Monitor database size
- [ ] Review performance metrics
- [ ] Check disk space
- [ ] Update dependencies (if needed)
- [ ] Test backup restoration

### Monthly Tasks
- [ ] Full security audit
- [ ] Performance optimization review
- [ ] Database maintenance
- [ ] SSL certificate renewal check
- [ ] User feedback review
- [ ] Update Django and packages

### Quarterly Tasks
- [ ] Security vulnerability scan
- [ ] Code review
- [ ] Architecture assessment
- [ ] Scaling analysis
- [ ] Cost optimization
- [ ] Compliance review

---

## Emergency Procedures

### Application Down
```bash
# 1. Check if process is running
ps aux | grep gunicorn

# 2. Check logs
tail -f /var/log/social_media_api.log

# 3. Check database connectivity
python manage.py dbshell

# 4. Restart application
supervisorctl restart social_media_api

# 5. Or with Docker
docker-compose restart web
```

### Database Corruption
```bash
# 1. Backup current state
pg_dump database_name > backup.sql

# 2. Stop application
supervisorctl stop social_media_api

# 3. Restore from backup
psql database_name < backup.sql

# 4. Verify integrity
python manage.py dbshell

# 5. Restart application
supervisorctl start social_media_api
```

### High Memory Usage
```bash
# 1. Check memory
free -h

# 2. Check process memory
ps aux | grep python

# 3. Reduce Gunicorn workers
# Edit gunicorn_config.py or supervisord.conf

# 4. Add swap (if on VPS)
# Or increase instance size
```

### SSL Certificate Expiring
```bash
# Check expiration
openssl x509 -enddate -noout -in /path/to/cert.pem

# Renew with Certbot (Let's Encrypt)
certbot renew

# Reload Nginx
systemctl reload nginx
```

---

## Performance Optimization

### First Signs of Problems
- [ ] Slow response times
- [ ] High database load
- [ ] Memory usage increasing
- [ ] Errors in logs increasing

### Optimization Steps
1. **Database**
   - [ ] Add indexes to frequently queried fields
   - [ ] Optimize slow queries
   - [ ] Archive old data
   - [ ] Configure connection pooling

2. **Caching**
   - [ ] Enable Redis
   - [ ] Cache API responses
   - [ ] Cache database queries
   - [ ] Cache static files

3. **Code**
   - [ ] Use select_related() for foreign keys
   - [ ] Use prefetch_related() for reverse relations
   - [ ] Minimize database queries
   - [ ] Profile slow endpoints

4. **Infrastructure**
   - [ ] Add more Gunicorn workers
   - [ ] Use CDN for static files
   - [ ] Enable compression
   - [ ] Load balance traffic

---

## Monitoring Setup

### Recommended Tools
- [ ] Sentry (Error tracking)
- [ ] New Relic (Performance monitoring)
- [ ] DataDog (Infrastructure monitoring)
- [ ] UptimeRobot (Uptime monitoring)
- [ ] Papertrail (Log aggregation)

### Alerting
- [ ] Set up email alerts for errors
- [ ] Set up SMS alerts for critical issues
- [ ] Configure uptime monitoring
- [ ] Monitor response times
- [ ] Monitor error rates

---

## Backup & Recovery

### Backup Strategy
- [ ] Database backup daily
- [ ] Code backup on Git (redundant)
- [ ] Media files backup weekly
- [ ] Static files backup (regenerable)
- [ ] `.env` backup (secure location)

### Recovery Testing
- [ ] Test database restore monthly
- [ ] Test code recovery
- [ ] Document recovery procedures
- [ ] Keep recovery time < 1 hour goal

### Backup Locations
- [ ] Primary: Cloud storage (AWS S3, Azure Blob)
- [ ] Secondary: Offsite backup
- [ ] Tertiary: Local backup

---

## Scaling Checklist

### When to Scale
- [ ] Response time > 500ms consistently
- [ ] Database connections maxed
- [ ] CPU/Memory usage > 80%
- [ ] User growth > 100% month-over-month

### Horizontal Scaling (Add Servers)
- [ ] Set up load balancer
- [ ] Add more application servers
- [ ] Configure shared database
- [ ] Use shared cache (Redis)
- [ ] Set up session storage

### Vertical Scaling (Bigger Server)
- [ ] Increase RAM
- [ ] Increase CPU cores
- [ ] Upgrade storage
- [ ] Monitor improvements

---

## Cost Management

### Cost Tracking
- [ ] Document current costs
- [ ] Set monthly budget
- [ ] Review costs weekly
- [ ] Identify optimization opportunities

### Cost Optimization
- [ ] Right-size database
- [ ] Use spot instances (if AWS)
- [ ] Remove unused resources
- [ ] Optimize data transfer
- [ ] Cache aggressively

---

## Documentation Maintenance

Keep Up-to-Date:
- [ ] API documentation
- [ ] Deployment procedures
- [ ] Runbooks for common issues
- [ ] Architecture diagrams
- [ ] Database schema
- [ ] Configuration changes

---

## Pre-Launch Sign-Off

### Technical Lead Sign-Off
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Performance acceptable
- [ ] Security audit passed

### Ops Team Sign-Off
- [ ] Infrastructure ready
- [ ] Monitoring configured
- [ ] Backups working
- [ ] Recovery tested

### Product Team Sign-Off
- [ ] Features working as expected
- [ ] UX acceptable
- [ ] Documentation complete
- [ ] Go-live date confirmed

---

## Post-Launch Review

### 1 Hour After Launch
- [ ] System stable
- [ ] No critical errors
- [ ] Response times good
- [ ] Users can perform basic actions

### 1 Day After Launch
- [ ] No data corruption
- [ ] All endpoints working
- [ ] Performance stable
- [ ] User feedback positive

### 1 Week After Launch
- [ ] Identify improvement areas
- [ ] Fix critical bugs
- [ ] Optimize based on usage patterns
- [ ] Gather metrics

### 1 Month After Launch
- [ ] Full retrospective
- [ ] Document lessons learned
- [ ] Plan improvements
- [ ] Scale if needed

---

## Final Verification

Before marking as complete:

```bash
# 1. Test all endpoints
curl -X GET http://yourdomain.com/api/posts/

# 2. Test authentication
curl -X POST http://yourdomain.com/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# 3. Check database
python manage.py dbshell
SELECT count(*) FROM accounts_customuser;
\q

# 4. Check static files
http://yourdomain.com/static/admin/css/base.css

# 5. Check admin
http://yourdomain.com/admin/ (login with superuser)

# 6. Monitor logs
tail -f /var/log/social_media_api.log
```

---

**Checklist Created:** December 2024
**Last Updated:** December 2024
**Status:** READY FOR DEPLOYMENT ✅

---

Print this checklist and keep it handy during deployment!
