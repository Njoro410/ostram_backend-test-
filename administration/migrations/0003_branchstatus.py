# Generated by Django 4.1.5 on 2023-09-18 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration', '0002_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], max_length=200)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='branch_status_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='branch_status_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'branch_status',
            },
        ),
    ]