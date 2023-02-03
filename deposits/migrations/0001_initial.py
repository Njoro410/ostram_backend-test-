# Generated by Django 4.1.5 on 2023-02-03 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0004_alter_staff_years_in_workplace'),
        ('members', '0002_rename_residentialareas_residential_areas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposits_Account',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='administration.basemodel')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('account_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits_account', to='members.members')),
            ],
            bases=('administration.basemodel',),
        ),
    ]
