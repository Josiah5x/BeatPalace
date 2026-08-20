from django.conf import settings
from django.db import models



class Collaboration(models.Model):

    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_collaborations"
    )

    producer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="producer_collaborations"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("completed", "Completed"),
        ],
        default="pending"
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