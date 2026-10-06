from django.contrib import admin

from .models import Note, Notebook


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    fields = ['title', 'attachment']


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'title', 'created']
    inlines = [NoteInline]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'notebook', 'updated']
    list_filter = ['notebook']
    search_fields = ['title', 'body']
