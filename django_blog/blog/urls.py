from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Blog posts (CRUD using class-based views)
    path('post/', views.PostListView.as_view(), name='post'),
    path('post/new/', views.PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
