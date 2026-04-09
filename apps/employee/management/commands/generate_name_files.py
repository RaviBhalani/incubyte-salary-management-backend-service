from django.core.management.base import BaseCommand
from faker import Faker

from apps.employee.constants import (
    DATA_DIR,
    FAKER_LOCALE,
    FIRST_NAMES_COUNT,
    FIRST_NAMES_FILE,
    GENERATE_NAME_FILES_HELP,
    GENERATE_NAME_FILES_SUCCESS_MESSAGE,
    LAST_NAMES_COUNT,
    LAST_NAMES_FILE,
)


class Command(BaseCommand):
    help = GENERATE_NAME_FILES_HELP

    def handle(self, *args, **options):
        fake = Faker(FAKER_LOCALE)
        DATA_DIR.mkdir(exist_ok=True)

        first_names = {fake.first_name() for _ in range(FIRST_NAMES_COUNT * 5)}
        last_names = {fake.last_name() for _ in range(LAST_NAMES_COUNT * 5)}

        FIRST_NAMES_FILE.write_text("\n".join(sorted(first_names)[:FIRST_NAMES_COUNT]))
        LAST_NAMES_FILE.write_text("\n".join(sorted(last_names)[:LAST_NAMES_COUNT]))

        self.stdout.write(
            self.style.SUCCESS(
                GENERATE_NAME_FILES_SUCCESS_MESSAGE.format(
                    first_count=FIRST_NAMES_COUNT,
                    first_file=FIRST_NAMES_FILE,
                    last_count=LAST_NAMES_COUNT,
                    last_file=LAST_NAMES_FILE,
                )
            )
        )
