from django.urls import path 

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'), 
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='book-delete'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name='author-delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowedbooks/', views.LoanedBooksListView.as_view(), name='borrowed-books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]