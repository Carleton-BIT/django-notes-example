"""End-to-end tests: a real browser uses the site the way a student would.

The `page` fixture is a browser tab. These are the only tests that run the
JavaScript, so they are the only ones that prove the hx- attributes work.
"""
from playwright.sync_api import expect

from notes.models import Note


def test_create_a_notebook_and_add_a_note_with_a_file(page, db, tmp_path):
    lecture = tmp_path / 'lecture.txt'
    lecture.write_text('hello')

    page.goto('/')
    page.get_by_role('link', name='New notebook').click()
    page.get_by_label('Course code').fill('COMP 1405')
    page.get_by_label('Title').fill('Intro to Computer Science')
    page.get_by_role('button', name='Create notebook').click()
    expect(page.get_by_role('heading', name='COMP 1405 Intro to Computer Science')).to_be_visible()
    expect(page.get_by_text('No notes in this notebook yet.')).to_be_visible()

    page.get_by_role('link', name='Add note').click()
    page.get_by_label('Title').fill('Lecture 1')
    page.get_by_label('Body').fill('Variables and loops')
    page.get_by_label('Attachment').set_input_files(lecture)
    page.get_by_role('button', name='Save note').click()
    expect(page.get_by_role('heading', name='Lecture 1')).to_be_visible()
    expect(page.get_by_role('link', name='lecture.txt')).to_be_visible()

    page.get_by_role('link', name='Course Notes').click()
    expect(page.get_by_role('link', name='COMP 1405')).to_contain_text('1 note')


def test_a_file_type_that_is_not_allowed_shows_an_error(page, notebook, tmp_path):
    script = tmp_path / 'page.html'
    script.write_text('<script></script>')

    page.goto(f'/notebooks/{notebook.pk}/notes/new/')
    page.get_by_label('Title').fill('Bad')
    page.get_by_label('Attachment').set_input_files(script)
    page.get_by_role('button', name='Save note').click()
    expect(page.get_by_text('File extension “html” is not allowed.')).to_be_visible()
    expect(page.get_by_role('heading', name='Add note')).to_be_visible()


def test_search_filters_the_notes_while_typing(page, notebook):
    Note.objects.create(notebook=notebook, title='Joins')
    Note.objects.create(notebook=notebook, title='Indexes')

    page.goto(notebook.get_absolute_url())
    search = page.get_by_placeholder('Search this notebook')
    search.press_sequentially('join')
    expect(page.get_by_role('link', name='Joins')).to_be_visible()
    expect(page.get_by_role('link', name='Indexes')).not_to_be_visible()
    # Only the list was replaced: the page did not reload, so the text is still in the box.
    expect(search).to_have_value('join')

    search.fill('recursion')
    expect(page.get_by_text('No notes match "recursion".')).to_be_visible()


def test_delete_a_note_after_confirming(page, notebook):
    note = Note.objects.create(notebook=notebook, title='Old note')

    page.goto(note.get_absolute_url())
    page.once('dialog', lambda dialog: dialog.accept())
    page.get_by_role('button', name='Delete note').click()
    expect(page).to_have_url(notebook.get_absolute_url())
    expect(page.get_by_text('No notes in this notebook yet.')).to_be_visible()
    assert not Note.objects.filter(pk=note.pk).exists()


def test_cancelling_the_confirmation_keeps_the_notebook(page, notebook):
    Note.objects.create(notebook=notebook, title='Keep me')
    messages = []

    def cancel(dialog):
        messages.append(dialog.message)
        dialog.dismiss()

    page.goto(notebook.get_absolute_url())
    page.once('dialog', cancel)
    page.get_by_role('button', name='Delete notebook').click()
    assert messages == ['Delete this notebook and all of its notes?']
    expect(page).to_have_url(notebook.get_absolute_url())
    assert Note.objects.filter(title='Keep me').exists()
