# Generated by Django 4.1.5 on 2023-07-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authentication', '0003_alter_staffaccount_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffaccount',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_groups', to='auth.group'),
        ),
        migrations.AddField(
            model_name='staffaccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_permissions', to='auth.permission'),
        ),
    ]
