from django.urls import path
from .views import (
    UserRegistrationView,
    user_login,
    user_logout,
    UserProfileView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]