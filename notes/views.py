from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NotebookForm, NoteForm
from .models import Note, Notebook


def notebook_list(request):
    notebooks = Notebook.objects.annotate(note_count=Count('notes'))
    return render(request, 'notes/notebook_list.html', {'notebooks': notebooks})


def notebook_create(request):
    form = NotebookForm(request.POST or None)
    if form.is_valid():
        notebook = form.save()
        return redirect(notebook)
    return render(request, 'notes/notebook_form.html', {'form': form})


def notebook_detail(request, pk):
    notebook = get_object_or_404(Notebook, pk=pk)
    query = request.GET.get('q', '').strip()
    notes = notebook.notes.all()
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(body__icontains=query))
    context = {'notebook': notebook, 'notes': notes, 'query': query}
    if request.htmx:
        return render(request, 'notes/_note_list.html', context)
    return render(request, 'notes/notebook_detail.html', context)


@require_POST
def notebook_delete(request, pk):
    get_object_or_404(Notebook, pk=pk).delete()
    return redirect('notebook_list')


def note_create(request, notebook_pk):
    notebook = get_object_or_404(Notebook, pk=notebook_pk)
    form = NoteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.notebook = notebook
        note.save()
        return redirect(note)
    return render(request, 'notes/note_form.html', {'form': form, 'notebook': notebook})


def note_detail(request, pk):
    note = get_object_or_404(Note.objects.select_related('notebook'), pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


def note_update(request, pk):
    note = get_object_or_404(Note.objects.select_related('notebook'), pk=pk)
    form = NoteForm(request.POST or None, request.FILES or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect(note)
    return render(request, 'notes/note_form.html', {'form': form, 'notebook': note.notebook, 'note': note})


@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    notebook = note.notebook
    note.delete()
    return redirect(notebook)
