from django.shortcuts import render
from django.views import View
from .models import Book, Library
from django.views.generic import DetailView

# Create your views here.

# Function-based view to list all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# Class-based view to show details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'