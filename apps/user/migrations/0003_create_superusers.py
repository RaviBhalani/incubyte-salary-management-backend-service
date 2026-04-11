import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_superusers(apps, schema_editor):
    User = get_user_model()

    email = os.environ.get("SUPERUSER_EMAIL")
    password = os.environ.get("SUPERUSER_PASSWORD")
    first_name = os.environ.get("SUPERUSER_FIRST_NAME")
    last_name = os.environ.get("SUPERUSER_LAST_NAME")

    if not all([email, password, first_name, last_name]):
        return

    if not User.objects.filter(email=email).exists():
        user = User.objects.create_superuser(email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_remove_user_created_ts_remove_user_email_verified_and_more"),
    ]

    operations = [
        migrations.RunPython(create_superusers, reverse_code=migrations.RunPython.noop),
    ]
