# Generated by Django 3.2.12 on 2022-05-25 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_watchhasfeature_unique_watch_feature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watch',
            name='feature_list',
        ),
        migrations.AlterField(
            model_name='watchhasfeature',
            name='watch',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
