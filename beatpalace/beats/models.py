from django.conf import settings
from django.db import models


class Beat(models.Model):

    producer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="beats"
    )

    title = models.CharField(
        max_length=200
    )

    cover = models.ImageField(
        upload_to="beats/covers/",
        blank=True,
        null=True
    )

    audio = models.FileField(
        upload_to="beats/audio/"
    )

    genre = models.CharField(
        max_length=100
    )

    bpm = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    musical_key = models.CharField(
        max_length=20,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    exclusive_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    streams = models.PositiveIntegerField(
        default=0
    )

    likes = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

class Song(models.Model):

    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="songs"
    )

    beat = models.ForeignKey(
        Beat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="songs"
    )

    title = models.CharField(
        max_length=200
    )

    artwork = models.ImageField(
        upload_to="songs/artwork/",
        blank=True,
        null=True
    )

    audio = models.FileField(
        upload_to="songs/audio/"
    )

    streams = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title