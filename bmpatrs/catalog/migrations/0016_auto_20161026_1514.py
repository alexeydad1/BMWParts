# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_productmanufacturer_alt_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='id_stock',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Stock', verbose_name='\u0421\u043a\u043b\u0430\u0434'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.ProductCategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.ProductManufacturer'),
        ),
    ]