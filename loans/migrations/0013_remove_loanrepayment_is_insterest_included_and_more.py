# Generated by Django 4.1.5 on 2023-06-21 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0012_loans_installment_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanrepayment',
            name='is_insterest_included',
        ),
        migrations.RemoveField(
            model_name='loans',
            name='installment_amount',
        ),
        migrations.RemoveField(
            model_name='loans',
            name='installment_schedule',
        ),
        migrations.RemoveField(
            model_name='loans',
            name='total_installments',
        ),
        migrations.AddField(
            model_name='installment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
