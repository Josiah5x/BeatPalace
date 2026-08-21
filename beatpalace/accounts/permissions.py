from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from music.models import Music
from collaborations.models import Collaboration


ARTIST_GROUP = "Artist"
PRODUCER_GROUP = "Producer"


def get_permission(model, codename):

    content_type = ContentType.objects.get_for_model(
        model
    )

    return Permission.objects.get(
        content_type=content_type,
        codename=codename
    )


def setup_groups():

    artist_group, _ = Group.objects.get_or_create(
        name=ARTIST_GROUP
    )

    producer_group, _ = Group.objects.get_or_create(
        name=PRODUCER_GROUP
    )

    # -----------------------------------------
    # MUSIC PERMISSIONS
    # -----------------------------------------

    upload_music = get_permission(
        Music,
        "upload_music"
    )

    edit_music = get_permission(
        Music,
        "edit_own_music"
    )

    delete_music = get_permission(
        Music,
        "delete_own_music"
    )

    manage_beats = get_permission(
        Music,
        "manage_beats"
    )

    # -----------------------------------------
    # COLLABORATION PERMISSIONS
    # -----------------------------------------

    send_collaboration = get_permission(
        Collaboration,
        "send_collaboration"
    )

    manage_collaboration = get_permission(
        Collaboration,
        "manage_collaboration"
    )

    # -----------------------------------------
    # ARTIST
    # -----------------------------------------

    artist_group.permissions.set([
        upload_music,
        edit_music,
        delete_music,
        send_collaboration,
        manage_collaboration,
    ])

    # -----------------------------------------
    # PRODUCER
    # -----------------------------------------

    producer_group.permissions.set([
        upload_music,
        edit_music,
        delete_music,
        manage_beats,
        send_collaboration,
        manage_collaboration,
    ])