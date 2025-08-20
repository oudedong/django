from django.urls import path
from catalog import views

urlpatterns =[
    path(route='', view=views.index, name="index"),
    path(route='books/', view=views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.RenewBookInstanceView.as_view(), name='renew-bookinst'),
    
    path('author/create/', views.CreateAuthorView.as_view(), name='create-author'),
    path('author/<int:pk>/update', views.UpdateAuthorView.as_view(), name='update-author'),
    path('author/<int:pk>/delete', views.DeleteAuthorView.as_view(), name='delete-author'),

    path('book/create', views.CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>/update', views.UpdateBookView.as_view(), name='update-book'),
    path('book/<int:pk>/delete', views.DeleteBookView.as_view(), name='delete-book'),
]