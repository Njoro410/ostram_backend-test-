# Generated by Django 4.1.5 on 2024-01-04 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deposits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawDeposits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawn_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('withdrawn_date', models.DateField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depositsminus', to='deposits.depositsaccount')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='depositsminus_instance_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='depositsminus_instance_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='WidthdrawDeposits',
        ),
    ]
