from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    Uses Django ModelForm to automatically handle validation and prevent unsafe input.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']  # match your Book model fields
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter author name'}),
            'published_date': forms.NumberInput(attrs={'placeholder': 'Enter year of publication'}),
        }
        labels = {
            'published_date': 'Year Published',
        }

    def clean_published_date(self):
        """
        Validate that the published_date is a positive integer (year).
        """
        year = self.cleaned_data.get('published_date')
        if year < 0:
            raise forms.ValidationError("Year must be a positive integer")
        return year


class SearchForm(forms.Form):
    """
    Form for searching books by title.
    """
    q = forms.CharField(
        max_length=100,
        required=False,
        label='Search Books',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title to search'})
    )
