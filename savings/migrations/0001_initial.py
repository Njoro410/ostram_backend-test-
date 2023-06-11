# Generated by Django 4.1.5 on 2023-06-02 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('authentication', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Savings_Account',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.basemodel')),
                ('savings_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('account_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings_account', to='members.members')),
            ],
            options={
                'db_table': 'savings_account',
            },
            bases=('authentication.basemodel',),
        ),
    ]
