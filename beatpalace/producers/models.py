from django.conf import settings
from django.db import models


class ProducerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="producer_profile"
    )

    stage_name = models.CharField(max_length=150)

    bio = models.TextField(blank=True)

    studio_name = models.CharField(
        max_length=150,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    followers = models.PositiveIntegerField(
        default=0
    )

    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.stage_name