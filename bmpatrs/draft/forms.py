# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from draft.models import ItemD,Draft



class DraftPlus(ModelForm):

    class Meta:
        model=ItemD
        fields=['draft']
        labels = {
            'draft': (''),
        }
        widgets = {
            'draft': forms.Select(attrs={'placeholder': u'Выберите черновик',
                                         'style':'min-width:185px;padding:0 5px;height:25px;font-size: 0.8rem;border-color: #000;'
                                         }),
        }

