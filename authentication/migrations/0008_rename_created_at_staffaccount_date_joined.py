# Generated by Django 4.1.5 on 2023-07-19 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_rename_date_joined_staffaccount_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffaccount',
            old_name='created_at',
            new_name='date_joined',
        ),
    ]
