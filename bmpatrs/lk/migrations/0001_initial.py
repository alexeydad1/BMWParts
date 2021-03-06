# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 13:55
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fathername', models.CharField(blank=True, default='', max_length=50, verbose_name='Отчество')),
                ('telephone', models.CharField(max_length=32, verbose_name='Телефон')),
                ('vin', models.CharField(max_length=32, verbose_name='VIN номер автомобиля')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
