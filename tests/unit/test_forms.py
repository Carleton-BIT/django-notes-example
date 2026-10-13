"""Unit tests: form validation, with no database and no HTTP."""
from django.core.files.uploadedfile import SimpleUploadedFile

from notes.forms import MAX_UPLOAD_BYTES, NotebookForm, NoteForm


def test_notebook_needs_a_course_code_and_a_title():
    form = NotebookForm({'description': 'No code or title'})
    assert not form.is_valid()
    assert set(form.errors) == {'course_code', 'title'}


def test_note_needs_only_a_title():
    assert NoteForm({'title': 'Lecture 1'}).is_valid()
    assert not NoteForm({'body': 'No title'}).is_valid()


def test_note_accepts_a_pdf():
    upload = SimpleUploadedFile('slides.pdf', b'%PDF')
    form = NoteForm({'title': 'Lecture 1'}, {'attachment': upload})
    assert form.is_valid()


def test_note_rejects_a_file_type_that_is_not_allowed():
    upload = SimpleUploadedFile('page.html', b'<script></script>')
    form = NoteForm({'title': 'Lecture 1'}, {'attachment': upload})
    assert not form.is_valid()
    assert 'attachment' in form.errors


def test_note_rejects_a_file_over_the_size_limit():
    upload = SimpleUploadedFile('big.zip', b'')
    upload.size = MAX_UPLOAD_BYTES + 1
    form = NoteForm({'title': 'Lecture 1'}, {'attachment': upload})
    assert form.errors['attachment'] == ['Files can be at most 10 MB.']
