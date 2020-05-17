# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-08 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20161026_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'permissions': (('can_purchase_price', '\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0437\u0430\u043a\u0443\u043f\u043e\u0447\u043d\u0443\u044e \u0446\u0435\u043d\u0443'), ('can_id_stock', '\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0421\u043a\u043b\u0430\u0434'), ('can_price_dealer', '\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0446\u0435\u043d\u0443 \u0434\u0438\u043b\u0435\u0440\u0430')), 'verbose_name': '\u0426\u0435\u043d\u0430', 'verbose_name_plural': '\u0426\u0435\u043d\u044b'},
        ),
        migrations.AddField(
            model_name='price',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d'),
        ),
        migrations.AddField(
            model_name='price',
            name='dealer_price',
            field=models.DecimalField(decimal_places=2, max_digits=18, null=True, verbose_name='\u0420\u043e\u0437\u043d\u0438\u0447\u043d\u0430\u044f \u0446\u0435\u043d\u0430 \u0414\u0438\u043b\u0435\u0440\u0430'),
        ),
    ]
