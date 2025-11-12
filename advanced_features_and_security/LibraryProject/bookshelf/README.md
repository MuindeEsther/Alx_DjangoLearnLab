Custom Permissions:
- can_view: allows viewing book records
- can_create: allows adding new books
- can_edit: allows editing existing books
- can_delete: allows deleting books

Groups:
- Viewers: can_view
- Editors: can_create, can_edit
- Admins: all permissions

scripts/create_group.py

-- Creating groupd and assigning permissions


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

# Create groups
editors, _ = Group.objects.get_or_create(name='Editors')
viewers, _ = Group.objects.get_or_create(name='Viewers')
admins, _ = Group.objects.get_or_create(name='Admins')

# Get book permissions
content_type = ContentType.objects.get_for_model(Book)
can_view = Permission.objects.get(codename='can_view', content_type=content_type)
can_create = Permission.objects.get(codename='can_create', content_type=content_type)
can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

# Assign permissions to groups
editors.permissions.set([can_create, can_edit])
viewers.permissions.set([can_view])
admins.permissions.set([can_view, can_create, can_edit, can_delete])

# Django Security Best Practices Implemented

1. Secure Settings:
   - DEBUG=False
   - CSRF_COOKIE_SECURE=True
   - SESSION_COOKIE_SECURE=True
   - SECURE_BROWSER_XSS_FILTER=True
   - X_FRAME_OPTIONS='DENY'
   - SECURE_CONTENT_TYPE_NOSNIFF=True
   - SECURE_SSL_REDIRECT=True

2. Templates:
   - All POST forms include {% csrf_token %}

3. Views:
   - User input validated via Django forms
   - ORM queries used instead of raw SQL
   - Views protected with @login_required and @permission_required

4. Content Security Policy:
   - CSP headers set via middleware or django-csp

