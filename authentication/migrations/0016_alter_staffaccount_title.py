# Generated by Django 4.1.5 on 2023-09-25 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_staffaccount_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffaccount',
            name='title',
            field=models.CharField(blank=True, choices=[('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Ms.')], max_length=150, null=True),
        ),
    ]