from bookshelf.models import Book

In [32]: book = Book.objects.get(title="Ninete 
    ...: en Eighty-Four")

In [33]: book.delete()
    ...: 
Out[33]: (1, {'bookshelf.Book': 1})

In [34]: Book.objects.all()
Out[34]: <QuerySet []>

In [19]: book = Book.objects.get(title="Ninete 
    ...: en Eighty-four")

In [20]: book.delete()
Out[20]: (1, {'bookshelf.Book': 1})

In [21]: Book.objects.all()
Out[21]: <QuerySet [<Book: 1984 by George Orwell (1949)>]>