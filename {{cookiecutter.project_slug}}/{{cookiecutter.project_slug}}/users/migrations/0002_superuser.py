from datetime import datetime

from django.conf import settings
from django.db import migrations, models
from django.utils import timezone

from {{ cookiecutter.project_slug }}.users.models import User


def forwards_func(apps, schema_editor):
    now = timezone.now()
    User.objects.create_user(
        password='changeme',
        is_superuser=True,
        username='admin',
        first_name='Admin',
        last_name='Admin',
        email='paolo.fantozzi@gmail.com',
        is_staff=True,
        is_active=True,
        name='Admin',
        cf='0000',
        is_privacy_accepted=True,
        privacy_accepted_datetime=now,
        is_terms_and_conditions_accepted=True,
        terms_and_conditions_accepted_datetime=now,
        is_marketing_accepted=True,
        marketing_accepted_datetime=now,
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
