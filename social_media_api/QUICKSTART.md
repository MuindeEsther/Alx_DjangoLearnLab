# Quick Start - Deployment Commands

## 🚀 TL;DR - Deploy in 5 Minutes

### Option 1: Docker (Recommended - 5 minutes)
```bash
# 1. Clone repo
git clone <your-repo-url>
cd social_media_api

# 2. Create environment file
cp .env.example .env
# Edit .env - change SECRET_KEY and other settings

# 3. Run with Docker
docker-compose up -d

# 4. Create superuser
docker-compose exec web python manage.py createsuperuser

# Access at: http://localhost:8000
```

### Option 2: Heroku (2-3 minutes)
```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-app-name

# 3. Add database
heroku addons:create heroku-postgresql:hobby-dev

# 4. Set secrets
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False

# 5. Deploy
git push heroku main

# 6. Create superuser
heroku run python manage.py createsuperuser

# Access at: https://your-app-name.herokuapp.com
```

### Option 3: Local Development (for testing)
```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 2. Install
pip install -r requirements.txt

# 3. Migrate
python manage.py migrate

# 4. Run
python manage.py runserver

# Access at: http://localhost:8000
```

---

## 📋 Important Files

| File | Purpose | Action |
|------|---------|--------|
| `.env` | Secrets & config | Create from `.env.example` |
| `requirements.txt` | Python packages | Already prepared |
| `docker-compose.yml` | Docker stack | Ready to use |
| `DEPLOYMENT.md` | Detailed guide | Read for full instructions |
| `README.md` | API documentation | Reference |

---

## 🔑 Critical Environment Variables

**Minimum required for production:**

```env
# Generate new SECRET_KEY!
SECRET_KEY=your-very-long-random-string-here

# Set to False in production
DEBUG=False

# Your domain
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Frontend URL
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

---

## ⚡ Common Commands

```bash
# View logs
docker-compose logs -f web

# Stop everything
docker-compose down

# Run migrations
docker-compose exec web python manage.py migrate

# Create user
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test
```

---

## 🚨 Before You Deploy

- [ ] Create `.env` file
- [ ] Generate new `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Push to GitHub
- [ ] Test locally first

---

## ✅ Verification Checklist

After deployment, verify:

```bash
# 1. API is responding
curl https://yourdomain.com/api/

# 2. Admin is accessible
https://yourdomain.com/admin/

# 3. Database migrations ran
docker-compose exec web python manage.py showmigrations

# 4. Static files serving
https://yourdomain.com/static/admin/css/base.css

# 5. Create test post
# Use API documentation at /api/
```

---

## 📞 Help

- **Full guide**: See `DEPLOYMENT.md`
- **Security tips**: See `SECURITY.md`
- **API docs**: See `README.md`
- **Issues**: Check Docker logs: `docker-compose logs`

---

**Ready to deploy? Start with Docker option above!** 🎉
