# Generated by Django 3.2.12 on 2022-05-25 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_delete_watchhasfeature'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchHasFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.feature')),
                ('watch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.watch')),
            ],
            options={
                'db_table': 'watch_has_feature',
                'unique_together': {('watch', 'feature')},
            },
        ),
    ]
