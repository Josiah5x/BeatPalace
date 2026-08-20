from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from music.models import Music
from collaborations.models import Collaboration


ARTIST_GROUP = "Artist"
PRODUCER_GROUP = "Producer"


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

    music_content_type = ContentType.objects.get_for_model(
        Music
    )

    upload_music = Permission.objects.get(
        content_type=music_content_type,
        codename="upload_music"
    )

    edit_music = Permission.objects.get(
        content_type=music_content_type,
        codename="edit_own_music"
    )

    delete_music = Permission.objects.get(
        content_type=music_content_type,
        codename="delete_own_music"
    )

    manage_beats = Permission.objects.get(
        content_type=music_content_type,
        codename="manage_beats"
    )

    # -----------------------------------------
    # COLLABORATION PERMISSIONS
    # -----------------------------------------

    collaboration_content_type = ContentType.objects.get_for_model(
        Collaboration
    )

    send_collaboration = Permission.objects.get(
        content_type=collaboration_content_type,
        codename="send_collaboration"
    )

    manage_collaboration = Permission.objects.get(
        content_type=collaboration_content_type,
        codename="manage_collaboration"
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