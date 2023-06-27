# Generated by Django 4.1.5 on 2023-06-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0007_loans_total_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanproduct',
            name='is_fixed_interest',
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='interest_type',
            field=models.CharField(choices=[('Simple Interest', 'Simple Interest'), ('Compounding Interest', 'Compounding Interest')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
