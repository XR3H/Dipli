# Generated by Django 3.2.12 on 2022-05-04 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=45)),
                ('manufacturer_country', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'brand',
            },
        ),
        migrations.CreateModel(
            name='CaseBand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_type_name', models.CharField(max_length=55)),
            ],
            options={
                'db_table': 'case_band',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='GlassType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('glass_type_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'glass_type',
            },
        ),
        migrations.CreateModel(
            name='MechanismType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mechanism_name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'mechanism_type',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(blank=True, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=45, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=12, null=True)),
                ('addit_wishes', models.TextField(blank=True, null=True)),
                ('order_address', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_state_name', models.CharField(max_length=35)),
            ],
            options={
                'db_table': 'order_state',
            },
        ),
        migrations.CreateModel(
            name='StrapType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strap_type_name', models.CharField(max_length=55)),
            ],
            options={
                'db_table': 'strap_type',
            },
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=45)),
                ('model_description', models.TextField()),
                ('model_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('case_width', models.DecimalField(decimal_places=1, max_digits=3)),
                ('case_height', models.DecimalField(decimal_places=1, max_digits=3)),
                ('case_depth', models.DecimalField(decimal_places=1, max_digits=3)),
                ('weight', models.DecimalField(decimal_places=1, max_digits=4)),
                ('backlight', models.BooleanField(default=False)),
                ('waterproof_level', models.IntegerField(blank=True, default=0, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=2)),
                ('current_amount', models.PositiveIntegerField(default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.brand')),
                ('case_band', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.caseband')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.category')),
                ('glass_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.glasstype')),
                ('mechanism_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.mechanismtype')),
                ('strap_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.straptype')),
            ],
            options={
                'db_table': 'watch',
            },
        ),
        migrations.CreateModel(
            name='OrderHasProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.watch')),
            ],
            options={
                'db_table': 'order_has_product',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='mainapp.orderstate'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
