from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "archived", "updated_at", "created_at")
    list_filter = ("archived",)
    search_fields = ("title", "content", "tags")
