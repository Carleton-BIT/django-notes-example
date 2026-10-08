import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Note, Notebook

PLAIN_STATIC = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}


class SampleDataTests(TestCase):
    def test_sample_notebooks_are_loaded(self):
        self.assertEqual(Notebook.objects.count(), 2)
        self.assertTrue(Note.objects.filter(notebook__course_code='ITEC 4012').exists())


@override_settings(MEDIA_ROOT=tempfile.mkdtemp(), STORAGES=PLAIN_STATIC)
class NoteTests(TestCase):
    def setUp(self):
        self.notebook = Notebook.objects.create(course_code='TEST 1000', title='Testing')

    def test_notebook_list_shows_note_counts(self):
        Note.objects.create(notebook=self.notebook, title='First')
        response = self.client.get(reverse('notebook_list'))
        self.assertContains(response, 'TEST 1000')
        self.assertContains(response, '1 note')

    def test_create_note_with_attachment(self):
        upload = SimpleUploadedFile('lecture.txt', b'hello', content_type='text/plain')
        response = self.client.post(
            reverse('note_create', args=[self.notebook.pk]),
            {'title': 'Lecture 1', 'body': 'Intro', 'attachment': upload})
        note = Note.objects.get(title='Lecture 1')
        self.assertRedirects(response, note.get_absolute_url())
        self.assertEqual(note.notebook, self.notebook)
        self.assertEqual(note.attachment.read(), b'hello')
        self.assertEqual(note.attachment.url, '/media/attachments/lecture.txt')

    def test_rejects_file_types_that_are_not_allowed(self):
        upload = SimpleUploadedFile('page.html', b'<script></script>', content_type='text/html')
        response = self.client.post(
            reverse('note_create', args=[self.notebook.pk]), {'title': 'Bad', 'attachment': upload})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(title='Bad').exists())

    def test_htmx_search_returns_only_the_list(self):
        Note.objects.create(notebook=self.notebook, title='Joins')
        Note.objects.create(notebook=self.notebook, title='Indexes')
        response = self.client.get(self.notebook.get_absolute_url(), {'q': 'join'}, headers={'HX-Request': 'true'})
        self.assertContains(response, 'Joins')
        self.assertNotContains(response, 'Indexes')
        self.assertNotContains(response, '<html')

    def test_deleting_a_notebook_deletes_its_notes(self):
        Note.objects.create(notebook=self.notebook, title='Gone')
        response = self.client.delete(self.notebook.get_absolute_url())
        self.assertEqual(response.headers['HX-Redirect'], reverse('notebook_list'))
        self.assertFalse(Note.objects.filter(title='Gone').exists())

    def test_deleting_a_note_sends_the_browser_back_to_its_notebook(self):
        note = Note.objects.create(notebook=self.notebook, title='Gone')
        response = self.client.delete(note.get_absolute_url())
        self.assertEqual(response.headers['HX-Redirect'], self.notebook.get_absolute_url())
        self.assertFalse(Note.objects.filter(title='Gone').exists())
