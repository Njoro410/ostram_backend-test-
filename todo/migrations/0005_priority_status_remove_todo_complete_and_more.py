# Generated by Django 4.1.5 on 2023-08-12 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_alter_todo_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='todo',
            name='complete',
        ),
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.priority'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.status'),
        ),
    ]
