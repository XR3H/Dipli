# Generated by Django 3.2.12 on 2022-06-08 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0024_auto_20220608_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='locality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.locality'),
        ),
    ]