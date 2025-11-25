"""
This file contains all API views for the Book model using Django REST Framework generic views.

Views Included:
- BookListView: Lists all books (public)
- BookDetailView: Retrieves a single book by ID (public)
- BookCreateView: Creates a new book (authenticated users only)
- BookUpdateView: Updates an existing book (authenticated users only)
- BookDeleteView: Deletes a book (authenticated users only)

Each view uses DRF generic classes to reduce boilerplate code and simplify CRUD operations.
Permissions:
- Read-only for unauthenticated users.
- Full access for authenticated users.
"""


from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend  
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    
    # 🔍 Filtering, Searching, Ordering configuration
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # 1Filtering settings
    filterset_fields = ['title', 'author', 'publication_year']

    # 2️⃣ Searching settings
    search_fields = ['title', 'author__name']

    # 3️⃣ Ordering settings
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom behavior: automatically validate data before saving
    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom behavior during update
    def perform_update(self, serializer):
        serializer.save()



class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom behavior during deletion
    def perform_destroy(self, instance):
        instance.delete()
