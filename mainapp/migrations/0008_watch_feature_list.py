# Generated by Django 3.2.12 on 2022-05-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_rate_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='feature_list',
            field=models.ManyToManyField(through='mainapp.WatchHasFeature', to='mainapp.Feature'),
        ),
    ]