# Generated by Django 4.2 on 2023-06-18 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Model',
            new_name='MLModel',
        ),
    ]