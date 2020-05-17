# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_item_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='brand',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.ProductManufacturer', verbose_name='producer'),
        ),
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Stock', verbose_name='stock'),
        ),
    ]