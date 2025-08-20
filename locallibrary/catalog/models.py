from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.conf import settings
from datetime import date

# Create your models here.
class Genre(models.Model):
    
    name = models.CharField(max_length=20, help_text="Enter a book genre")

    def __str__(self):
        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True, blank=True)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    lang = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        genres = self.genre.all()
        if len(genres)>3:
            genres = genres[:3] + [Genre(name='...')]
        return ','.join([genre.name for genre in genres])

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    @property
    def is_overdue(self):
        return bool(self.due_back and self.due_back < date.today())

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    
    lang = models.CharField(max_length=2)

    class Meta:
        ordering = ['-lang']
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower('lang'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('language-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.lang