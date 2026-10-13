"""Integration tests: a request goes through the URLs, view, form, database and template.

The `client` fixture is Django's test client. It calls the views directly, so
there is no browser and no JavaScript.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from notes.models import Note, Notebook


def test_sample_notebooks_are_loaded(db):
    assert Notebook.objects.count() == 2
    assert Note.objects.filter(notebook__course_code='ITEC 4012').exists()


def test_notebook_list_shows_note_counts(client, notebook):
    Note.objects.create(notebook=notebook, title='First')
    response = client.get(reverse('notebook_list'))
    assertContains(response, 'TEST 1000')
    assertContains(response, '1 note')


def test_create_note_with_attachment(client, notebook):
    upload = SimpleUploadedFile('lecture.txt', b'hello', content_type='text/plain')
    response = client.post(
        reverse('note_create', args=[notebook.pk]),
        {'title': 'Lecture 1', 'body': 'Intro', 'attachment': upload})
    note = Note.objects.get(title='Lecture 1')
    assertRedirects(response, note.get_absolute_url())
    assert note.notebook == notebook
    assert note.attachment.read() == b'hello'
    assert note.attachment.url == '/media/attachments/lecture.txt'


def test_rejects_file_types_that_are_not_allowed(client, notebook):
    upload = SimpleUploadedFile('page.html', b'<script></script>', content_type='text/html')
    response = client.post(
        reverse('note_create', args=[notebook.pk]), {'title': 'Bad', 'attachment': upload})
    assert response.status_code == 200
    assert not Note.objects.filter(title='Bad').exists()


def test_edit_note(client, notebook):
    note = Note.objects.create(notebook=notebook, title='Draft')
    response = client.post(reverse('note_update', args=[note.pk]), {'title': 'Final', 'body': 'Done'})
    assertRedirects(response, note.get_absolute_url())
    note.refresh_from_db()
    assert note.title == 'Final'


def test_missing_notebook_is_a_404(client, db):
    response = client.get(reverse('notebook_detail', args=[999999]))
    assert response.status_code == 404


def test_htmx_search_returns_only_the_list(client, notebook):
    Note.objects.create(notebook=notebook, title='Joins')
    Note.objects.create(notebook=notebook, title='Indexes')
    response = client.get(notebook.get_absolute_url(), {'q': 'join'}, headers={'HX-Request': 'true'})
    assertContains(response, 'Joins')
    assertNotContains(response, 'Indexes')
    assertNotContains(response, '<html')


def test_deleting_a_notebook_deletes_its_notes(client, notebook):
    Note.objects.create(notebook=notebook, title='Gone')
    response = client.delete(notebook.get_absolute_url())
    assert response.headers['HX-Redirect'] == reverse('notebook_list')
    assert not Note.objects.filter(title='Gone').exists()


def test_deleting_a_note_sends_the_browser_back_to_its_notebook(client, notebook):
    note = Note.objects.create(notebook=notebook, title='Gone')
    response = client.delete(note.get_absolute_url())
    assert response.headers['HX-Redirect'] == notebook.get_absolute_url()
    assert not Note.objects.filter(title='Gone').exists()
