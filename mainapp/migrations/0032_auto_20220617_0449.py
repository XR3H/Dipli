# Generated by Django 3.2.12 on 2022-06-17 01:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0031_alter_orderhasproduct_noted_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='add_date',
            field=models.DateField(default=datetime.date(2022, 6, 17)),
        ),
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2022, 6, 17), null=True),
        ),
    ]