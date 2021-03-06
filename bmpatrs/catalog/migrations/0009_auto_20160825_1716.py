# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-25 14:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_crossproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='BMW', max_length=128, verbose_name='Название')),
                ('margin', models.IntegerField(default=0, verbose_name='Наценка')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.ProductManufacturer'),
        ),
    ]
