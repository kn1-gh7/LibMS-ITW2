from django import forms
from .models import *
from django.db.models import F

GENRE_CHOICES = (
    ("0", "Others"),
    ("1", "Fiction"),
    ("2", "Mystery"),
    ("3", "Fantasy"),
    ("4", "Horror"),
    ("5", "Nonfiction"),
    ("6", "Romance"),
    ("7", "Thriller"),
    ("8", "Science fiction"),
    ("9", "Historical fiction"),
    ("10", "Short story"),
    ("11", "Literary fiction"),
    ("12", "Poetry"),
    ("13", "Graphic novel"),
    ("14", "Biography"),
    ("15", "Young adult"),
    ("16", "Memoir"),
    ("17", "Dystopia"),
    ("18", "Magical realism"),
    ("19", "Children literature"),
    ("20", "Adventure fiction"),
    ("21", "Action fiction"),
    ("22", "Contemporary literature"),
    ("23", "Paranormal romance"),
    ("24", "Women fiction"),
    ("25", "Academic literature"),
)

class AddBookForm(forms.Form):
    isbn = forms.CharField(max_length=13, label="ISBN")
    title = forms.CharField(max_length=100, label="Title")
    author = forms.CharField(max_length=50, required=False, label="Author")
    year_published = forms.IntegerField(required=False, label="Year of Publication")
    description_text = forms.CharField(max_length=200, required=False, label="Description")
    genres = forms.MultipleChoiceField(choices = GENRE_CHOICES, help_text="<i style='font-size: small;'>Use <kbd>Ctrl+Click</kbd> to select multiple genres</i>", required=False)

class ReaderForm(forms.Form):
    name = forms.CharField(max_length=50, label="Name")

class IssueBookForm(forms.Form):
    user_id = forms.ModelChoiceField(queryset = Users.objects.all(), label="User ID")
    isbn = forms.ModelChoiceField(queryset = Books.objects.filter(librarydb__total_count__gt = F('librarydb__issued_count')), label="Book ISBN")

class ReturnBookForm(forms.Form):
    trans = forms.ModelChoiceField(queryset = BooksAndUsers.objects.all(), label="Transaction ID")

class SearchReaderForm(forms.Form):
    query = forms.CharField(max_length=100, label="Input", required=False)

class SearchBookForm(forms.Form):
    query = forms.CharField(max_length=100, label="Input", required=False)