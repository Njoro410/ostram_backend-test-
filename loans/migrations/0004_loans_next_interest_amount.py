# Generated by Django 4.1.5 on 2023-06-19 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_remove_loanrepayment_late_charges_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loans',
            name='next_interest_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
