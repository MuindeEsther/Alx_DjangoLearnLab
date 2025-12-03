from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post


# Custom User Creation Form with Email field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Custom User Edit Form
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# Authentication Views
def register(request):
    """Handle user registration with email validation."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created successfully.')
            return redirect('blog:posts')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('blog:posts')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('blog:posts')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'blog/login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('blog:home')


@login_required(login_url='blog:login')
def profile(request):
    """Display user profile information."""
    return render(request, 'blog/profile.html', {'user': request.user})


@login_required(login_url='blog:login')
def edit_profile(request):
    """Allow authenticated user to edit their profile."""
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('blog:profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'blog/edit_profile.html', {'form': form})


# Blog Views
def home(request):
    """Display home page with recent posts."""
    posts = Post.objects.all().order_by('-published_date')[:5]
    return render(request, 'blog/home.html', {'posts': posts})


def posts_list(request):
    """Display all blog posts with pagination."""
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/posts_list.html', {'posts': posts})


def post_detail(request, post_id):
    """Display a single blog post."""
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required(login_url='blog:login')
def create_post(request):
    """Allow authenticated users to create a new blog post."""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', post_id=post.id)
        else:
            messages.error(request, 'Title and content are required.')
    
    return render(request, 'blog/create_post.html')


@login_required(login_url='blog:login')
def edit_post(request, post_id):
    """Allow authors to edit their own posts."""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.save()
        messages.success(request, 'Post updated successfully!')
        return redirect('blog:post_detail', post_id=post.id)
    
    return render(request, 'blog/edit_post.html', {'post': post})


@login_required(login_url='blog:login')
def delete_post(request, post_id):
    """Allow authors to delete their own posts."""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:posts')
    
    return render(request, 'blog/delete_post.html', {'post': post})
