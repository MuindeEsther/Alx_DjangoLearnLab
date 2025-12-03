# Django Blog - AI Coding Instructions

## Project Overview

This is a **Django 5.2 blog application** (ALX learning project) with a minimal starter setup. The project uses SQLite for development and follows Django conventions.

**Key Facts:**
- Single app structure: `blog/` (not yet registered in `INSTALLED_APPS`)
- Database: SQLite (`db.sqlite3`)
- Python entry point: `manage.py`
- Static files: `blog/static/` and project-level `static/`
- Templates: `blog/templates/blog/` (Django app-level organization)

## Architecture & Data Flow

### Current State
The `Post` model is defined but the blog app is incomplete:
- ✅ **Models** (`blog/models.py`): `Post` model with title, content, author (ForeignKey to User), published_date
- ✅ **Templates** (`blog/templates/blog/base.html`): Base layout with navigation (references undefined URL names: 'home', 'posts', 'login', 'register')
- ⚠️ **Views** (`blog/views.py`): Empty - needs implementation
- ⚠️ **Admin** (`blog/admin.py`): Empty - needs model registration
- ⚠️ **URLs** (`django_blog/urls.py`): Only admin URL configured - needs blog app include and blog app URLs file

### Data Flow (To Be Implemented)
User → Django URL Router → View → Query `Post` model → Render template with context

### Common Pattern: App Registration
Before any app functionality works:
1. Add `'blog'` to `INSTALLED_APPS` in `django_blog/settings.py`
2. Create `blog/urls.py` with app-specific URL patterns
3. Include blog URLs in `django_blog/urls.py` with `path('blog/', include('blog.urls'))`

## Essential Developer Workflows

### Running the Server
```bash
python manage.py runserver
```
Server runs on `http://127.0.0.1:8000/` by default.

### Database Migrations
```bash
python manage.py makemigrations     # Create migration files after model changes
python manage.py migrate             # Apply migrations to SQLite database
```
Migrations are auto-tracked in `blog/migrations/`.

### Django Admin Access
```bash
python manage.py createsuperuser    # Create admin user (interactive prompt)
```
Access admin at `http://127.0.0.1:8000/admin/`

### Testing (When Added)
```bash
python manage.py test               # Run tests from blog/tests.py
```

## Key Project Conventions

### Template Organization
- Base template: `blog/templates/blog/base.html`
- Child templates should extend `base.html` and override `{% block content %}`
- Reference static files: `{% static 'blog/css/styles.css' %}` (requires `{% load static %}`)
- URL references: `{% url 'url_name' %}` (URL names defined in `urls.py`)

### Static Files Location
- App-specific: `blog/static/blog/css/` and `blog/static/blog/js/`
- Following Django convention: `<app>/static/<app>/`
- To collect static files: `python manage.py collectstatic`

### URL Naming Convention
Current undefined names in template: `'home'`, `'posts'`, `'login'`, `'register'`
Define these in `blog/urls.py` as:
```python
path('', views.home, name='home')
path('posts/', views.posts_list, name='posts')
```

## Critical Files & Their Purpose

| File | Purpose | Status |
|------|---------|--------|
| `blog/models.py` | Data models (Post) | Defined, not registered in admin |
| `blog/views.py` | Request handlers for blog pages | Empty |
| `blog/urls.py` | Blog-specific URL routing | Missing - must create |
| `blog/admin.py` | Django admin configuration | Empty |
| `django_blog/urls.py` | Project-level URL dispatcher | Only admin configured |
| `django_blog/settings.py` | Project configuration, `INSTALLED_APPS` | Blog app not installed |
| `blog/templates/blog/base.html` | Main HTML layout | References undefined URLs |
| `blog/static/blog/css/styles.css` | Stylesheet | Exists (may be empty) |

## Authentication System - IMPLEMENTED

### User Registration & Login
- **Registration**: Custom form extends `UserCreationForm`, validates email uniqueness
- **Login**: Django's built-in auth with username/password
- **Logout**: Clears session and redirects to home
- **Profile Management**: View and edit user details (first_name, last_name, email)

### Security Features
- CSRF tokens in all forms (via `{% csrf_token %}`)
- Passwords hashed using Django's default PBKDF2 algorithm
- `@login_required` decorator protects post creation/editing/deletion
- Post author verification: Only post authors can edit/delete their posts
- Email uniqueness validation during registration

### Authentication Routes
```
/register/           - POST: Create account, GET: Show form
/login/              - POST: Authenticate user, GET: Show login form
/logout/             - POST: End session
/profile/            - GET: View user profile (login_required)
/profile/edit/       - POST/GET: Edit profile details (login_required)
```

## Blog System - IMPLEMENTED

### Post Management Routes
```
/                    - Home page with recent posts
/posts/              - List all posts
/posts/<id>/         - View single post
/posts/create/       - Create new post (login_required)
/posts/<id>/edit/    - Edit post (login_required + author check)
/posts/<id>/delete/  - Delete post (login_required + author check)
```

### Key Views
- `register()`: Custom registration with email validation
- `login_view()`: Standard Django login
- `logout_view()`: Session cleanup
- `profile()` / `edit_profile()`: User profile management
- `home()`: Recent posts homepage
- `posts_list()`: All posts chronologically
- `post_detail()`: Single post with edit/delete for authors
- `create_post()`: Form-based post creation
- `edit_post()`: Author-only post editing
- `delete_post()`: Author-only post deletion with confirmation

### Custom Forms
- `CustomUserCreationForm`: Extends `UserCreationForm`, adds email field with uniqueness check
- `UserEditForm`: ModelForm for User fields (first_name, last_name, email)

## Integration Points

- **Django Admin**: Models must be registered in `admin.py` to appear in `/admin/`
- **User Authentication**: `User` model imported from `django.contrib.auth` - used for Post.author
- **Static Files**: Served from `blog/static/blog/` path; must use `{% load static %}` in templates
- **URL Resolution**: Templates use `{% url %}` tag - matching names must exist in URL patterns

## Quick Command Reference

```bash
python manage.py startapp <app_name>         # Create new app
python manage.py shell                       # Interactive Python shell with Django context
python manage.py dbshell                     # SQLite3 shell
python manage.py check                       # Validate project configuration
```

## Testing & Setup Instructions

### 1. Apply Database Migrations
```bash
python manage.py makemigrations    # Generate migration files (blog app models)
python manage.py migrate            # Apply migrations to SQLite3
```
The Post model is now tracked in the database.

### 2. Create Superuser for Admin Access
```bash
python manage.py createsuperuser
# Interactive prompts:
# Username: <enter username>
# Email: <enter email>
# Password: <enter secure password>
```

### 3. Run Development Server
```bash
python manage.py runserver
```
Server runs at `http://127.0.0.1:8000/`

### 4. Access the Application

**User Flows:**
1. **Register**: Navigate to `/register/` → Fill form → Auto-login
2. **Login**: Navigate to `/login/` → Enter credentials
3. **Create Post**: `/posts/create/` → Title + Content → Publish
4. **Edit/Delete**: Navigate to post → Author-only buttons appear
5. **Profile**: `/profile/` → View posts and profile info
6. **Edit Profile**: `/profile/edit/` → Update name/email

**Admin Panel:**
- URL: `/admin/`
- Login with superuser credentials
- Manage posts, users, permissions
- Filter posts by author/date, search by title

### 5. Testing Authentication Flows

**Test Registration:**
- Valid registration with unique email → User created, logged in
- Duplicate email → Form error: "This email address is already registered."
- Password mismatch → Form error: "Passwords don't match"
- Short password → Form error: "Too short" (Django password validator)

**Test Login:**
- Valid credentials → Logged in, redirected to /posts/
- Invalid credentials → Error message: "Invalid username or password"
- Already authenticated → Redirect to /posts/

**Test Authorization:**
- Logged-out user → Access /profile/ → Redirect to /login/
- Logged-out user → Access /posts/create/ → Redirect to /login/
- User A edits User B's post → Error: "You do not have permission"

**Test Post Operations:**
- Create post as authenticated user → Redirect to post detail
- Edit own post → Changes saved, success message
- Delete own post → Confirmation page required
- View post by non-author → No edit/delete buttons

### 6. Browser Testing
- Check responsive nav (authentication status shown)
- Verify messages display (success/error)
- Test form validation (inline feedback)
- Confirm CSRF tokens present (Django requirement)

### 7. Django Shell Testing (Optional)
```bash
python manage.py shell

# Create user programmatically
from django.contrib.auth.models import User
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Create post
from blog.models import Post
post = Post.objects.create(
    title='Test Post',
    content='This is test content',
    author=user
)

# Query posts
Post.objects.all()
user.posts.all()
```

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No such table: blog_post" | Migration not applied | Run `python manage.py migrate` |
| "Page not found at /register/" | URL not included | Check `django_blog/urls.py` includes blog.urls |
| Login redirects infinitely | `LOGIN_URL` not configured | Django uses default `/accounts/login/`; we use `login_required(login_url='blog:login')` |
| CSRF token missing | `{% csrf_token %}` not in form | Add to all POST forms |
| Author can't edit post | Permission check failed | Verify `post.author == request.user` in view |
| Static files not loading | Debug=False in production | Use `python manage.py collectstatic` for production |
