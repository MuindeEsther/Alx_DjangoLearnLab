# LibraryProject 📚

This is a simple Django project created to explore the basics of Django web development.

## Project Overview
The **LibraryProject** is a sample web application built using the Django framework.  
It demonstrates how to:
- Create a Django project using `django-admin startproject`
- Set up and run the Django development server
- Understand the basic Django project structure

## Project Structure
After creating the project, you will see the following files and folders:
- `manage.py` — Command-line utility for interacting with this Django project.
- `LibraryProject/` — Main project directory that contains:
  - `settings.py` — Configuration for your project.
  - `urls.py` — URL routing for the project.
  - `wsgi.py` and `asgi.py` — Interfaces for web servers.

## How to Run the Project
1. Install Django:
   ```bash
   pip install django

# LibraryProject – Security and HTTPS Configuration

This README provides instructions and explanations for implementing security best practices and HTTPS in the LibraryProject Django application.

---

## **1. Django Security Settings**

The following settings are implemented in `LibraryProject/settings.py`:

### **Debug and HTTPS**
```python
DEBUG = False  # Disable detailed error pages in production
SECURE_SSL_REDIRECT = True  # Redirect all HTTP traffic to HTTPS
SESSION_COOKIE_SECURE = True  # Session cookies sent over HTTPS only
CSRF_COOKIE_SECURE = True     # CSRF cookies sent over HTTPS only
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking by denying framing
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing
SECURE_BROWSER_XSS_FILTER = True    # Enable browser XSS filtering
```

## 2. Deployment Configuration (HTTPS)

Your Django app must be served through a web server that supports HTTPS. Example with Nginx:
```nginx
# Redirect all HTTP traffic to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.key;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Django app running locally
        include proxy_params;
    }

    
}

location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header X-Forwarded-Proto $scheme;  # This sets HTTP_X_FORWARDED_PROTO
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

```
