# Generated by Django 4.1.5 on 2023-05-05 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_alter_loan_type_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_type',
            name='rate',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]