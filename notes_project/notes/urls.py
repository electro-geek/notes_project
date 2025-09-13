from django.urls import path
from .views import NoteListCreateView, NoteDeleteView, notes_list, create_note, delete_note, register

urlpatterns = [
    # API URLs
    path('api/notes/', NoteListCreateView.as_view(), name='api_notes'),
    path('api/notes/<int:pk>/', NoteDeleteView.as_view(), name='api_delete_note'),
    
    # Template URLs
    path('', notes_list, name='notes_list'),
    path('create/', create_note, name='create_note'),
    path('delete/<int:pk>/', delete_note, name='delete_note'),
    path('register/', register, name='register'),
]
