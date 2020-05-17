# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,get_object_or_404
from cart.Cart import Cart
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from draft.models import Draft,ItemD
from catalog.models import Stock,Product,Price
from lk.models import Accounts
import datetime

# Create your views here.
def drafts(request):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'GET':

        if request.user.is_authenticated():

            args['draft'] = Draft.objects.filter(accounts=auth.get_user(request))
            args['username'] = auth.get_user(request).username
            return render(request, "draft/draft.html", args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Пользователь не найден!'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)
            # return render(request,"lk/login.html",args)
    else:
        return render(request, "draft/draft.html", args)


@csrf_protect
def add_to_draft(request):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'POST':
        if len(request.POST['name_draft'])>2 and request.user.is_authenticated():
            draft=Draft()
            draft.name=request.POST['name_draft']
            draft.creation_date=datetime.datetime.now()
            draft.accounts = Accounts.objects.get(username=auth.get_user(request))
            draft.save()

            for item in cart:
                itemd = ItemD()
                itemd.draft = draft
                itemd.product = item.product
                itemd.stock = Stock.objects.get(pk=item.stock.pk)
                itemd.quantity = item.quantity
                itemd.unit_price = item.unit_price
                itemd.brand = item.brand
                itemd.save()

            cart.clear()
            cartItem = cart.count()
            totalprice = cart.summary()
            args['cartItem'] = cartItem
            args['cartTotal'] = totalprice

            return redirect('/lk/drafts/', "draft/draft.html", args)
        else:
            return redirect('/cart/', "cart/cart.html", args)

    else:
        return render(request, "cart/cart.html", args)


@csrf_protect
def add_to_draft_old(request):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'POST':
        if request.user.is_authenticated():
            draft=get_object_or_404(Draft,pk=int(request.POST['draft']),accounts_id=auth.get_user(request).id)
            itemD=ItemD.objects.filter(draft=draft)

            for item in cart:
                flagItem = 0
                for draft_item in itemD:
                    if item.product == draft_item.product and item.stock.pk == draft_item.stock.pk and item.brand == draft_item.brand:
                        draft_item.quantity += item.quantity
                        draft_item.save()
                        flagItem=1
                if flagItem != 1:
                    itemd = ItemD()
                    itemd.draft = draft
                    itemd.product = item.product
                    itemd.stock = Stock.objects.get(pk=item.stock.pk)
                    itemd.quantity = item.quantity
                    itemd.unit_price = item.unit_price
                    itemd.brand = item.brand
                    itemd.save()


            cart.clear()
            cartItem = cart.count()
            totalprice = cart.summary()
            args['cartItem'] = cartItem
            args['cartTotal'] = totalprice

            return redirect('/lk/drafts/', "draft/draft.html", args)
        else:
            return render(request, "cart/cart.html", args)

    else:
        return render(request, "cart/cart.html", args)


def draft_detail(request,id=1):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'GET':
        if request.user.is_authenticated():
            draft=get_object_or_404(Draft,pk=id,
                                    accounts_id=auth.get_user(request).id)
            item_draft=ItemD.objects.select_related().filter(draft_id=id)

            for item in item_draft:
# дописать проверку на бренд!!!!!!!!
                price=Price.objects.filter(p_product=item.product,
                                           id_stock=item.stock)
                if price[0].our_price != item.unit_price:
                    item.unit_price=price[0].our_price
                    item.save()

            item_draft = ItemD.objects.select_related().filter(draft_id=id)
            args['draftName'] = draft
            args['draft'] = item_draft
            args['username'] = auth.get_user(request).username
            return render(request, "draft/draft_detail.html", args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Войдите под своей учетной записью'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


    else:
        return render(request, "draft/draft.html", args)

def draft_item_del(request,product,stock,draft,brand):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'GET':
        if request.user.is_authenticated():
            args['username'] = auth.get_user(request).username
            itemd = ItemD.objects.get(
                draft_id=draft,
                # поставил заглушку от дублей вместо get
                product=Product.objects.filter(partnumber=product,producer_id=brand)[0],
                stock_id=stock,
                brand_id=brand,
            )
            itemd.delete()
            draftN=ItemD.objects.select_related().filter(draft_id=draft)
            if len(draftN)==0:
                draft_del=Draft.objects.get(pk=draft)
                draft_del.delete()
                return redirect('/lk/drafts/', "draft/draft.html", args)
            else:
                args['draft'] = draftN
                return redirect('/lk/draft_detail/'+ draft +'/', "draft/draft_detail.html", args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Войдите под своей учетной записью'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


    else:
        return render(request, "draft/draft.html", args)

def draft_del(request,draft):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'GET':
        if request.user.is_authenticated():
            args['username'] = auth.get_user(request).username
            draft_del = Draft.objects.get(pk=draft,accounts_id=auth.get_user(request).id)
            draft_del.delete()
            return redirect('/lk/drafts/', "draft/draft.html", args)

        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Войдите под своей учетной записью'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


    else:
        return render(request, "draft/draft.html", args)


@csrf_protect
def draft_update(request,draft_id):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))

    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice
    args['username'] = auth.get_user(request).username

    if request.method == 'POST':
        if request.user.is_authenticated():
            args['username'] = auth.get_user(request).username

            i = 0
            for item in request.POST.getlist('id_product'):
                product_i = Product.objects.filter(partnumber=request.POST.getlist('id_product')[i],
                                                   producer=request.POST.getlist('prd')[i])[0]
                stock_i = Stock.objects.get(id=request.POST.getlist('stk')[i])
                if request.POST.getlist('qty')[i] != '' and request.POST.getlist('qty')[i].isdigit():
                    quantity = int(request.POST.getlist('qty')[i])
                else:
                    quantity = 1
                itemD=ItemD.objects.get(product=product_i,
                                        stock=stock_i,
                                        draft=draft_id,
                                        brand=request.POST.getlist('prd')[i])
                itemD.quantity=int(quantity)
                itemD.save()
                i += 1
            draftName = get_object_or_404(Draft, pk=draft_id,
                                          accounts_id=auth.get_user(request).id)

            args['draftName'] = draftName
            args['draft'] = ItemD.objects.filter(draft=draft_id)
            return redirect('/lk/draft_detail/'+ draft_id +'/', "draft/draft_detail.html", args)

        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Войдите под своей учетной записью'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)


    else:
        return render(request, "draft/draft_detail.html", args)


# try:
#     item = models.Item.objects.get(
#         cart=self.cart,
#         product=product,
#         stock=stock,
#     )
# except models.Item.DoesNotExist:
#     raise ItemDoesNotExist
# else:  # ItemAlreadyExists
#     if quantity == 0:
#         item.delete()
#     else:
#         # item.unit_price = unit_price
#         item.quantity = int(quantity)
#         item.save()