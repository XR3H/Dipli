# Generated by Django 3.2.12 on 2022-06-07 22:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0023_alter_rate_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality_name', models.CharField(max_length=75)),
            ],
            options={
                'db_table': 'locality',
            },
        ),
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2022, 6, 8), null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='locality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.locality'),
        ),
    ]