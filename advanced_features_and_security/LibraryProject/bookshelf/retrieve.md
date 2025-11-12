books = Book.objects.all()

In [25]: book = Book.objects.get(title="1984")

In [26]: book.title, book.author, book.published_date
Out[26]: ('1984', 'George Orwell', 1949)

In [23]: books
Out[23]: <QuerySet [<Book: 1984 by George Orwell (1949)>]>

In [4]: from bookshelf.models import Book      

In [5]: books = Book.objects.all()

In [6]: books
Out[6]: <QuerySet [<Book: 1984 by George Orwell (1949)>, <Book: 1984 by George Orwell (1949)>]>

In [9]: for b in books:
   ...:     print(b)
   ...: 
1984 by George Orwell (1949)
1984 by George Orwell (1949)

In [10]: book = Book.objects.filter(title="198 
    ...: 4").first()

In [11]: book
Out[11]: <Book: 1984 by George Orwell (1949)>