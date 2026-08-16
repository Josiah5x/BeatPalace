from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from producers.models import ProducerProfile
from artists.models import ArtistProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.role == "producer":

        ProducerProfile.objects.create(
            user=instance,
            stage_name=instance.username
        )

    elif instance.role == "artist":

        ArtistProfile.objects.create(
            user=instance,
            artist_name=instance.username
        )