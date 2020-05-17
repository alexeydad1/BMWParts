# -*- coding: utf-8 -*-
from django.db import models
from decimal import *

# Create your models here.



class Offer(models.Model):
    comment = models.TextField(verbose_name=u'Комментарий', max_length=512, blank=True)
    # В последствии удлаить поле FIO кго замена customer
    fio = models.TextField(verbose_name=u'Ф.И.О', max_length=128, blank=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=50, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    closed_at = models.DateTimeField(verbose_name='Закрыт', blank=True, null=True)
    # Удалил поле с пользователем
    vin = models.CharField(verbose_name=u'VIN автомобиля',max_length=50,default='',blank=True)
    discount = models.PositiveIntegerField(verbose_name = u'Скидка', default=0)
    status = models.ForeignKey('orders.OrderStatus',verbose_name=u'Статус',default=1,null=True ,on_delete=models.SET_NULL)
    customer = models.ForeignKey('offer.Customer', verbose_name=u'Клиент', blank=True, null=True ,on_delete=models.SET_NULL)
    aw_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=u'Цена', default=0.0)

    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.pk

    def price_offer(self):
        total_price = 0
        for p in self.positions_offer.all():
            total_price += p.total_price_offer()
        return total_price

    def price_offer_purhase(self):
        total_price = 0
        for p in self.positions_offer.all():
            total_price += p.total_price_offer_purchase()
        return total_price

    def price_works(self):
        total_price = 0
        for p in self.positions_works_offer.all():
            total_price += p.unit_price
        return total_price

    def price_all_offer(self):
        total_price = self.price_offer() + self.price_works()
        return total_price


class ItemOffer(models.Model):
    offer = models.ForeignKey(Offer, related_name='positions_offer', verbose_name=u'Заявка')
    quantity = models.PositiveIntegerField(verbose_name=u'Кол-во')
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=u'Цена')
    unit_price_discount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=u'Цена', default=Decimal(0))
    purchase_price = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name=u'Закупочная цена')
    product = models.ForeignKey('catalog.Product', verbose_name=u'Товар',null=True ,on_delete=models.SET_NULL)
    stock = models.ForeignKey('catalog.Stock', verbose_name=u'Склад',null=True ,on_delete=models.SET_NULL)
    brand = models.ForeignKey('catalog.ProductManufacturer', verbose_name=u'Бренд', default=1,null=True ,on_delete=models.SET_NULL)
    invoice = models.ForeignKey('supplier.Invoice', verbose_name=u'Накладная', null=True ,on_delete=models.SET_NULL)
    status_offer = models.PositiveIntegerField(verbose_name=u'Статус запчасти',default=0)

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Позиции'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price_offer(self):
        return self.quantity * self.unit_price_discount

    def total_price_offer_purchase(self):
        return self.quantity * self.purchase_price


class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    fio = models.TextField(verbose_name=u'Ф.И.О', max_length=128, blank=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=50, default='', blank=True)
    email = models.EmailField(verbose_name=u'E-mail', max_length=75, default='', blank=True)
    vin = models.CharField(verbose_name=u'VIN автомобиля', max_length=50, default='', blank=True)
    address = models.TextField(verbose_name=u'Адрес', max_length=256, blank=True)
    comment = models.TextField(verbose_name=u'Комментарий', max_length=256, blank=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name=u'Баланс')
   #Удалил поле с пользователем

    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        ordering = ('fio',)

    def __unicode__(self):
        return u'%s' % self.fio

    def all_new_offer(self):
        offers = ItemOffer.objects.select_related().filter(offer__customer=self,offer__status=1)
        total = 0
        for offer in offers:
            total += offer.total_price_offer()
        return total


class BalanceHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата')
    customer = models.ForeignKey('offer.Customer', verbose_name=u'Клиент',null=True ,on_delete=models.PROTECT)
    operations = models.CharField(verbose_name=u'Операция', max_length=256, blank=True)
    balance_price = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name=u'Сумма')

    class Meta:
        verbose_name = u'История баланса'
        verbose_name_plural = u'Истории балансов'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.customer


class Works(models.Model):
    number = models.CharField(verbose_name=u'Номер запчасти',max_length=128,primary_key=True)# номер работы
    name = models.CharField(verbose_name=u'Название работы', max_length=256,blank=True)# наименование работы


    class Meta:
        verbose_name = u'Работа СТО'
        verbose_name_plural = u'Работы СТО'
        ordering = ('-number',)

    def __unicode__(self):
        return u'%s' % self.name


class WorkOffer(models.Model):
    offer = models.ForeignKey(Offer,related_name='positions_works_offer',verbose_name=u'Заявка')
    work = models.ForeignKey(Works,verbose_name=u'Работа')
    aw = models.PositiveIntegerField(verbose_name=u'AW',default=0)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=u'Цена',default=0.0)


    class Meta:
        verbose_name = u'Работа'
        verbose_name_plural = u'Работы'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.work

