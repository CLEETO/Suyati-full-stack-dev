# Generated by Django 4.2 on 2023-06-21 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='static/images/listing1.png', upload_to=''),
        ),
    ]
