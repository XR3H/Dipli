# Generated by Django 3.2.12 on 2022-06-08 22:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0026_alter_order_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='locality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.locality'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2022, 6, 9), null=True),
        ),
    ]
