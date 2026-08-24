from django.conf import settings
from django.db import models


class Collaboration(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_collaborations",
    )

    producer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="producer_collaborations",
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        permissions = [
            (
                "send_collaboration",
                "Can send collaboration requests"
            ),
            (
                "manage_collaboration",
                "Can manage collaborations"
            ),
        ]

    def __str__(self):

        return (
            f"{self.artist.username} → "
            f"{self.producer.username}"
        )