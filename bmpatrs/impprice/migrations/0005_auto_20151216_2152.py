# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impprice', '0004_auto_20151216_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='our_price',
            field=models.FloatField(verbose_name='Розничная цена НАША!!!'),
        ),
        migrations.AlterField(
            model_name='price',
            name='purchase_price',
            field=models.FloatField(verbose_name='Закупочная цена'),
        ),
        migrations.AlterField(
            model_name='price',
            name='purchase_speed_price',
            field=models.FloatField(verbose_name='Закупочная цена СР'),
        ),
        migrations.AlterField(
            model_name='price',
            name='quantity_stock_msk',
            field=models.FloatField(verbose_name='Склад МСК'),
        ),
        migrations.AlterField(
            model_name='price',
            name='quantity_stock_spb',
            field=models.FloatField(verbose_name='Склад СПБ'),
        ),
        migrations.AlterField(
            model_name='price',
            name='rrc_price',
            field=models.FloatField(verbose_name='Розницная цена дилера'),
        ),
        migrations.AlterField(
            model_name='price',
            name='sale_price',
            field=models.FloatField(verbose_name='Закупочная цена акция'),
        ),
    ]
