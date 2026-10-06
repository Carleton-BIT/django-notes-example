from pathlib import Path

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp']
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS + ['pdf', 'txt', 'md', 'docx', 'pptx', 'xlsx', 'zip']


class Notebook(models.Model):
    course_code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course_code', 'title']

    def __str__(self):
        return f'{self.course_code} - {self.title}'

    def get_absolute_url(self):
        return reverse('notebook_detail', args=[self.pk])


class Note(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to='attachments/',
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)],
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', args=[self.pk])

    @property
    def attachment_name(self):
        return Path(self.attachment.name).name

    @property
    def attachment_is_image(self):
        return Path(self.attachment.name).suffix.lower().lstrip('.') in IMAGE_EXTENSIONS
