In [14]: book = Book.objects.filter(title="198 
    ...: 4").first()

In [15]: book.title = "Nineteen Eighty-four"   

In [16]: book.save()

In [18]: book
Out[18]: <Book: Nineteen Eighty-four by George 
Orwell (1949)>

