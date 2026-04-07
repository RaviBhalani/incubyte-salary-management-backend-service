from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.user.constants import (
    CREATE_SUPERUSER_HELP,
    CREATE_SUPERUSER_SUCCESS_MESSAGE,
    USER_ALREADY_EXISTS_MESSAGE,
)


class Command(BaseCommand):
    help = CREATE_SUPERUSER_HELP

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--first-name", required=True)
        parser.add_argument("--last-name", required=True)

    def handle(self, *args, **options):
        user_model = get_user_model()
        email = options["email"]

        if user_model.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(USER_ALREADY_EXISTS_MESSAGE.format(email)))
            return

        user = user_model.objects.create_superuser(
            email=email,
            password=options["password"],
        )
        user.first_name = options["first_name"]
        user.last_name = options["last_name"]
        user.save()
        self.stdout.write(self.style.SUCCESS(CREATE_SUPERUSER_SUCCESS_MESSAGE.format(email)))
