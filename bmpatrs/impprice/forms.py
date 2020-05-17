# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from .models import FilePrice
from catalog.models import Stock


class UploadFilePrice(ModelForm):
    class Meta:
        model = FilePrice
        fields = ['stock', 'import_filenames']


class UploadFileCSV(forms.Form):
    file = forms.FileField(label='Файл для загрузки')
    number = forms.IntegerField(label='№ колонки с номером запчасти')
    qty = forms.IntegerField(label='№ колонки с количеством')
    price = forms.IntegerField(label='№ колонки с ценой закупки')
    price_dealer = forms.IntegerField(label='№ колонки с ценой розница Дилера')
    margin = forms.IntegerField(label='Наценка в процентах')
    round_price = forms.IntegerField(label='Кратность округления например:"5"')
