# Generated by Django 4.1.5 on 2023-06-19 06:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0002_rename_residential_areas_residentialareas'),
        ('deposits', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Deposits_Account',
            new_name='DepositsAccount',
        ),
    ]
