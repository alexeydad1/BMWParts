# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 13:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20160925_1625'),
        ('orders', '0010_auto_20160918_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderposition',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.ProductManufacturer', verbose_name='\u0411\u0440\u0435\u043d\u0434'),
        ),
    ]