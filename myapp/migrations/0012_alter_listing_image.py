# Generated by Django 4.2 on 2023-06-19 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='static/images/listing1.png', upload_to='static/images/list_images/'),
        ),
    ]
