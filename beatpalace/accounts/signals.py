from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .permissions import setup_groups
User = get_user_model()

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


@receiver(post_save, sender=User)
def assign_user_group(
    sender,
    instance,
    created,
    **kwargs
):

    if not instance.role:
        return

    from django.contrib.auth.models import Group

    artist_group = Group.objects.filter(
        name="Artist"
    ).first()

    producer_group = Group.objects.filter(
        name="Producer"
    ).first()

    # Remove only BeatPalace role groups
    if artist_group:
        instance.groups.remove(
            artist_group
        )

    if producer_group:
        instance.groups.remove(
            producer_group
        )

    # Add correct group
    if instance.role == "artist" and artist_group:

        instance.groups.add(
            artist_group
        )

    elif instance.role == "producer" and producer_group:

        instance.groups.add(
            producer_group
        )