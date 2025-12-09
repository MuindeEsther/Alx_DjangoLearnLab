# Social Media API - Django REST Framework

A modern Django REST Framework API for a social media platform with features like user authentication, posts, comments, likes, and notifications.

## Features

- **User Authentication**: Token-based authentication with custom user model
- **Posts Management**: Create, read, update, and delete posts
- **Comments**: Add comments to posts with nested serialization
- **Likes**: Like and unlike posts
- **Follow System**: Follow/unfollow other users
- **Notifications**: Real-time notification system
- **Pagination**: Standard pagination for list views
- **Filtering & Search**: Filter posts by author and search content

## Tech Stack

- Django 5.2.7
- Django REST Framework 3.14.0
- Python 3.10+
- SQLite (development) / PostgreSQL (production)

## Project Structure

```
social_media_api/
├── accounts/           # User authentication & profiles
├── posts/             # Posts, comments, and likes
├── notifications/     # Notification system
├── social_media_api/  # Project settings
├── manage.py
├── requirements.txt
├── Procfile          # Heroku deployment
├── runtime.txt       # Python version
├── .env.example      # Environment variables template
└── .gitignore
```

## Local Development Setup

### Prerequisites

- Python 3.10 or higher
- pip and virtualenv
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/MuindeEsther/Alx_DjangoLearnLab.git
cd social_media_api
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings (optional for local development)
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Create superuser (admin)**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login and get token
- `POST /api/accounts/logout/` - Logout

### Posts
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create new post (authenticated)
- `GET /api/posts/{id}/` - Get post details
- `PUT /api/posts/{id}/` - Update post (author only)
- `DELETE /api/posts/{id}/` - Delete post (author only)
- `POST /api/posts/{id}/like/` - Like a post
- `POST /api/posts/{id}/unlike/` - Unlike a post

### Comments
- `GET /api/posts/{post_id}/comments/` - List post comments
- `POST /api/posts/{post_id}/comments/` - Create comment (authenticated)

### Users
- `GET /api/accounts/` - List users
- `GET /api/accounts/{id}/` - Get user profile
- `POST /api/accounts/{id}/follow/` - Follow user
- `POST /api/accounts/{id}/unfollow/` - Unfollow user

### Notifications
- `GET /notifications/` - List user notifications
- `POST /notifications/{id}/mark-as-read/` - Mark notification as read

## Deployment

### Option 1: Deploy to Heroku

1. **Create Heroku account and install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku app**
```bash
heroku create your-app-name
```

4. **Set environment variables**
```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
```

5. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

6. **Deploy to Heroku**
```bash
git push heroku main
```

### Option 2: Deploy to PythonAnywhere

1. Visit https://www.pythonanywhere.com/
2. Sign up for a free account
3. Follow their Django deployment guide
4. Upload your code via git or web interface
5. Configure virtual environment with dependencies from `requirements.txt`
6. Set up static files serving

### Option 3: Deploy to DigitalOcean / AWS / Azure

1. Create a Linux server (Ubuntu 20.04 or later)
2. Install Python 3.10+, PostgreSQL, and Nginx
3. Clone repository and set up virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Configure Gunicorn and Nginx for reverse proxy
6. Set up environment variables in `.env` file
7. Collect static files: `python manage.py collectstatic --noinput`
8. Run migrations: `python manage.py migrate`
9. Start Gunicorn: `gunicorn social_media_api.wsgi`

## Production Deployment Checklist

- [ ] Set `DEBUG = False` in settings or `.env`
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure PostgreSQL database
- [ ] Set up email backend for password reset
- [ ] Enable CORS if frontend is separate
- [ ] Collect static files
- [ ] Run migrations
- [ ] Create superuser for admin access
- [ ] Monitor logs and error tracking
- [ ] Set up database backups
- [ ] Configure CDN for media files (optional)

## Environment Variables

Key environment variables for production:

```
SECRET_KEY          - Django secret key (generate new one for production)
DEBUG               - Set to False in production
ALLOWED_HOSTS       - Comma-separated list of allowed domains
DATABASE_URL        - Database connection string (optional, uses SQLite if not set)
EMAIL_HOST          - SMTP server for email
EMAIL_PORT          - SMTP port
EMAIL_HOST_USER     - Email username
EMAIL_HOST_PASSWORD - Email password
```

## Common Issues & Troubleshooting

### Database Errors on Deploy
```bash
heroku run python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Permission denied on media uploads
- Ensure `MEDIA_ROOT` directory exists and is writable
- On servers, ensure proper file permissions

### CSRF token errors
- Ensure CORS is properly configured if using separate frontend
- Check `CSRF_TRUSTED_ORIGINS` in settings

## Security Notes

1. **Never commit `.env` file** - Use `.env.example` as template
2. **Use strong SECRET_KEY** - Generate new one for production
3. **Enable HTTPS** - Always use SSL/TLS in production
4. **Update dependencies** - Regularly update packages for security patches
5. **Use environment variables** - Store sensitive data in env, not in code

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

- **Muinde Esther** - Initial work

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review Django REST Framework docs: https://www.django-rest-framework.org/

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Heroku Django Deployment](https://devcenter.heroku.com/articles/django-app-configuration)
- [PythonAnywhere](https://help.pythonanywhere.com/pages/Django)
