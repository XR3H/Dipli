# Generated by Django 3.2.12 on 2022-05-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_rename_venue_image_watch_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='image',
            field=models.ImageField(blank=True, default='images/default_watch.jpg', null=True, upload_to='images/'),
        ),
    ]
