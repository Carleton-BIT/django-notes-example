"""Unit tests: one small piece of logic at a time, with no database and no HTTP."""
import pytest

from notes.models import Note, Notebook


def test_notebook_is_displayed_as_code_and_title():
    notebook = Notebook(course_code='ITEC 4012', title='Web Application Frameworks')
    assert str(notebook) == 'ITEC 4012 - Web Application Frameworks'


def test_attachment_name_leaves_out_the_folder():
    note = Note(attachment='attachments/lecture-1.pdf')
    assert note.attachment_name == 'lecture-1.pdf'


@pytest.mark.parametrize('filename, is_image', [
    ('diagram.png', True),
    ('photo.JPG', True),
    ('slides.pdf', False),
    ('archive.png.zip', False),
    ('README', False),
])
def test_attachment_is_image(filename, is_image):
    note = Note(attachment=f'attachments/{filename}')
    assert note.attachment_is_image == is_image
