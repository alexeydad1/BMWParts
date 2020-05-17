# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMessage
from cart.Cart import Cart
from .forms import OrderForm
from .models import Order,OrderPosition,OrderStatus
from lk.models import Accounts,BalanceHistoryAccounts
from catalog.models import Price,Stock
from draft.models import ItemD,Draft
import datetime
from api_mg import send_message


# Create your views here.
@csrf_protect
def order(request):# периписать все как логин все!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    url_referer=request.META.get('HTTP_REFERER','/')
    cart = Cart(request)
    
    cartItem=cart.count()
    totalprice=cart.summary()
    
    args=dict(cart=Cart(request))

    args['cartItem']=cartItem
    args['cartTotal']=totalprice
    
    if request.method == 'GET':
        
        if request.user.is_authenticated():  
        #if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            
            args['f_name']=request.user.first_name
            args['l_name']=request.user.last_name
            args['phone']=request.user.accounts.telephone
            args['e_mail']=request.user.email
            args['username']=auth.get_user(request).username
            
            #auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return render(request,"orders/order.html",args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors']='Пользователь не найден!'
            args['username']=auth.get_user(request).username
           
            
            return redirect('%s?next=%s' % ('/lk/login/', request.path),args)
            #return render(request,"lk/login.html",args)
    else:
        '''-------------функция сохранения заказа--------------
        Сделать проверку формы!!!
        Сделать страницу с редиректом после оформления заказа
        Готово--- Сделать отправку письма с заказом на почту клиенту
        !!!Функция рабочая!!!
        '''
        fError=0
        args['f_name']=request.POST['f_name']
        args['l_name']=request.POST['l_name']
        args['phone']=request.POST['telephone']
        args['e_mail']=request.POST['e_mail']
        args['username']=auth.get_user(request).username
        args['address']=request.POST['address']
        args['commentorder']=request.POST['commentorder']
        
        
        
        if len(request.POST['f_name'])<2:
            args['f_name_errors']='Заполните поле "Имя"'
            fError=1

        if len(request.POST['address'])<10:
            args['address_errors']='Заполните поле "Адрес"'
            fError=1

        if len(request.POST['e_mail'])<4:
            args['e_mail_errors']='Заполните поле "E-mail"'
            fError=1
        elif '@' not in request.POST['e_mail']:
            args['e_mail_errors']='Указанный вами "E-mail"  некорректен'
            fError=1
        else:
            pass
 
        if len(request.POST['telephone'])<2:
            args['phone']='Заполните поле "Телефон"'
            fError=1
           
        if fError == 1:
            return render(request,"orders/order.html",args)
        
        order = Order()
        order.status = OrderStatus.objects.get(pk=1)
        order.accounts = Accounts.objects.get(username=auth.get_user(request))
        order.name = auth.get_user(request).username
        order.address = request.POST['address']
        order.comment = request.POST['commentorder']
        order.save()
        
        cart = Cart(request)
        
        for item in cart:
            orderP = OrderPosition()
            orderP.order = order
            orderP.product = item.product
            orderP.id_stock = Stock.objects.get(pk=item.stock.pk)
            orderP.count = item.quantity
# переписать на поиск цены по Бренду
            orderP.price_purchase = Price.objects.get(p_product=item.product,id_stock=item.stock.pk).purchase_price
            orderP.price_sale = item.unit_price
            orderP.brand = item.brand
            orderP.save()

        orderPositions = OrderPosition.objects.filter(order=order)
        order_mail_sus(request.user.first_name,request.POST['e_mail'],order.pk,orderPositions,order.address,order.comment)
        cart.clear()
        cartItem = cart.count()
        totalprice=cart.summary()

        request.session['id_order'] = order.number_order
        request.session.save()
        balance_order(request, order)
        return redirect('/order_finish/',{'username':auth.get_user(request).username,'cartItem':cartItem,'cartTotal':totalprice})


@csrf_protect
def orderDraft(request,id_draft):  # периписать все как логин все!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()

    args = dict(cart=Cart(request))
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice

    args['draft'] = ItemD.objects.select_related().filter(draft=id_draft)
    args['draftName'] = Draft.objects.get(id=id_draft)
    if request.method == 'GET':
        if request.user.is_authenticated():
            # if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"

            args['f_name'] = request.user.first_name
            args['l_name'] = request.user.last_name
            args['phone'] = request.user.accounts.telephone
            args['e_mail'] = request.user.email
            args['username'] = auth.get_user(request).username

            # auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return render(request, "orders/order_draft.html", args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Пользователь не найден!'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)
            # return render(request,"lk/login.html",args)
    else:
        '''-------------функция сохранения заказа--------------
        Сделать проверку формы!!!
        Сделать страницу с редиректом после оформления заказа
        Готово--- Сделать отправку письма с заказом на почту клиенту
        !!!Функция рабочая!!!
        '''
        fError = 0
        args['f_name'] = request.POST['f_name']
        args['l_name'] = request.POST['l_name']
        args['phone'] = request.POST['telephone']
        args['e_mail'] = request.POST['e_mail']
        args['username'] = auth.get_user(request).username
        args['address'] = request.POST['address']
        args['commentorder'] = request.POST['commentorder']

        if len(request.POST['f_name']) < 2:
            args['f_name_errors'] = 'Заполните поле "Имя"'
            fError = 1

        if len(request.POST['address']) < 10:
            args['address_errors'] = 'Заполните поле "Адрес"'
            fError = 1

        if len(request.POST['e_mail']) < 4:
            args['e_mail_errors'] = 'Заполните поле "E-mail"'
            fError = 1
        elif '@' not in request.POST['e_mail']:
            args['e_mail_errors'] = 'Указанный вами "E-mail"  некорректен'
            fError = 1
        else:
            pass

        if len(request.POST['telephone']) < 2:
            args['phone'] = 'Заполните поле "Телефон"'
            fError = 1

        if fError == 1:
            args['draft'] = ItemD.objects.select_related().filter(draft=id_draft)
            args['draftName'] = Draft.objects.get(id=id_draft)
            return render(request, "orders/order_draft.html", args)

        order = Order()
        order.status = OrderStatus.objects.get(pk=1)
        order.accounts = Accounts.objects.get(username=auth.get_user(request))
        order.name = auth.get_user(request).username
        order.address = request.POST['address']
        order.comment = request.POST['commentorder']
        order.save()

        draft = ItemD.objects.select_related().filter(draft=id_draft)

        for item in draft:
            orderP = OrderPosition()
            orderP.order = order
            orderP.product = item.product
            orderP.id_stock = Stock.objects.get(pk=item.stock.pk)
            orderP.count = item.quantity
# переписать на поиск цены по Бренду
            price = Price.objects.filter(p_product=item.product, id_stock=item.stock.pk)
            orderP.price_purchase = price[0].purchase_price
            orderP.price_sale = price[0].our_price
            orderP.brand = item.brand
            orderP.save()

        orderPositions = OrderPosition.objects.filter(order=order)
        order_mail_sus(request.user.first_name, request.POST['e_mail'], order.pk, orderPositions, order.address, order.comment)

        cartItem = cart.count()
        totalprice = cart.summary()
        balance_order(request,order)
        return render(request, "orders/order.html",
                      {'username': auth.get_user(request).username, 'cartItem': cartItem, 'cartTotal': totalprice})



def order_finish(request):
    url_referer = request.META.get('HTTP_REFERER', '/')
    cart = Cart(request)

    cartItem = cart.count()
    totalprice = cart.summary()
    args = {}
    args['cartItem'] = cartItem
    args['cartTotal'] = totalprice

    if request.method == 'GET':
        if request.user.is_authenticated():
            # if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            id_order = request.session.get('id_order',None)
            if 'id_order' in request.session:
                del request.session['id_order']
            else:
                return redirect(url_referer, args)
            request.session.save()
            order = Order.objects.get(number_order=id_order)
            order_item = OrderPosition.objects.select_related().filter(order=id_order)
            delivery = 0
            for item in order_item:
                if delivery < item.id_stock.delivery_time:
                    delivery = item.id_stock.delivery_time

            now_date = datetime.date.today()
            delta = datetime.timedelta(days=delivery)  # дельта в днях
            now_date = now_date + delta  # Узнаем какое число будет через n дней
            args['delivery'] = now_date.strftime('%d.%m.%Y')
            args['order_position'] = order_item
            args['name'] = request.user.last_name + ' ' + request.user.first_name
            args['phone'] = order.accounts.telephone
            args['order'] = order
            args['address'] = order.address

            args['username'] = auth.get_user(request).username

            # auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return render(request, "orders/order_chekout.html", args)
        else:
            # Отображение страницы с ошибкой
            args['login_errors'] = 'Пользователь не найден!'
            args['username'] = auth.get_user(request).username

            return redirect('%s?next=%s' % ('/lk/login/', request.path), args)
            # return render(request,"lk/login.html",args)
    else:
        return redirect(url_referer, args)




def order_mail_sus(name,email,numOrder,itemOrder,address,commentOrder):
        
        subject = u'Заказ №%s bmwminiparts.ru' % numOrder
        
        body=u'<!DOCTYPE html>'
        body+=u'<html>'
        body+=u'<head>'
        body+=u'</head>'
        body+=u'<body>'
        body+=u'<hr align="center" color="darkgray" width="90%" size="1px">'
        body+=u'<div><p>Уважаемый (ая) %s, благодарим Вас за то, что Вы воспользовались ' % name
        body+=u'услугами интернет-магазина запчастей и акссесуаров www.bmwminiparts.ru</p></div>'
        body+=u'<br>'
        body+=u'<table cellspacing="5" cellpadding="10" width="100% ">'
        body+=u'<thead bgcolor="#E6E9EE" >'
        body+=u'<tr>'
        body+=u'<th align="center">Номер</th>'
        body+=u'<th align="center">Описание</th>'
        body+=u'<th align="center">Цена</th>'
        body+=u'<th align="center">Кол-во</th>'
        body+=u'<th align="center">Сумма</th>'
        body+=u'</tr>'
        body+=u'</thead>'
        
        tPrice=0
        for item in itemOrder:
            body+=u'<tr>'
            body+=u'<td align="center">%s</td>' % item.product
            body+=u'<td align="center">%s</td>' % item.product.description
            body+=u'<td align="center">%s</td>' % item.price_sale
            body+=u'<td align="center">%s</td>' % item.count
            body+=u'<td align="center">%s</td>' % item.price()
            price=item.price()
            body+=u'</tr>'
            body+=u'<tr><td colspan="5"><hr align="center" color="darkgray" width="90%" size="1px"></td></tr>'
            tPrice+=price
        body+=u'<tr><td colspan="5" align="right">Итого: %s рублей</td></tr>' % tPrice
        body+=u'</table>'
        
        body+=u'<br><br><div>'
        body+=u'<p>Адрес доставки: %s</p>' % address
        body+=u'<p>Комментарий к закуазу: %s</p></div>' %commentOrder
        
        body+=u'<br><hr align="center" color="darkgray" width="90%" size="1px">'
        body+=u'''<div style="color:darkgray;">
                <p>Сайт: www.bmwminiparts.ru</p>
                <p>E-mail: zakaz@bmwminiparts.ru</p>
                <p>Instagram: instagram.com/bmwminiparts</p>
                <p>VK: vk.com/bmwminiparts</p>
                <p>Телефон: +7 (911) 121-62-53</p>
                </div>
              '''
        
        
        body += u'</body>'
        body += u'</html>'
        mail_from = 'order@bmwminiparts.ru' # ваш аккааунт
        mail_to = [email,'order@bmwminiparts.ru','zakaz@bmwminiparts.ru'] # список получателей
         
        send_message(subject, 'Заказ <order@bmwminiparts.ru>', body, mail_to)


def balance_order(request, order):
    account = Accounts.objects.get(username=auth.get_user(request))
    balance_h = BalanceHistoryAccounts()
    balance_h.account = account
    balance_h.operations = 'Списание по заказу №' + str(order.number_order)
    balance_h.balance_price = order.price()
    balance_h.save()
    account.balance -= order.price()
    account.save()