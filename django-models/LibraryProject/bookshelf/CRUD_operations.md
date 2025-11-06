# CREATE

from bookshelf.models import Book

In [2]: book = Book.objects.create(title="1984",author="George Orwell 
   ...: ", published_date=1949)

In [3]: book
Out[3]: <Book: 1984 by George Orwell (1949)>

# RETRIEVE

books = Book.objects.all()

In [25]: book = Book.objects.get(title="1984")

In [26]: book.title, book.author, book.published_date
Out[26]: ('1984', 'George Orwell', 1949)


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

# UPDATE

book = Book.objects.get(title="1984") 
    ...: 

In [29]: book.title = "Nineteen Eighty-Four"   

In [30]: book.save()

In [31]: book
Out[31]: <Book: Nineteen Eighty-Four by George 
Orwell (1949)>

In [14]: book = Book.objects.filter(title="198 
    ...: 4").first()

In [15]: book.title = "Nineteen Eighty-four"   

In [16]: book.save()

In [18]: book
Out[18]: <Book: Nineteen Eighty-four by George 
Orwell (1949)>

# DELETE

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