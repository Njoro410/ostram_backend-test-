# Generated by Django 4.1.5 on 2023-06-21 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0008_remove_loanproduct_is_fixed_interest_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loans')),
            ],
            options={
                'db_table': 'loans_installments',
            },
        ),
        migrations.AlterField(
            model_name='loanproduct',
            name='interest_type',
            field=models.CharField(choices=[('Simple', 'Simple'), ('Compounding', 'Compounding')], max_length=50),
        ),
        migrations.DeleteModel(
            name='InterestRateChange',
        ),
    ]
