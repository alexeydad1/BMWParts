# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0015_auto_20161025_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemoffer',
            name='brand',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.ProductManufacturer', verbose_name='\u0411\u0440\u0435\u043d\u0434'),
        ),
        migrations.AlterField(
            model_name='itemoffer',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Product', verbose_name='\u0422\u043e\u0432\u0430\u0440'),
        ),
        migrations.AlterField(
            model_name='itemoffer',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Stock', verbose_name='\u0421\u043a\u043b\u0430\u0434'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.Customer', verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.OrderStatus', verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
    ]