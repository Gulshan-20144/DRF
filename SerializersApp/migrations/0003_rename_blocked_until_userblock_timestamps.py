# Generated by Django 4.2.11 on 2024-06-27 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SerializersApp', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userblock',
            old_name='blocked_until',
            new_name='timestamps',
        ),
    ]
