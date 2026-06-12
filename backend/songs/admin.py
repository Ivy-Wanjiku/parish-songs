from django.contrib import admin
from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'language', 'misa_id',
        'key_signature', 'has_score', 'uploaded_by_name', 'created_at',
    ]
    list_filter = ['category', 'language', 'misa_id', 'has_score']
    search_fields = ['title', 'lyrics', 'uploaded_by_name']
    readonly_fields = ['has_score', 'uploaded_by', 'uploaded_by_name', 'created_at', 'updated_at']
