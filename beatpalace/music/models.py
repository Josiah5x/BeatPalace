from django.db import models
from django.conf import settings


class Music(models.Model):

    MUSIC_TYPE_CHOICES = (
        ("song", "Song"),
        ("beat", "Beat"),
        ("demo", "Demo"),
    )

    GENRE_CHOICES = (
        ("afrobeats", "Afrobeats"),
        ("hiphop", "Hip Hop"),
        ("rnb", "R&B"),
        ("pop", "Pop"),
        ("gospel", "Gospel"),
        ("dancehall", "Dancehall"),
        ("amapiano", "Amapiano"),
        ("other", "Other"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="music_tracks"
    )

    title = models.CharField(max_length=200)

    music_type = models.CharField(
        max_length=20,
        choices=MUSIC_TYPE_CHOICES
    )

    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        default="other"
    )

    description = models.TextField(
        blank=True
    )

    audio_file = models.FileField(
        upload_to="music/audio/"
    )

    artwork = models.ImageField(
        upload_to="music/artwork/",
        blank=True,
        null=True
    )

    duration = models.PositiveIntegerField(
        default=0,
        help_text="Duration in seconds"
    )

    plays = models.PositiveIntegerField(
        default=0
    )

    is_public = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title