# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from orders.models import OrderStatus
from .models import Accounts
from django import forms


class SingupForm(UserCreationForm):
    
    class Meta:
        model = Accounts
        fields = ['username','email','first_name', 'last_name', 'fathername', 'telephone']
        widgets = {
            'telephone': forms.TextInput(attrs={'placeholder': '+7(___) ___-__-__',
                                             'pattern': "+7([0-9]{3}) [0-9]{3}-[0-9]{2}-[0-9]{2}",
                                                'id' : "telephone"
                                         }),
        }


class FindOrderUsers(forms.Form):
    find = forms.CharField(label=u'Поиск',max_length=100,required=False)
    status = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Статусы заказов:")
    #status = forms.ModelChoiceField(queryset=OrderStatus.objects.all(),
                                    #label=u'Статусы заказов',
                                    #empty_label=None,
                                    #widget=forms.CheckboxSelectMultiple,
                                    #required=False)