from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    """
    View function for home page of site.
    """

    # Generate counts of some of the main objects 
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    num_books_with_alice = Book.objects.filter(title="Alice")

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_alice': num_books_with_alice
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = "catalog/book_list.html"



class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
