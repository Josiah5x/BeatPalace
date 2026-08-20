from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        producer_group, _ = Group.objects.get_or_create(name="Producer")

        artist_group, _ = Group.objects.get_or_create(name="Artist")

        # Producer permissions
        producer_permissions = Permission.objects.filter(
            codename__in=[
                "view_producerprofile",
                "add_producerproject",
                "change_producerproject",
                "delete_producerproject",
            ]
        )

        producer_group.permissions.set(producer_permissions)

        # Artist permissions
        artist_permissions = Permission.objects.filter(
            codename__in=[
                "view_artistprofile",
                "change_artistprofile",
            ]
        )

        artist_group.permissions.set(artist_permissions)

        self.stdout.write(self.style.SUCCESS("BeatPalace groups created successfully."))
