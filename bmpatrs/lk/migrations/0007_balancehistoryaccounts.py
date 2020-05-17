# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-23 13:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20170423_1621'),
        ('lk', '0006_accounts_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceHistoryAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('operations', models.CharField(blank=True, max_length=256, verbose_name='\u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044f')),
                ('balance_price', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='\u0421\u0443\u043c\u043c\u0430')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lk.Accounts', verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.Order', verbose_name='\u0417\u0430\u043a\u0430\u0437')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0431\u0430\u043b\u0430\u043d\u0441\u0430 \u041a\u043b\u0438\u0435\u043d\u0442\u0430',
                'verbose_name_plural': '\u0418\u0441\u0442\u043e\u0440\u0438\u0438 \u0431\u0430\u043b\u0430\u043d\u0441\u043e\u0432 \u041a\u043b\u0438\u0435\u043d\u0442\u043e\u0432',
            },
        ),
    ]