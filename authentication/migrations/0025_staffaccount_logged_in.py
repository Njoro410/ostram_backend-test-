# Generated by Django 4.1.5 on 2023-09-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0024_staffaccount_otp_base32'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffaccount',
            name='logged_in',
            field=models.BooleanField(default=False),
        ),
    ]
