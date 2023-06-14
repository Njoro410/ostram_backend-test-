# Generated by Django 4.1.5 on 2023-06-13 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(blank=True, choices=[('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')], max_length=60, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='DocumentStatus_instance_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='DocumentStatus_instance_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'document_status',
            },
        ),
    ]
