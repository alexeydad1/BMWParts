# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User, UserManager
# Create your models here.
class Accounts (User):
    fathername = models.CharField(verbose_name=u'Отчество', max_length=50, default='', blank=True)
    telephone = models.CharField(verbose_name=u'Телефон', max_length=32)
    cart_id = models.IntegerField(verbose_name=u'CART-ID', default=0)
    discount = models.IntegerField(verbose_name=u'Скидка', default=0)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name=u'Баланс')
    # garage=models.ForeignKey(Auto,verbose_name='Гараж')
    objects = UserManager()
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class BalanceHistoryAccounts(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
    account = models.ForeignKey('lk.Accounts', verbose_name=u'Клиент', on_delete=models.PROTECT)
    operations = models.CharField(verbose_name=u'Операция', max_length=256, blank=True)
    balance_price = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name=u'Сумма')

    class Meta:
        verbose_name = u'История баланса Клиента'
        verbose_name_plural = u'Истории балансов Клиентов'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.account

# class Auto (models.Model):
#     id_user=models.ForeignKey(User,verbose_name='Пользователь')
#     vin= models.CharField(verbose_name = u'VIN-номер автомобиля', max_length=24, default='', blank=True)
#     
#     
#     def __str__(self):
#         return str(self.vin)
#     
#     class Meta:
#         verbose_name = "VIN номер автомобиля"
#         verbose_name_plural = "VIN номера автомобилей"