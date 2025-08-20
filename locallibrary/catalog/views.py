from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views import View
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.form import renew_due_back, BookForm
from django.http.response import HttpResponseRedirect
import datetime
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genre = Genre.objects.all().count()

    num_visit = request.session.get('num_visit', 0)
    num_visit += 1
    request.session['num_visit'] = num_visit

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_visit': num_visit,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 2
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 2
class AuthorDetailView(DetailView):
    model=Author
    template_name='author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)\
            .filter(status__exact='o')\
            .order_by('due_back')

class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'borrowed_bookinstance_list.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')\
            .order_by('due_back')

class RenewBookInstanceView(PermissionRequiredMixin, View):

    permission_required = 'catalog.can_mark_returned'

    def get(self, request, pk):

        default_val = datetime.date.today()+datetime.timedelta(weeks=3)

        form = renew_due_back(initial={'renew_data':default_val})
        bookinst = get_object_or_404(BookInstance, pk=pk)
        return render(request, 'renew_book_instance.html', {'form': form, 'book_instance':bookinst})
    
    def post(self, request, pk):

        form = renew_due_back(request.POST)
        bookinst = get_object_or_404(BookInstance, pk=pk)

        if form.is_valid():
            bookinst.due_back = form.cleaned_data['renew_data']
            bookinst.save()
            return HttpResponseRedirect(reverse('borrowed'))
        return render(request, 'renew_book_instance.html', {'form': form, 'book_instance':bookinst})

class CreateAuthorView(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.add_author'
    fields=['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial={'date_of_death': datetime.date.today()}
    template_name = 'createauthor.html'
class UpdateAuthorView(PermissionRequiredMixin, UpdateView):
    model = Author
    template_name = 'createauthor.html'
    permission_required = 'catalog.change_author'
    fields=['first_name', 'last_name', 'date_of_birth', 'date_of_death']
class DeleteAuthorView(PermissionRequiredMixin, DeleteView):
    model = Author
    template_name = 'deleteauthor.html'
    permission_required = 'catalog.delete_author'
    success_url = reverse_lazy('authors')
    def form_vaild(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(self.request.path)

class CreateBookView(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required='catalog.add_book'
    fields=['title', 'author', 'summary', 'isbn', 'genre', 'lang']
    template_name = 'createbook.html'
class UpdateBookView(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required='catalog.change_book'
    fields=['title', 'author', 'summary', 'isbn', 'genre', 'lang']
    template_name = 'createbook.html'
class DeleteBookView(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required='catalog.delete_book'
    template_name = 'deletebook.html'
    success_url = reverse_lazy('books')
    def form_vaild(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(self.request.path)