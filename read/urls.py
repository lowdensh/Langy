from . import views
from django.urls import path


app_name = 'read'
urlpatterns = [
    path('books', views.books, name='books'),

    path('<int:book_id>/details', views.details, name='details'),
    path('<int:book_id>/start-read', views.start_read, name='start_read'),
    path('<int:book_id>/<int:langy_session_id>/close-book', views.close_book, name='close_book'),
    path('<int:book_id>/<int:langy_session_id>', views.read, name='read'),

    path('<int:book_id>/pages/manage', views.pages_manage, name='pages_manage'),
    path('<int:book_id>/pages/generate', views.pages_generate, name='pages_generate'),
    path('<int:book_id>/pages/save', views.pages_save, name='pages_save'),
    
    path('<int:book_id>/words/manage', views.words_manage, name='words_manage'),
    path('<int:book_id>/words/generate', views.words_generate, name='words_generate'),
    path('<int:book_id>/words/save', views.words_save, name='words_save'),
]
