# -*- coding: utf-8 -*-
from django.contrib import auth
from django.shortcuts import render,get_object_or_404,redirect
from catalog.models import Product,Price,CrossProduct,ProductManufacturer
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_protect
from cart.Cart import Cart
from django.core.mail import EmailMessage

import re
import requests
import datetime
from BeautifulSoup import BeautifulSoup
from api_mg import send_message


s = requests.Session()
# Create your views here.

def home(request):
    #form = SearchForm()
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()

    return render(request, 'slider.html',{'username':auth.get_user(request).username,
                                          'cartItem':cartItem,
                                          'cartTotal':totalprice})#, {'form': form}


def search(request, brand=None, partnumber=None):
    # if this is a POST request we need to process the form data
    cart = Cart(request)
    cartItem = cart.count()
    totalprice=cart.summary()

    if request.method == 'GET':
        url_referer = request.META.get('HTTP_REFERER', '/')
        if brand != None and partnumber != None:
            product = Product.objects.filter(partnumber=partnumber,producer__name=brand)
            p = partnumber
            p_null = 0
            if p.startswith('0'):
               for n in p:
                   if n == '0':
                       p_null +=1
                   else:
                       break
               p = p[p_null:]
        else:
            pn = request.GET['partnumber']
            reg = re.compile('[^a-zA-Z0-9]')
            p = reg.sub('', pn)
            p_null = 0
            if p.startswith('0'):
               for n in p:
                   if n == '0':
                       p_null +=1
                   else:
                       break
               p = p[p_null:]

        #Ищем номер в базе
#найти способ искать запчать по производителю
        #product = Product.objects.filter(partnumber=p).values('partnumber','producer').order_by().distinct()

            product = Product.objects.filter(partnumber=p)
        # Если не нашли

        if len(product) == 0:
            if 'lk/offer_detail/' in url_referer:
                if 'error_request' not in request.session:
                    request.session['error_request'] = 'У нас в каталоге нет такой запчасти!'
                    request.session.save()
                return redirect(url_referer, 'offer/offer_detail.html',
                                {'p': p,
                                 'username': auth.get_user(request).username,
                                 'cartItem': cartItem,
                                 'cartTotal': totalprice})
            else:
                return render(request, 'catalog/products.html',
                          {'p': p,
                           'error_request':'У нас в каталоге нет такой запчасти!',
                           'username':auth.get_user(request).username,
                           'cartItem':cartItem,'cartTotal':totalprice})
        # Если нашли больше одного номера выводим на экран пользователю для выбора
        if len(product) > 1:
            return render(request, 'catalog/products.html',
                          {'p': p,
                           'many_products' : product,
                           'username': auth.get_user(request).username,
                           'cartItem': cartItem, 'cartTotal': totalprice})
        else:
        #ПОИСК не оригинала
            user = auth.get_user(request)
            if user.is_authenticated:
                u_discount = user.accounts.discount
            else:
                u_discount = 0

            cross_parts = []
            no_price_cross_parts = []
            if len(p) < 11:
                cross_p = CrossProduct.objects.filter(crossnumber__icontains='---'+ p + '---')
            else:
                cross_p = CrossProduct.objects.filter(crossnumber__icontains= p)

            corss_p_uniq = set()

            for c_p_u in cross_p:
                cross_sep = c_p_u.crossnumber.split('---')
                for c_sep in cross_sep:
                    corss_p_uniq.add(c_sep)

            if len(cross_p) > 0:
                # if len(cross_p)==1:
                #     cross = cross_p.crossnumber.split('---')
                # else:
                #     cross=cross_p[0].crossnumber.split('---')

                # for c_p in corss_p_uniq:
                #     cross = c_p.crossnumber.split('---')
                #     cross_product = Product.objects.filter(partnumber__in=cross)
                    #print corss_p_uniq
                    c = Price.objects.select_related().filter(p_product__in=corss_p_uniq)
                   #print c
                    for price in c:
                        if price.p_product != p:
                            product_cross=Product.objects.select_related().filter(partnumber=price.p_product).values('description','producer','producer__name').order_by().distinct()
                            utc_3 = datetime.timedelta(hours=3)
                            date_price = price.created_at + utc_3
                            cross_dict = {
                                'stock': price.id_stock.name_stock,
                                'producer': product_cross[0].get('producer__name'),
                                'p_product': price.p_product,
                                'description': product_cross[0].get('description'),
                                'qty': price.qty,
                                'delivery_time': price.id_stock.delivery_time,
                                'purchase_price': str(price.purchase_price),
                                'our_price': str(price.our_price),
                                'id_stock': price.id_stock.pk,
                                'pk': price.pk,
                                'producer_pk': product_cross[0].get('producer'),
                                'created_at': date_price.strftime("%d %B %Y г. %H:%M"),
                                }
                            if user.is_authenticated and u_discount > 0:
                                cross_dict['our_price_discount'] = str(dicsount_user(u_discount, price.our_price))
                            cross_parts.append(cross_dict)

                    # for cp in cross_product:
                    #    if cp.partnumber != p:
                    #            c = Price.objects.select_related().filter(p_product=cp.partnumber)
                    #            if len(c) > 0:
                    #                cross_dict = {'partnumber': cp.partnumber,
                    #                              'description': cp.description,
                    #                              'producer': cp.producer,
                    #                              'qty': c[0].qty,
                    #                              'price_in': c[0].purchase_price,
                    #                              'delivery_time':c[0].id_stock.delivery_time,
                    #                              'our_price':c[0].our_price,
                    #                              'stock':c[0].id_stock.pk,
                    #                              'id_price':c[0].pk}
                    #                cross_parts.append(cross_dict)
                    #            else:
                    #                no_price_cross_parts.append(cp)

            parts = Price.objects.filter(p_product=p)
            if u_discount > 0:
                parts1 = []
                for p in parts:
                    p_dict = {
                        'p_product':p.p_product,
                        'id_stock':p.id_stock,
                        'qty':p.qty,
                        'purchase_price':p.purchase_price,
                        'our_price':p.our_price,
                        'our_price_discount':dicsount_user(u_discount,p.our_price),
                        'brand':p.brand,
                        'dealer_price':p.dealer_price,
                        'created_at':p.created_at,
                        'pk':p.pk
                    }
                    parts1.append(p_dict)
                parts = parts1
                    # redirect to a new URL:

            if len(parts) > 0:
                if 'lk/offer_detail/' in url_referer:
                    if 'offer' not in request.session:
                        request.session['offer'] = list()
                        for price in parts:
                            stock = price.id_stock.name_stock
                            producer = product[0].producer.name
                            description = product[0].description
                            request.session['offer'].append({
                                'stock': stock,
                                'producer': producer,
                                'p_product': price.p_product,
                                'description': description,
                                'qty': price.qty,
                                'delivery_time': price.id_stock.delivery_time,
                                'purchase_price': str(price.purchase_price),
                                'our_price': str(price.our_price),
                                'dealer_price': str(price.dealer_price),
                                'created_at': str(price.created_at),
                                'id_stock': price.id_stock.pk,
                                'pk': price.pk,
                                'producer_pk': product[0].producer.pk,
                            })
                        if 'offer_cross' not in request.session:
                            request.session['offer_cross'] = cross_parts
                        else:
                            del request.session['offer_cross']
                            request.session['offer_cross'] = cross_parts
                    else:
                        if 'offer_cross' not in request.session:
                            request.session['offer_cross'] = cross_parts
                        else:
                            del request.session['offer_cross']
                            request.session['offer_cross'] = cross_parts

                        del request.session['offer']
                        request.session['offer'] = list()
                        for price in parts:
                            stock = price.id_stock.name_stock
                            producer = product[0].producer.name
                            description = product[0].description
                            request.session['offer'].append({
                                'stock': stock,
                                'producer': producer,
                                'p_product': price.p_product,
                                'description': description,
                                'qty': price.qty,
                                'delivery_time': price.id_stock.delivery_time,
                                'purchase_price': str(price.purchase_price),
                                'our_price': str(price.our_price),
                                'dealer_price': str(price.dealer_price),
                                'created_at': str(price.created_at),
                                'id_stock': price.id_stock.pk,
                                'pk': price.pk,
                                'producer_pk': product[0].producer.pk,
                            })
                    request.session.save()
                    return redirect(url_referer, 'offer/offer_detail.html',
                                  {'username': auth.get_user(request).username,
                                   'cartItem': cartItem,
                                   'cartTotal': totalprice})

                else:

                    return render(request, 'catalog/products.html',
                              {'parts': parts,
                               'producer': unicode(product[0].producer),
                               'descript':unicode(product[0].description),
                               'cross_parts': cross_parts,
                               'no_price_cross_parts': no_price_cross_parts,
                               'product' : product[0],
                               'p': p,
                               'username':auth.get_user(request).username,
                               'cartItem':cartItem,
                                'cartTotal':totalprice})

            else:
                if 'lk/offer_detail/' in url_referer:
                    if 'no_price_offer' not in request.session:
                        request.session['no_price_offer'] = list()
                        producer = product[0].producer.name
                        description = product[0].description
                        request.session['no_price_offer'].append({
                            'producer': producer,
                            'partnumber': product[0].partnumber,
                            'description': description,

                        })
                        if 'offer_cross' not in request.session:
                            request.session['offer_cross'] = cross_parts
                        else:
                            del request.session['offer_cross']
                            request.session['offer_cross'] = cross_parts
                    else:
                        if 'offer_cross' not in request.session:
                            request.session['offer_cross'] = cross_parts
                        else:
                            del request.session['offer_cross']
                            request.session['offer_cross'] = cross_parts

                        del request.session['no_price_offer']
                        request.session['no_price_offer'] = list()
                        producer = product[0].producer.name
                        description = product[0].description
                        request.session['no_price_offer'].append({
                            'producer': producer,
                            'partnumber': product[0].partnumber,
                            'description': description,

                        })
                    request.session.save()
                    return redirect(url_referer, 'offer/offer_detail.html',
                                  {'username': auth.get_user(request).username,
                                   'cartItem': cartItem,
                                   'cartTotal': totalprice})
                return render(request, 'catalog/products.html',
                              {'no_price': product[0],
                               'descript': product[0].description,
                               'producer': product[0].producer,
                               'cross_parts': cross_parts,
                               'no_price_cross_parts': no_price_cross_parts,
                               'p': p,
                               'username':auth.get_user(request).username,
                               'cartItem':cartItem,
                               'cartTotal':totalprice})

    # if a GET (or any other method) we'll create a blank form
    else:
        return render(request, 'base.html', {'username':auth.get_user(request).username,
                                             'cartItem':cartItem,
                                             'cartTotal':totalprice})


def search_brand(request,brand,partnumber):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    if request.method == 'GET':

        p = partnumber

        product = get_object_or_404(Product,partnumber=p,
                                    producer=ProductManufacturer.objects.get(name=brand))
        parts = Price.objects.filter(p_product=p)
        return render(request, 'catalog/products.html',
                      {'parts': parts,
                       'product': product,
                       'p': p,
                       'username': auth.get_user(request).username,
                       'cartItem': cartItem,
                       'cartTotal': totalprice})
    else:

        return render(request, 'base.html', {'username': auth.get_user(request).username,
                                             'cartItem': cartItem,
                                             'cartTotal': totalprice})


def to_all_bmw(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    if request.method == 'GET':


        return render(request, 'to_all_bmw.html',
                      {'username': auth.get_user(request).username,
                       'cartItem': cartItem,
                       'cartTotal': totalprice}
                      )
    else:

        return render(request, 'base.html', {'username': auth.get_user(request).username,
                                             'cartItem': cartItem,
                                             'cartTotal': totalprice})


def oil_tech(request):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    if request.method == 'GET':
        products_oil = Product.objects.filter(category_id=2)
        products_tehnical = Product.objects.filter(category_id=3)
        return render(request, 'teh_oil.html',
                      {'username': auth.get_user(request).username,
                       'cartItem': cartItem,
                       'cartTotal': totalprice,
                       'products_oil': products_oil,
                       'products_tehnical':products_tehnical}
                      )
    else:

        return render(request, 'base.html', {'username': auth.get_user(request).username,
                                             'cartItem': cartItem,
                                             'cartTotal': totalprice})


def model_to(request,series,kuzov=None,motor=None):

    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    if request.method == 'GET':

        if series and motor == None:
            if series == '1' and motor == None:
                models =[{'model':'F20','img':'/img/models/kuzov/F20.png','motor':['116i','125i','135i','120d']},
                {'model':'E87','img':'/img/models/kuzov/E87.png','motor':['116i','118i','120i','130i','120d']}]

            if series == '2' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png', 'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == '3' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png', 'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == '4' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png', 'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == '5' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png', 'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == '6' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png', 'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == '7' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'i8' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'X1' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'i8' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'X3' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'X4' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'X5' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]

            if series == 'X6' and motor == None:
                models = [
                    {'model': 'F20', 'img': '/img/models/3_Series.png',
                     'motor': ['116i', '125i', '135i', '120d']},
                    {'model': 'E87', 'img': '/img/models/2_Series.png',
                     'motor': ['116i', '118i', '120i', '130i', '120d']}]


            return render(request, 'model_to.html',
                      {'username': auth.get_user(request).username,
                       'cartItem': cartItem,
                       'cartTotal': totalprice,
                       'models': models,
                       'series': series
                       }
                      )

        if series and motor != None:
            parts={}
            if series == '1' and motor == '116i' and kuzov == 'F20':
                parts = {'oil_filter':'11427635557',
                        'air_filter':'13718507320',
                        'salon_filter':'64119237555',
                        'break_front':'34116858910',
                        'break_rear':'34216873093',
                        'disc_brake_front':'34116792215',
                        'disc_brake_rear':'34216792225',
                        'sensor_brake_front':'34356792289',
                        'sensor_brake_rear':'34356792292'
                        }

            if series == '1' and motor == '125i' and kuzov == 'F20':
                parts = {'oil_filter':'11428683204',
                        'air_filter':'13718507320',
                        'salon_filter':'64119237555',
                        'break_front':'34106859181',
                        'break_rear':'34216873093',
                        'disc_brake_front':'34116792219',
                        'disc_brake_rear':'34216792227',
                        'sensor_brake_front':'34356792289',
                        'sensor_brake_rear':'34356792292'
                         }

            if series == '1' and motor == '135i' and kuzov == 'F20':
                parts = {'oil_filter':'11427566327',
                        'air_filter':'13718616909',
                        'salon_filter':'64119237555',
                        'break_front':'34116878876',
                        'break_rear':'34216876422',
                        'disc_brake_front':'34116792223',
                        'disc_brake_rear':'34206797605',
                        'sensor_brake_front':'34356792289',
                        'sensor_brake_rear':'34356792292'
                         }

            if series == '1' and motor == '120d' and kuzov == 'F20':
                parts = {'oil_filter':'11428507683',
                        'air_filter':'13718511668',
                        'salon_filter':'64119237555',
                        'break_front':'34116850568',
                        'break_rear':'34216873093',
                        'disc_brake_front':'34116792217',
                        'disc_brake_rear':'34216792227',
                        'sensor_brake_front':'34356792289',
                        'sensor_brake_rear':'34356792292'
                         }
            if len(parts) > 0:
                return render(request, 'model_to.html',
                              {'username': auth.get_user(request).username,
                               'cartItem': cartItem,
                               'cartTotal': totalprice,
                               'parts': parts,
                               'series': series,
                               'motor': motor,
                               'kuzov': kuzov
                               }
                              )
            else:
                page_not = u'Страница находится в разработке и скоро появится!'
                return render(request, 'model_to.html', {'username': auth.get_user(request).username,
                                                         'cartItem': cartItem,
                                                         'cartTotal': totalprice,
                                                         'page_not': page_not})
        page_not = u'Страница находится в разработке и скоро появится!'
        return render(request, 'model_to.html', {'username': auth.get_user(request).username,
                                                 'cartItem': cartItem,
                                                 'cartTotal': totalprice,
                                                 'page_not': page_not})
    else:

        return render(request, 'base.html', {'username': auth.get_user(request).username,
                                             'cartItem': cartItem,
                                             'cartTotal': totalprice})

# @csrf_protect
# def parser_ilcats(request):
#     cart = Cart(request)
#     cartItem = cart.count()
#     totalprice = cart.summary()
#     url_referer = request.META.get('HTTP_REFERER', '/')
#     if request.method == 'GET':
#         if '/catalog_online/' not in url_referer:
#             response = request_session('http://bmw.ilcats.ru//clid/1')
#             response = response.replace('http://bmw.ilcats.ru', '/catalog_online')
#         else:
#             response = request_session(request.path.replace('/catalog_online','http://bmw.ilcats.ru'))
#             response = response.replace('http://bmw.ilcats.ru', '/catalog_online')
#             response = response.replace('http://www.neoriginal.ru/spares/bmw/', '/search?partnumber=')
#
#         soup = BeautifulSoup(response)
#
#         block = soup.findAll(id="ms_12")
#         #soup.map.decompose()
#         ilcats_list = []
#
#         for b in block:
#
#             ilcats_list.append(unicode(b).encode('utf-8'))
#
#
#         ilcats = ''.join(ilcats_list)
#
#
#
#         patern = between_parse(ilcats, '<div class="panel-heading">',
#                             '</div></div></div>')
#         ilcats = ilcats.replace(patern,"")
#
#         patern = between_parse(ilcats, '<map',
#                                '</map>')
#
#         ilcats = ilcats.replace(patern, "")
#
#         patern = between_parse(ilcats, '<div class="btn-toolbar">',
#                                '''</ul>
# </div>
# </div>''')
#
#         ilcats = ilcats.replace(patern, "")
#
#         return render(request, 'etk_online.html',
#                       {'username': auth.get_user(request).username,
#                        'cartItem': cartItem,
#                        'cartTotal': totalprice,
#                        'ilcats': ilcats
#                        }
#                       )
#     else:
#
#         vin = request.POST['vin']
#         response = request_session('http://bmw.ilcats.ru//vin/'+vin+'/clid/1')
#         response = response.replace('http://bmw.ilcats.ru', '/catalog_online')
#
#         soup = BeautifulSoup(response)
#
#         block = soup.findAll(id="ms_12")
#         # soup.map.decompose()
#         ilcats_list = []
#
#         for b in block:
#             ilcats_list.append(unicode(b).encode('utf-8'))
#
#         ilcats = ''.join(ilcats_list)
#
#
#         patern = between_parse(ilcats,'<div class="panel-heading">','</div></div></div>')
#         ilcats = ilcats.replace(patern, "")
#         return render(request, 'etk_online.html',
#                       {'username': auth.get_user(request).username,
#                        'cartItem': cartItem,
#                        'cartTotal': totalprice,
#                        'ilcats': ilcats
#                        }
#                       )


@csrf_protect
def inquiry_part(request,pnumber):
    cart = Cart(request)
    cartItem = cart.count()
    totalprice = cart.summary()
    if request.method == 'POST':
        part = Product.objects.filter(partnumber=pnumber)
        name = request.POST['name']
        telephone = request.POST['telephone']
        e_mail = request.POST['e_mail']
        comment = request.POST['comment']
        order_mail_sus(part, e_mail, name, telephone, comment)
        return render(request, 'catalog/inquiry.html', {'username': auth.get_user(request).username,
                                                 'cartItem': cartItem,
                                                 'cartTotal': totalprice,
                                                 'part': part[0],
                                                 'name': name,
                                                 'telephone': telephone,
                                                 'e_mail': e_mail,
                                                 'comment': comment
                                                                        })
    else:

        return render(request, 'base.html', {'username': auth.get_user(request).username,
                                             'cartItem': cartItem,
                                             'cartTotal': totalprice})

def set_loop(lst):
    seen = set()
    result = []
    for x in lst:
        if x in seen:
            continue
        seen.add(x)
        result.append(x)
    return result

# @csrf_protect
# def request_session(link):
#     headers = {'User-agent': 'Mozilla/5.0'}
#     r = s.get(link,headers=headers)
#     r.encoding = 'utf-8'
#     return r.text


def between_parse(s,find1,find2):
    p1 = s.find(find1)
    p2 = s.find(find2)
    return s[p1:p2+len(find2)]


def order_mail_sus(part, email, name, telephone, comment):
    subject = u'Запрос на поставку детали %s ' % part[0].partnumber
    body = u'<!DOCTYPE html>'
    body += u'<html>'
    body += u'<head>'
    body += u'</head>'
    body += u'<body>'
    body += u'<h5>Запрос на поставку детали :</h5></br>'
    body += u'<hr><h4>{0} - {1}</h4><hr></br>'.format(
        part[0].partnumber, part[0].description)
    body += u'<h4>Контакты клиента :</h4>'
    body += u'<table cellpadding="7">'
    body += u'<tr><td>Имя:   </td><td>{0}</td></tr>' \
            u'<tr><td>Телефон:   </td><td>{1}</td></tr>' \
            u'<tr><td>E - mail:   </td><td>{2}</td></tr>' \
            u'<tr><td>Комментарий:   </td><td>{3}</td></tr>'.format(
    name, telephone, email, comment)
    body += u'</table>'
    body += u'</body>'
    body += u'</html>'
    mail_to = ['zakaz@bmwminiparts.ru']  # список получателей

    send_message(subject, 'Заказ <order@bmwminiparts.ru>', body, mail_to)


def dicsount_user(u_discount,price):
    d = price - (price*u_discount/100)
    return d