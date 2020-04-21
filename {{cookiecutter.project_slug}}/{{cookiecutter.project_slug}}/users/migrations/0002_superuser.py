from datetime import datetime

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from {{ cookiecutter.project_slug }}.users.models import User


def forwards_func(apps, schema_editor):
    User.objects.create_user(
        password='changeme',
        is_superuser=True,
        username='admin',
        first_name='Admin',
        last_name='Admin',
        email='{{cookiecutter.email}}',
        is_staff=True,
        is_active=True,
        name='Admin',
        cf='0000',
        is_email_validated=True,
        is_privacy_accepted=True,
    )


def reverse_func(apps, schema_editor):
    User.objects.get(username='admin').delete()



class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
