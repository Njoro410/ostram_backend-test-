# Generated by Django 4.1.5 on 2023-07-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LipaNaMpesaCallback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_request_id', models.CharField(max_length=255)),
                ('checkout_request_id', models.CharField(max_length=255)),
                ('result_code', models.IntegerField()),
                ('result_desc', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mpesa_receipt_number', models.CharField(max_length=255)),
                ('transaction_date', models.DateTimeField()),
                ('phone_number', models.CharField(max_length=255)),
            ],
        ),
    ]
