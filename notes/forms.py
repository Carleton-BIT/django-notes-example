from django import forms

from .models import Note, Notebook

MAX_UPLOAD_BYTES = 10 * 1024 * 1024


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['course_code', 'title', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'attachment']
        widgets = {'body': forms.Textarea(attrs={'rows': 10})}

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment and attachment.size > MAX_UPLOAD_BYTES:
            raise forms.ValidationError('Files can be at most 10 MB.')
        return attachment
