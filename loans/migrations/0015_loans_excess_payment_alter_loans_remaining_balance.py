# Generated by Django 4.1.5 on 2023-06-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0014_installment_total_installment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='loans',
            name='excess_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='loans',
            name='remaining_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
