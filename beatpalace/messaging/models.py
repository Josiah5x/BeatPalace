from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Conversation(models.Model):

    collaboration = models.OneToOneField(
        "collaborations.Collaboration",
        on_delete=models.CASCADE,
        related_name="conversation",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"Conversation - "
            f"{self.collaboration.artist.username} & "
            f"{self.collaboration.producer.username}"
        )





def validate_audio_file(value):
    allowed_extensions = {
        ".mp3",
        ".wav",
        ".flac",
        ".m4a",
        ".aac",
        ".ogg",
    }

    extension = Path(value.name).suffix.lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Only MP3, WAV, FLAC, M4A, AAC and OGG audio files are allowed."
        )


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    message = models.TextField(
        blank=True
    )

    audio = models.FileField(
        upload_to="messages/audio/%Y/%m/",
        null=True,
        blank=True,
        validators=[validate_audio_file],
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        if self.message:
            return (
                f"{self.sender.username}: "
                f"{self.message[:40]}"
            )

        if self.audio:
            return (
                f"{self.sender.username}: "
                f"{self.audio.name}"
            )

        return f"{self.sender.username}: Audio message"