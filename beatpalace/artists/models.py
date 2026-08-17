from django.conf import settings
from django.db import models



class ArtistProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_profile"
    )

    artist_name = models.CharField(
        max_length=100,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    avatar = models.ImageField(
        upload_to="artists/avatars/",
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="artists/covers/",
        blank=True,
        null=True
    )

    genre = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    twitter = models.URLField(
        blank=True
    )

    followers_count = models.PositiveIntegerField(
        default=0
    )

    monthly_listeners = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.artist_name or self.user.username