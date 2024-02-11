# Generated by Django 3.2.12 on 2022-06-17 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0038_addtrig6'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='indication_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.indicationtype'),
        ),
        migrations.AlterField(
            model_name='watch',
            name='mechanism_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.mechanismtype'),
        ),
    ]