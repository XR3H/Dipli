# Generated by Django 3.2.12 on 2022-05-29 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_remove_order_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='mainapp.paymenttype'),
        ),
    ]
