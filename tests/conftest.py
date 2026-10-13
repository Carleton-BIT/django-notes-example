"""Fixtures shared by every test. pytest finds this file by its name."""
import pytest

from notes.models import Notebook


@pytest.fixture(autouse=True)
def test_storage(settings, tmp_path):
    """Save uploads in a temporary folder and serve static files without collectstatic."""
    settings.MEDIA_ROOT = tmp_path
    settings.STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }


@pytest.fixture
def notebook(db):
    return Notebook.objects.create(course_code='TEST 1000', title='Testing')
