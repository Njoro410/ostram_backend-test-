# Generated by Django 4.1.5 on 2023-09-25 07:45

from django.db import migrations


import uuid

def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('authentication', 'staffaccount')
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_staffaccount_uuid'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
