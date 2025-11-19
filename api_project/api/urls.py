from django.urls import path
from .views import BookList

urlpatterns = [
    path('', BookList.as_view(), name='book-list'),  # Maps to the BookList view
]