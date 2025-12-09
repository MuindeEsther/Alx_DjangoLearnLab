# Production Security Settings
# Add these to settings.py or use environment variables for production

"""
Production Deployment Security Checklist:

1. HTTPS/SSL Configuration
   - Use HTTPS_ONLY environment variable
   - Configure SSL certificate on your hosting

2. Security Headers
   - SECURE_SSL_REDIRECT = True
   - SECURE_HSTS_SECONDS = 31536000
   - SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   - SECURE_HSTS_PRELOAD = True

3. CSRF Protection
   - CSRF_COOKIE_SECURE = True (HTTPS only)
   - CSRF_COOKIE_HTTPONLY = True
   - SESSION_COOKIE_SECURE = True
   - SESSION_COOKIE_HTTPONLY = True

4. Content Security Policy
   - Use django-csp package for advanced CSP

5. Database Security
   - Use strong passwords
   - Regular backups
   - Encryption at rest

6. API Security
   - Token rotation
   - Rate limiting
   - Input validation
   - SQL injection prevention (Django ORM handles this)

7. Monitoring
   - Error logging with Sentry
   - Performance monitoring
   - Security audits
"""

# Add to your settings.py for production:
# 
# if not DEBUG:
#     # SSL/HTTPS
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_SECURITY_POLICY = {
#         "default-src": ("'self'",),
#     }
#     
#     # HSTS
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
