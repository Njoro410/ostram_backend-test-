# Generated by Django 4.1.5 on 2023-07-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_rename_created_at_staffaccount_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffaccount',
            name='fullname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='staffaccount',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        ),
        migrations.AlterField(
            model_name='staffaccount',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.'),
        ),
        migrations.AlterField(
            model_name='staffaccount',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.'),
        ),
    ]
