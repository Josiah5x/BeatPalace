from django.conf import settings
from django.db import models

class Follow(models.Model):

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="engagement_following"
    )

    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="engagement_followers"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_engagement_follow"
            )
        ]

    def clean(self):

        if self.follower == self.following:

            raise ValidationError(
                "You cannot follow yourself."
            )

    def __str__(self):

        return (
            f"{self.follower.username} "
            f"follows "
            f"{self.following.username}"
        )