# Generated by Django 4.1.5 on 2023-07-19 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_created_at_staffaccount_date_joined_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffaccount',
            name='fullname',
        ),
    ]
