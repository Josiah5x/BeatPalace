from django.contrib import admin
from .models import Music


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "music_type",
        "genre",
        "plays",
        "is_public",
        "created_at",
    )

    list_filter = (
        "music_type",
        "genre",
        "is_public",
    )

    search_fields = (
        "title",
        "owner__username",
    )