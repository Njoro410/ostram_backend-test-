# Generated by Django 4.1.5 on 2024-01-07 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loans',
            name='is_active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
