# -*- coding: utf-8 -*- 
from django import forms

class OrderForm(forms.Form):
    f_name = forms.CharField(label='Имя')
    l_name = forms.CharField(label='Фамилия')
    address = forms.CharField(label='Адрес доставки')
    telephone = forms.CharField(label='Телефон')
    widgets = {
        'telephone': forms.TextInput(attrs={'placeholder': '+7(___) ___-__-__',
                                            'pattern': "+7([0-9]{3}) [0-9]{3}-[0-9]{2}-[0-9]{2}",
                                            'id': "telephone"
                                            }),
    }
    e_mail = forms.CharField(label='E-mail')
    commentorder= forms.CharField(label='Комментарий к заказу')