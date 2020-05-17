# -*- coding: utf-8 -*-
from django.forms import ModelForm
from offer.models import Offer,Customer
from django import forms
from django.utils.translation import ugettext as _
import datetime


year = datetime.date.today().year

class OfferForm(ModelForm):

    class Meta:
        model=Offer
        fields=['status','comment','fio','phone','vin','discount','customer']
        # labels = {
        #     'status': (''),
        # }
        widgets = {
            'status': forms.Select(attrs={'style':'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                                         }),
            'customer': forms.TextInput(attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                                          }),
            'comment': forms.Textarea(
                attrs={'style': 'height:25px;;font-size: 0.8rem;border-color: #000;'
                       }),
            'fio': forms.TextInput(
                attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
            'phone': forms.TextInput(
                attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
            'vin': forms.TextInput(
                attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
            'discount': forms.TextInput(
                attrs={'class':'discount','style': 'padding:0 5px;width:25px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
        }

class CustomerForm(ModelForm):

    class Meta:
        model=Customer
        fields=['fio','phone','address','email','vin','comment']
        # labels = {
        #     'status': (''),
        # }
        widgets = {
            'status': forms.Select(attrs={'style':'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                                         }),
            'comment': forms.Textarea(
                attrs={'style': 'height:25px;;font-size: 0.8rem;border-color: #000;'
                       }),
            'fio': forms.TextInput(
                attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
            'phone': forms.TextInput(
                attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
            'vin': forms.TextInput(
                attrs={'style': 'padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
            'discount': forms.TextInput(
                attrs={'class':'discount','style': 'padding:0 5px;width:25px;height:25px;font-size: 0.8rem;border-color: #000;'
                       }),
        }


class Dateform (forms.Form):
        periodstart = forms.DateField(
        widget=forms.SelectDateWidget(
            empty_label=("Выберите год", "Выберите месяц", "Выберите день"),
        ),
    )
        periodend = forms.DateField(label=_('Birth date'), initial=datetime.date.today,
        help_text=_('Today date in 3 selects (each for day, month and year) with 100 latest years'),
        widget=forms.SelectDateWidget(years=range(year, year-20, -1)))