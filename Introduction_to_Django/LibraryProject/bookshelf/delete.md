In [19]: book = Book.objects.get(title="Ninete 
    ...: en Eighty-four")

In [20]: book.delete()
Out[20]: (1, {'bookshelf.Book': 1})

In [21]: Book.objects.all()
Out[21]: <QuerySet [<Book: 1984 by George Orwell (1949)>]>