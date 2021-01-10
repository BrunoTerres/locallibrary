import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#require login to function based view
from django.contrib.auth.decorators import login_required, permission_required
#require login to class based view
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm


def index(request):
    """
    View function for home page of site.
    """

    # Generate counts of some of the main objects 
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Process the data in form.cleaned_data as required (here we just write it to the model due_back field).
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-books'))
    # If this is a GET (or any other method) create the default form
    else: 
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = "catalog/book_list.html"
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = "catalog/author_list.html"


class AuthorDetailView(generic.DetailView):
    """
    Generic class-based detail view for an author.
    """
    model = Author
    template_name = "catalog/author_detail.html"


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user
    """
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 4

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = "catalog/bookinstance_list_borrowed.html"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
