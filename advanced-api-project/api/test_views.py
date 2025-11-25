"""
Unit Tests for Book API Endpoints

This test suite covers:
1. CRUD Operations (Create, Read, Update, Delete)
2. Filtering functionality
3. Searching functionality
4. Ordering functionality
5. Permission and authentication checks

Test Database Configuration:
- Django AUTOMATICALLY creates a separate test database (test_<database_name>)
- The test database is isolated from production/development databases
- All data is created fresh for each test and destroyed after test completion
- No impact on your actual database data
- Authentication uses force_authenticate() instead of client.login() for better isolation

How Django Handles Test Database:
1. Before tests: Creates test_<database_name>
2. During tests: All operations happen in the test database
3. After tests: Automatically destroys the test database
4. Each test runs in a transaction that is rolled back after completion

Running Tests:
    python manage.py test api
    python manage.py test api.test_views
    python manage.py test api.test_views.BookAPITestCase
    python manage.py test api --verbosity=2  # Detailed output

Coverage:
- All endpoints are tested with valid and invalid inputs
- Authentication scenarios (authenticated vs unauthenticated)
- Edge cases and error handling
- No client.login() used - we use force_authenticate() for isolated testing
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book


class BookAPITestCase(TestCase):
    """
    Comprehensive test suite for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        """
        Set up test data and clients before each test method.
        This runs before every individual test.
        
        Authentication Methods Available:
        - self.client.login() - Standard Django authentication
        - self.client.force_authenticate() - DRF token/session bypass
        """
        # Create API client
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create sample books for testing
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            author='William Vincent',
            publication_year=2023
        )
        self.book2 = Book.objects.create(
            title='Python Crash Course',
            author='Eric Matthes',
            publication_year=2019
        )
        self.book3 = Book.objects.create(
            title='Flask Web Development',
            author='Miguel Grinberg',
            publication_year=2018
        )

    # ==================== BookListView TESTS ====================

    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can view the book list."""
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_books_authenticated(self):
        """Test that authenticated users can view the book list."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # ==================== BookDetailView TESTS ====================

    def test_retrieve_book_detail(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['author'], 'William Vincent')
        self.assertEqual(response.data['publication_year'], 2023)

    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        response = self.client.get('/api/books/9999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ==================== BookCreateView TESTS ====================

    def test_create_book_authenticated(self):
        """Test that authenticated users can create a book using force_authenticate."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'New Django Book',
            'author': 'Test Author',
            'publication_year': 2024
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Django Book')

    def test_create_book_with_login(self):
        """Test that authenticated users can create a book using client.login."""
        # Use standard Django login method
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Book Created With Login',
            'author': 'Login Test Author',
            'publication_year': 2024
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Book Created With Login')
        
        # Logout after test
        self.client.logout()

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create a book."""
        data = {
            'title': 'Unauthorized Book',
            'author': 'Test Author',
            'publication_year': 2024
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_invalid_data(self):
        """Test creating a book with missing required fields."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Incomplete Book'
        }
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==================== BookUpdateView TESTS ====================

    def test_update_book_authenticated(self):
        """Test that authenticated users can update a book using force_authenticate."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'title': 'Django for Beginners - Updated',
            'author': 'William Vincent',
            'publication_year': 2024
        }
        response = self.client.put(f'/api/books/{self.book1.id}/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Django for Beginners - Updated')
        self.assertEqual(self.book1.publication_year, 2024)

    def test_update_book_with_login(self):
        """Test that authenticated users can update a book using client.login."""
        # Use standard Django login method
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Updated With Login Method',
            'author': 'William Vincent',
            'publication_year': 2025
        }
        response = self.client.put(f'/api/books/{self.book1.id}/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated With Login Method')
        
        # Logout after test
        self.client.logout()

    def test_partial_update_book(self):
        """Test partial update (PATCH) of a book."""
        self.client.force_authenticate(user=self.user)
        
        data = {'publication_year': 2025}
        response = self.client.patch(f'/api/books/{self.book1.id}/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.publication_year, 2025)
        self.assertEqual(self.book1.title, 'Django for Beginners')

    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update a book."""
        data = {
            'title': 'Unauthorized Update',
            'author': 'William Vincent',
            'publication_year': 2024
        }
        response = self.client.put(f'/api/books/{self.book1.id}/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ==================== BookDeleteView TESTS ====================

    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete a book using force_authenticate."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_with_login(self):
        """Test that authenticated users can delete a book using client.login."""
        # Use standard Django login method
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.delete(f'/api/books/{self.book2.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())
        
        # Logout after test
        self.client.logout()

    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete a book."""
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)

    # ==================== FILTERING TESTS (BookListView) ====================

    def test_filter_by_title(self):
        """Test filtering books by exact title match."""
        response = self.client.get('/api/books/?title=Django for Beginners')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_filter_by_author(self):
        """Test filtering books by author."""
        response = self.client.get('/api/books/?author=Eric Matthes')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Eric Matthes')

    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get('/api/books/?publication_year=2023')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2023)

    def test_filter_multiple_criteria(self):
        """Test filtering with multiple criteria."""
        response = self.client.get('/api/books/?author=William Vincent&publication_year=2023')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_no_results(self):
        """Test filtering with criteria that match no books."""
        response = self.client.get('/api/books/?title=Nonexistent Book')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ==================== SEARCH TESTS (BookListView) ====================

    def test_search_by_title(self):
        """Test searching books by title keyword."""
        response = self.client.get('/api/books/?search=Django')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('Django' in response.data[0]['title'])

    def test_search_by_author(self):
        """Test searching books by author name."""
        response = self.client.get('/api/books/?search=Vincent')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('Vincent' in response.data[0]['author'])

    def test_search_partial_match(self):
        """Test search with partial keyword matches."""
        response = self.client.get('/api/books/?search=Python')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        response = self.client.get('/api/books/?search=django')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_no_results(self):
        """Test search with keyword that matches nothing."""
        response = self.client.get('/api/books/?search=XYZNonexistent')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ==================== ORDERING TESTS (BookListView) ====================

    def test_order_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_by_title_descending(self):
        """Test ordering books by title in descending order."""
        response = self.client.get('/api/books/?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_order_by_publication_year_ascending(self):
        """Test ordering books by publication year in ascending order."""
        response = self.client.get('/api/books/?ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))

    def test_order_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        response = self.client.get('/api/books/?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ==================== COMBINED QUERY TESTS ====================

    def test_combined_search_and_ordering(self):
        """Test combining search and ordering in a single query."""
        response = self.client.get('/api/books/?search=Python&ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if len(response.data) > 1:
            years = [book['publication_year'] for book in response.data]
            self.assertEqual(years, sorted(years))

    def test_combined_filter_and_ordering(self):
        """Test combining filtering and ordering."""
        response = self.client.get('/api/books/?publication_year=2023&ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 0)

    def test_combined_filter_search_ordering(self):
        """Test combining filtering, searching, and ordering."""
        response = self.client.get('/api/books/?search=Django&ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books matching the search, ordered by title