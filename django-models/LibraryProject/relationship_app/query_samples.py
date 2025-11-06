from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def get_books_by_author(author_name):
    """
    Return all books written by a given author name.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return f"No author found with the name '{author_name}'"


# 2️⃣ List all books in a specific library
def get_books_in_library(library_name):
    """
    Return all books available in the given library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return f"No library found with the name '{library_name}'"


# 3️⃣ Retrieve the librarian for a given library
def get_librarian_for_library(library_name):
    """
    Return the librarian assigned to a specific library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except Library.DoesNotExist:
        return f"No library found with the name '{library_name}'"
    except Librarian.DoesNotExist:
        return f"No librarian assigned to '{library_name}'"

def retrieve_librarian_for_library(library_name):
    """
    Return the librarian assigned to a specific library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except Library.DoesNotExist:
        return f"No library found with the name '{library_name}'"
    except Librarian.DoesNotExist:
        return f"No librarian assigned to '{library_name}'"
    
def display_results():
    print("Books by George Orwell:")
    for book in get_books_by_author("George Orwell"):
        print(f"- {book.title}")

    print("\nBooks in City Library:")
    for book in get_books_in_library("City Library"):
        print(f"- {book.title}")

    print("\nLibrarian for City Library:")
    print(get_librarian_for_library("City Library"))
