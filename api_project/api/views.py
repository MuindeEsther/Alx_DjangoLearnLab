from django.shortcuts import render
from .models import Book
from rest_framework.views import APIView
from .serializers import BookSerializer
from rest_framework import generics

# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all
    serializer_class = BookSerializer
    