# -*- coding: utf-8 -*- 
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _

from lk.models import Accounts

class AccountsAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name',
                    'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
                'first_name', 'last_name','fathername','email' , 'telephone','cart_id','discount','balance'
            )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи" 

admin.site.unregister(User)
admin.site.register(Accounts, AccountsAdmin)