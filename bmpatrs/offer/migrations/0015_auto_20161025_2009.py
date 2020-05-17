# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 17:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0014_auto_20161023_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='\u0411\u0430\u043b\u0430\u043d\u0441'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d'),
        ),
        migrations.AlterField(
            model_name='itemoffer',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='\u0417\u0430\u043a\u0443\u043f\u043e\u0447\u043d\u0430\u044f \u0446\u0435\u043d\u0430'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='offer.Customer', verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.OrderStatus', verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441'),
        ),
    ]
