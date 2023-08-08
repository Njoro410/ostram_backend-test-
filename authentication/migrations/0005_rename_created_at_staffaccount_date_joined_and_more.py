# Generated by Django 4.1.5 on 2023-07-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_staffaccount_groups_staffaccount_user_permissions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffaccount',
            old_name='created_at',
            new_name='date_joined',
        ),
        migrations.AddField(
            model_name='staffaccount',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='staffaccount',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]