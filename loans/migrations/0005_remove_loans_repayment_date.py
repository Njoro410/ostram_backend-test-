# Generated by Django 4.1.5 on 2023-05-05 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_remove_loans_repaid_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loans',
            name='repayment_date',
        ),
    ]
