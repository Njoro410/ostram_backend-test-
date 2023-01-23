# Generated by Django 4.1.5 on 2023-01-23 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResidentialAreas',
            fields=[
                ('area_code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(blank=True, max_length=120, null=True)),
                ('mbr_no', models.IntegerField()),
                ('id_no', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=120, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=120, null=True)),
                ('next_of_kin', models.CharField(blank=True, max_length=120, null=True)),
                ('phone_nos', models.CharField(blank=True, max_length=120, null=True)),
                ('relationship', models.CharField(blank=True, max_length=120, null=True)),
                ('residential', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='members.residentialareas')),
            ],
        ),
    ]
