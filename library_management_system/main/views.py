from django.shortcuts import render, redirect
from .forms import * 
from .models import *
from datetime import datetime
from django.db.models import Q 

# Create your views here.
def home(request):
    return render(request, "home.html")

def add_book(request):
    message = None
    form = AddBookForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            isbn = data['isbn']
            t, is_created = Books.objects.get_or_create(
                ISBN=isbn,
                defaults={"title": data["title"], "author":data["author"], "year_published": data["year_published"], "description_text": data["description_text"]}
            )
            t.save()
            obj, obj_created = LibraryDB.objects.get_or_create(
                book_isbn=t,
                defaults={'total_count': 0, 'issued_count': 0}
            )
            obj.total_count += 1
            obj.save()
            if is_created == True:
                for i in data['genres']:
                    BookGenres(book_ISBN=t, genres=Genres.objects.get(label=int(i))).save()
            message = isbn
    return render(request, "addbook.html", {'form': form, 'message': message})

def add_reader(request):
    message = None
    form = ReaderForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            t = Users(name=form.cleaned_data['name'])
            t.save()
            message = t.user_id
    return render(request, "addreader.html", {'form': form, 'message':message})

def view_transactions(request):
    obj = Transactions.objects.all()
    return render(request, "transactions.html", {'obj': obj[::-1]})

def issue_book(request):
    message = None
    exists = None
    form = IssueBookForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            isbn = data['isbn']
            user_id = data['user_id']
            t = Transactions(
                trans_type = TransactionTypes.objects.get(t_type=1), 
                trans_time = datetime.now(), 
                the_user_id = user_id,
                book_id = isbn
            )
            t.save()
            obj = BooksAndUsers(
                t_id = t,
                book_id = isbn,
                user_id = user_id,
            )
            obj.save()
            d = LibraryDB.objects.get(book_isbn=isbn)
            d.issued_count += 1
            d.save()
            message = f"Book with ISBN {t.book_id} issued to {t.the_user_id} at {t.trans_time} with transaction ID {t.pk}"
    return render(request, "issuebook.html", {'form': form, 'message': message, 'exists': exists})

def return_book(request):
    message = None
    form = ReturnBookForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            obj = data['trans']
            t = Transactions(
                trans_type = TransactionTypes.objects.get(t_type=2), 
                trans_time = datetime.now(), 
                the_user_id = obj.user_id,
                book_id = obj.book_id
            )
            t.save()
            d = LibraryDB.objects.get(book_isbn=obj.book_id)
            d.issued_count -= 1
            d.save()
            obj.delete()
            message = t
    return render(request, 'returnbook.html', {'form':form, 'message': message})

def search_reader(request):
    obj = None
    form = SearchReaderForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            t = request.POST["query"]
            if t == "":
                obj = Users.objects.all()
            else:
                obj = Users.objects.filter(name__icontains=request.POST['query'])
    return render(request, 'search_reader.html', {'form': form, 'obj': obj})

def search_book(request):
    obj = None
    form = SearchBookForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid:
            t = request.POST["query"]
            if t == "":
                obj = Books.objects.all()
            else:
                obj = Books.objects.filter(Q(ISBN__icontains=request.POST['query']) | Q(title__icontains=request.POST['query']) | Q(author__icontains=request.POST['query']) | Q(description_text__icontains=request.POST['query']))
    return render(request, 'search_book.html', {'form': form, 'obj': obj})

def book_details(request, isbn):
    try:
        obj = Books.objects.get(ISBN=isbn)
    except:
        obj = None
    try:
        obj1 = LibraryDB.objects.get(book_isbn=isbn)
        available = obj1.total_count - obj1.issued_count
    except:
        obj1 = None
    try:
        obj2 = BooksAndUsers.objects.filter(book_id=isbn)
    except:
        obj2 = None
    try:
        obj3 = BookGenres.objects.filter(book_ISBN=isbn)
    except:
        obj3 = None
    try:
        arr = []
        for i in obj3:
            arr.append(i.genres.categories)
        print(arr)
    except:
        arr = None
    return render(request, 'book_details.html', {'obj': obj, 'obj1': obj1, 'available': available, 'obj2': obj2, 'arr': arr})

def reader_details(request, user_id):
    try:
        obj = Users.objects.get(user_id=user_id)
    except:
        obj = None
    try:
        obj1 = BooksAndUsers.objects.filter(user_id=user_id)
    except:
        obj1 = None
    try:
        obj2 = Transactions.objects.filter(the_user_id=user_id).filter(trans_type=TransactionTypes.objects.get(t_type=1))
    except:
        obj2 = None
    return render(request, 'reader_details.html', {'obj': obj, 'obj1': obj1, 'obj2': obj2})