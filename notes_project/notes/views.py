from rest_framework import generics, permissions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Note
from .serializer import NoteSerializer

# API Views
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDeleteView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

# Template Views
@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/notes_list.html', {'notes': notes})

@login_required
def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            messages.success(request, 'Note created successfully!')
            return redirect('notes_list')
        else:
            messages.error(request, 'Please fill in both title and content.')
    return render(request, 'notes/create_note.html')

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes_list')
    return render(request, 'notes/confirm_delete.html', {'note': note})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('notes_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
