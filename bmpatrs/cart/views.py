# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib import auth
from .Cart import Cart
from catalog.models import Product,Stock,Price,ProductManufacturer
from draft.forms import DraftPlus
from draft.models import Draft,ItemD
from django.views.decorators.csrf import csrf_protect


def add_to_cart(request,product_id,stock,id_price,id_brand,quantity=1):
    user = auth.get_user(request)
    if user.is_authenticated:
        u_discount = user.accounts.discount
    else:
        u_discount = 0
    url_referer = request.META.get('HTTP_REFERER','/')
    product = Product.objects.filter(partnumber=product_id,producer_id=id_brand)
    stock = Stock.objects.get(id=stock)
    unit_price = Price.objects.get(pk=id_price,p_product=product_id,id_stock=stock)
    brand = ProductManufacturer.objects.get(pk=id_brand)
    cart = Cart(request)

    cart.add(product[0],dicsount_user(u_discount,unit_price.our_price),stock,brand,quantity)
    
    cartItem=cart.count()
    totalprice=cart.summary()
    return redirect(url_referer,{'username':auth.get_user(request).username,'cartItem':cartItem,'cartTotal':totalprice})#, {'form': form}


def remove_from_cart(request,product_id,stock,id_brand):
    url_referer=request.META.get('HTTP_REFERER','/')
    
    product = Product.objects.filter(partnumber=product_id,producer=id_brand)
    brand = ProductManufacturer.objects.get(pk=id_brand)
    stock = Stock.objects.get(id=stock)
    cart = Cart(request)
    cart.remove(product[0],stock,brand)
    
    cartItem=cart.count()
    totalprice=cart.summary()
    return redirect(url_referer,{'username':auth.get_user(request).username,'cartItem':cartItem,'cartTotal':totalprice})#, {'form': form}


@csrf_protect
def update_cart(request,unit_price=None):
    url_referer = request.META.get('HTTP_REFERER','/')
    cart = Cart(request)
    
    if request.method == 'POST':
        i=0
        for item in request.POST.getlist('id_product'):
            product = Product.objects.filter(partnumber=request.POST.getlist('id_product')[i],
                                           producer=request.POST.getlist('prd')[i])
            stock = Stock.objects.get(id=request.POST.getlist('stk')[i])
            if request.POST.getlist('qty')[i]!='' and request.POST.getlist('qty')[i].isdigit():
                quantity = int(request.POST.getlist('qty')[i])
            else:
                quantity = 1
            brand = ProductManufacturer.objects.get(pk=request.POST.getlist('prd')[i])
            cart.update(product[0], quantity,stock,brand)
            i += 1
     
    cartItem = cart.count()
    totalprice = cart.summary()
    return redirect(url_referer,{'username':auth.get_user(request).username,'cartItem':cartItem,'cartTotal':totalprice})
    

def get_cart(request):
    cart = Cart(request)
    totalprice = cart.summary()
    cartItem = cart.count()

    form = DraftPlus()
    form.fields["draft"].queryset = Draft.objects.filter(accounts=auth.get_user(request).id)
    form.fields["draft"].empty_label = u"Выберите черновик"
    c = dict(cart=Cart(request))
    c['cartItem'] = cart.count()
    c['cartTotal'] = cart.summary()
    c['username'] = auth.get_user(request).username
    c['form'] = form
   
    return render(request,'cart/cart.html',c)

def dicsount_user(u_discount,price):
    d = price - (price*u_discount/100)
    return d