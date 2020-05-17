# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib import auth
from cart.Cart import Cart


def custom_proc(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username
    return args


def ContactsPage(request):
    args = custom_proc(request)
    return render(request,"staticpage/contacts.html",args)


def SalePage(request):
    args = custom_proc(request)
    return render(request,"staticpage/sale.html",args)


def AboutUsPage(request):
    args = custom_proc(request)
    return render(request,"staticpage/about_us.html",args)


def NewsPage(request):
    args = custom_proc(request)
    return render(request,"staticpage/news.html",args)


def DeliveryPaymentPage(request):
    args = custom_proc(request)
    return render(request,"staticpage/delivery_payment.html",args)
 
 
def robots(request):
    return render(request,'robots.txt', content_type='text/plain')