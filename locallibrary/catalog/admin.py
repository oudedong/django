from django.contrib import admin
from catalog.models import Author, Book, BookInstance, Genre, Language
# Register your models here.

#admin.site.register([Author, Book, BookInstance, Genre, Language])
admin.site.register([Genre, Language])

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
class AuthorInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ('last_name', 'first_name', ('date_of_birth', 'date_of_death'))
    inlines = [AuthorInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('id', 'book', 'imprint', 'status', 'borrower', 'due_back')
    fieldsets = (
        (None,
            {'fields':('id', 'book', 'imprint')}
        ),
        ('Available',
            {'fields':('borrower', 'status', 'due_back')}
        )
    )