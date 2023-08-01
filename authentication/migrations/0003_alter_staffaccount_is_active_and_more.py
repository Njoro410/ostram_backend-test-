# Generated by Django 4.1.5 on 2023-07-18 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_staffaccount_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffaccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='staffaccount',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='staffaccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='staffaccount',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
