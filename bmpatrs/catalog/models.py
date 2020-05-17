# -*- coding: utf-8 -*- 
from django.db import models
from time import time,strftime,localtime

def get_upload_file_name(instance,filename):
    ext = filename.split('.')[-1]
    filename = 'img/products/{}_{}.{}'.format(instance.partnumber,strftime('%d%m%Y', localtime(time())), ext)
    return filename


class ProductManufacturer(models.Model):
    name = models.CharField(verbose_name=u'Название',max_length=128,default='BMW')
    margin = models.IntegerField(verbose_name=u'Наценка', default=0)
    alt_name = models.CharField(verbose_name=u'Альтернативные названия', max_length=256, default='')

    class Meta:
        verbose_name = u'Производитель'
        verbose_name_plural = u'Производители'

    def __unicode__(self):
        return u'%s' % self.name


class ProductCategory(models.Model):
    name = models.CharField(verbose_name=u'Название',max_length=128)

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def __unicode__(self):
        return u'%s' % self.name


class Product(models.Model):
    partnumber = models.CharField(verbose_name=u'Номер запчасти',max_length=128)# номер запчасти
    description = models.TextField(verbose_name=u'Описание запчасти')# описание запчасти
    create_date = models.DateTimeField(u'Дата создания',auto_now=True)# Дата последнего изменения
    category = models.ForeignKey('catalog.ProductCategory',null=True ,on_delete=models.SET_NULL)# Категория товара
    producer = models.ForeignKey('catalog.ProductManufacturer',null=True ,on_delete=models.SET_NULL,default=1)# производитель
    image = models.ImageField(verbose_name=u'Фото товара',upload_to=get_upload_file_name,height_field=None, width_field=None,null=True,blank=True)


    def __unicode__(self):
        return u'%s' % self.partnumber

    def bit(self):
        if self.image:
            return u'<img src="%s" width="70"/>' % self.image.url
        else:
            return u'(none)'

    bit.short_descriptio = u'Изображение'
    bit.allow_tags = True

    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'


class CrossProduct(models.Model):
    productnumber = models.CharField(verbose_name=u'Номер запчасти',max_length=128)# номер запчасти
    crossnumber = models.TextField(verbose_name=u'Кросс Номера')# кросс номера через "---"

    def __unicode__(self):
        return u'%s' % self.productnumber

    class Meta:
        verbose_name = u'Кросс Номер'
        verbose_name_plural = u'Кросс Номера'


class Price(models.Model):   
   
    p_product = models.CharField(verbose_name=u'Номер запчасти',max_length=50,default=1)# номер зачасти
    id_stock = models.ForeignKey('catalog.Stock',null=True ,on_delete=models.SET_NULL,verbose_name=u'Склад',default=1)# id склада
    qty = models.IntegerField(verbose_name=u'Колчество')# Количество на складе
    
    purchase_price = models.DecimalField(max_digits=18, decimal_places=2,verbose_name=u'Закупочная цена',null=False)# Закупочная цена
    our_price = models.DecimalField(max_digits=18, decimal_places=2,verbose_name=u'Розничная цена НАША!!!')# Розничная цена НАША!!!!!!

    brand = models.CharField(verbose_name=u'Бренд', max_length=50, default='BMW')
    dealer_price = models.DecimalField(max_digits=18, decimal_places=2,verbose_name=u'Розничная цена Дилера',null=True)
    # Розничная цена Дилера
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'Обновлен',null=True)

    class Meta:
        permissions = (
                # Идентификатор права       Описание права
                ("can_purchase_price", "Показывать закупочную цену"),
                ("can_id_stock", "Показывать Склад"),
                ("can_price_dealer", "Показывать цену дилера"),

            )
        verbose_name = u'Цена'
        verbose_name_plural = u'Цены'
    
    def __unicode__(self):
        return u'%s' % self.p_product


class Stock(models.Model):
    name_stock = models.CharField(verbose_name=u'Название',max_length=128)# Название склада
    delivery_time = models.IntegerField(verbose_name=u'Время доставки')# Время доставки
    color_stock = models.CharField(verbose_name=u'Цвет',default='black',max_length=128)# Цвет склада
    delivery_comment = models.CharField(verbose_name=u'Комментарии по срокам поставки', default='', max_length=128)  # Комментарии по срокам достаки


    class Meta:
        verbose_name = u'Склад'
        verbose_name_plural = u'Склады'
    
    def __unicode__(self):
        return u'%s' % self.name_stock