from bookshelf.models import Book

In [2]: book = Book.objects.create(title="1984",author="George Orwell 
   ...: ", published_date=1949)

In [3]: book
Out[3]: <Book: 1984 by George Orwell (1949)>