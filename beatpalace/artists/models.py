from django.conf import settings
from django.db import models


class ArtistProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_profile"
    )

    artist_name = models.CharField(
        max_length=150
    )

    bio = models.TextField(
        blank=True
    )

    followers = models.PositiveIntegerField(
        default=0
    )

    monthly_listeners = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.artist_name