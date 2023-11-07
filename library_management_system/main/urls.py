from django.urls import path

from . import views

urlpatterns = [
    path("",                     views.home,              name="home"),
    path("add/book",             views.add_book,          name="add_book"),
    path("add/reader",           views.add_reader,        name="add_reader"),
    path("transactions",         views.view_transactions, name="view_transactions"),
    path("book/issue",           views.issue_book,        name="issue_book"),
    path("book/return",          views.return_book,       name="return_book"),
    path("search/reader",        views.search_reader,     name="search_reader"),
    path("search/book",          views.search_book,       name="search_book"),
    path("book/<str:isbn>",      views.book_details,      name="book_details"),
    path("reader/<str:user_id>", views.reader_details,    name="reader_details"),
]