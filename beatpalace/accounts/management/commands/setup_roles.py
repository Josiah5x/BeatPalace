from django.core.management.base import BaseCommand

from accounts.permissions import setup_groups


class Command(BaseCommand):

    help = "Create BeatPalace Artist and Producer groups"

    def handle(self, *args, **options):

        setup_groups()

        self.stdout.write(
            self.style.SUCCESS(
                "BeatPalace Artist and Producer groups configured successfully."
            )
        )