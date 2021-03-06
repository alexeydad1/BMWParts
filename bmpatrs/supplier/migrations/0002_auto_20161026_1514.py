# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='stock_sup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Stock', verbose_name='\u0421\u043a\u043b\u0430\u0434'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.Supplier', verbose_name='\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a'),
        ),
        migrations.AlterField(
            model_name='iteminvoice',
            name='brand',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.ProductManufacturer', verbose_name='\u0411\u0440\u0435\u043d\u0434'),
        ),
        migrations.AlterField(
            model_name='iteminvoice',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Product', verbose_name='\u0422\u043e\u0432\u0430\u0440'),
        ),
        migrations.AlterField(
            model_name='iteminvoice',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Stock', verbose_name='\u0421\u043a\u043b\u0430\u0434'),
        ),
    ]
