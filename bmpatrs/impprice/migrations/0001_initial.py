# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partnumber', models.CharField(max_length=50)),
                ('description_part', models.CharField(max_length=200)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('purchase_speed_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('rrc_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('our_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('quantity_stock_spb', models.DecimalField(decimal_places=5, max_digits=12)),
                ('quantity_stock_msk', models.DecimalField(decimal_places=5, max_digits=12)),
                ('import_filename', models.CharField(max_length=200)),
                ('import_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
