from django.conf import settings
from django.db import models

from django.db import models
from django.conf import settings


class Follow(models.Model):

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users_following",
        related_query_name="following_user"
    )

    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users_followers",
        related_query_name="follower_user"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="engagement_unique_follow"
            )
        ]

    def __str__(self):
        return (
            f"{self.follower.username} follows "
            f"{self.following.username}"
        )

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.follower == self.following:
            raise ValidationError(
                "You cannot follow yourself."
            )


class MusicLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="music_likes"
    )

    music = models.ForeignKey(
        "music.Music",
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "music"],
                name="unique_music_like"
            )
        ]

    def __str__(self):
        return f"{self.user} liked {self.music}"


class Comment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    music = models.ForeignKey(
        "music.Music",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}: {self.content[:30]}"