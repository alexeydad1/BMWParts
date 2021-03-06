# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0006_auto_20160227_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('checked_out', models.BooleanField(default=False, verbose_name='checked out')),
            ],
            options={
                'verbose_name': 'cart',
                'ordering': ('-creation_date',),
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='unit price')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart', verbose_name='cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product', verbose_name='product')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Stock', verbose_name='stock')),
            ],
            options={
                'verbose_name': 'item',
                'ordering': ('cart',),
                'verbose_name_plural': 'items',
            },
        ),
    ]
