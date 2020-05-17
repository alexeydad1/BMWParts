# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from time import time,strftime,localtime


def get_number_invoice():
    count = Invoice.objects.filter(created_at__startswith=strftime('%Y-%m-%d', localtime(time()))).count()
    count += 1
    return "%s/%s" % (strftime('%d%m%y', localtime(time())), count)


class Supplier(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    name = models.TextField(verbose_name=u'Название', max_length=128, blank=True)

    inn = models.IntegerField(verbose_name=u'ИНН', default=0)
    ogrn = models.IntegerField(verbose_name=u'ОГРН', default=0)
    kpp = models.IntegerField(verbose_name=u'КПП', default=0)

    contact = models.TextField(verbose_name=u'Контактное лицо', max_length=256, blank=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=50, default='', blank=True)
    email = models.EmailField(verbose_name=u'E-mail', max_length=75, default='', blank=True)
    address = models.TextField(verbose_name=u'Адрес', max_length=256, blank=True)

    stock = models.ManyToManyField('catalog.Stock',verbose_name=u'Склады')

    balance = models.IntegerField(verbose_name=u'Баланс', default=0)

    class Meta:
        verbose_name = u'Поставщик'
        verbose_name_plural = u'Поставщики'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_stock_name(self):
        stock_name_list = self.stock.all()
        stock_name_str = ''
        for stock in stock_name_list:
            stock_name_str += ', ' + stock.name_stock
        return stock_name_str.lstrip(', ')
    get_stock_name.short_description = u'Склады'


class Invoice(models.Model):
    number_invoice = models.CharField(verbose_name=u'Номер', max_length=50, default=get_number_invoice, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Создан')
    status = models.PositiveIntegerField(verbose_name=u'Статус',default=0)
    supplier = models.ForeignKey('supplier.Supplier', verbose_name=u'Поставщик',null=True ,on_delete=models.SET_NULL)
    stock_sup = models.ForeignKey('catalog.Stock', verbose_name=u'Склад',null=True ,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = u'Накладная'
        verbose_name_plural = u'Накладные'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s' % self.number_invoice

    def total_invoice(self):
        total_price = 0
        for i in self.item_invoice.all():
            total_price += i.total_price_item()
        return total_price


class ItemInvoice(models.Model):
    invoice = models.ForeignKey('supplier.Invoice',related_name='item_invoice', verbose_name=u'Накладная')
    offers = models.ManyToManyField('offer.Offer',verbose_name=u'Заявки')
    orders = models.ManyToManyField('orders.Order',verbose_name=u'Заявки',null=True)
    quantity = models.PositiveIntegerField(verbose_name=u'Кол-во')
    quantity_in = models.PositiveIntegerField(verbose_name=u'Кол-во по факту',default=0)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Закупочная цена')
    product = models.ForeignKey('catalog.Product', verbose_name=u'Товар',null=True ,on_delete=models.SET_NULL)
    stock = models.ForeignKey('catalog.Stock', verbose_name=u'Склад',null=True ,on_delete=models.SET_NULL)
    brand = models.ForeignKey('catalog.ProductManufacturer', verbose_name=u'Бренд', default=1,null=True ,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = u'Позиция накладной'
        verbose_name_plural = u'Позиции накладной'
        ordering = ('invoice',)

    def __unicode__(self):
        return u'%s' % self.product

    def get_offers(self):
        offers_list = self.offers.all()
        return offers_list

    def get_orders(self):
        orders_list = self.orders.all()
        return orders_list

    get_offers.short_description = u'Заявки'

    def total_price_item(self):
        return self.quantity_in * self.purchase_price
