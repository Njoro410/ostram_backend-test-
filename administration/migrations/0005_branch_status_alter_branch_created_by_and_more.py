# Generated by Django 4.1.5 on 2023-09-18 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0002_alter_residentialareas_created_on_and_more'),
        ('administration', '0004_alter_branchstatus_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='administration.branchstatus'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='created_by_on_branch', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.residentialareas'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branch_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='branch',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='updated_by_branch', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='branchstatus',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branch_status_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='branchstatus',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branch_status_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='globalcharges',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='globalCharges_instance_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='globalcharges',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='members.members'),
        ),
        migrations.AlterField(
            model_name='globalcharges',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='globalCharges_instance_updater', to=settings.AUTH_USER_MODEL),
        ),
    ]
