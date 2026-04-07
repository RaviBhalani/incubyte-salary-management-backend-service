from django.contrib.auth import get_user_model
from django.db import migrations


SUPERUSERS = [
    {
        "email": "ravibhalani8@gmail.com",
        "password": "RaviBhalani8",
        "first_name": "Ravi",
        "last_name": "Bhalani",
    },
    {
        "email": "hrmanager@incubyte.com",
        "password": "HRManager@Incubyte",
        "first_name": "HR",
        "last_name": "Manager",
    },
]


def create_superusers(apps, schema_editor):
    User = get_user_model()
    for data in SUPERUSERS:
        if not User.objects.filter(email=data["email"]).exists():
            user = User.objects.create_superuser(
                email=data["email"],
                password=data["password"],
            )
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_remove_user_created_ts_remove_user_email_verified_and_more"),
    ]

    operations = [
        migrations.RunPython(create_superusers, reverse_code=migrations.RunPython.noop),
    ]
