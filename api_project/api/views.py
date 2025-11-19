from django.shortcuts import render
from .models import Book
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework import viewsets

# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly] # Only logged in users
    
    def get_permissions(self):
        if self.action == 'destroy':   # DELETE
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    