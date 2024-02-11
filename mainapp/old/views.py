from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
#from .forms import LoginForm
import random
from .entity import *
from .DBManager import *
from django.conf import settings
from datetime import datetime
from django.utils import dateformat
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
#from django.contrib import auth

from .forms import *
from django.views import *
from django.db.models import F, Func
from django.db.models import *
from django_mysql.models import GroupConcat
from django.db.models.functions import Concat
import datetime
from django.db.models.functions import Coalesce


from django.core import serializers
from django.http import JsonResponse
import json
import MySQLdb
from django.db import connections



def index(request):
    row = DBManager.SelectAllMeals()
    #print(row)
    #print(request.user)
    #print(request.user.is_authenticated)
    return render(request, 'mainapp/index.html')

def menu(request):
    return render(request, 'mainapp/menu.html', {'meals': DBManager.SelectAllMeals(), 'categs': DBManager.SelectAllCategories(), 'categor_name': ('Меню',)})

def scheme(request):
    return render(request, 'mainapp/scheme.html', {'tables': DBManager.SelectAllTables()})

def menu_filt(request, category_id):
    return render(request, 'mainapp/menu.html', {'meals': DBManager.SelectMealsFiltered(category_id), 'categs': DBManager.SelectAllCategories(), 'categor_name': DBManager.CategoryGetName(category_id)})

def my_reservations(request):
    return render(request, 'mainapp/myreservations.html', {'reservations': DBManager.SelectAllUserReservations(request.user.id)})

def my_orders(request):
    return render(request, 'mainapp/myorders.html', {'orders': DBManager.SelectAllUserOrders(request.user.id)})

def make_order(request):
    return render(request, 'mainapp/makeorder.html', {'meals': DBManager.SelectAllMeals(), 'reservations': DBManager.SelectAllUserActiveReservations(request.user.id)})

def submit_order(request):
    order_id = DBManager.GetLastOrderID()+1
    table_time = (request.POST['table_time']).split()
    table = table_time[0]
    mon_con = {'января':1, 'февраля':2, 'марта':3, 'апреля':4, 'мая':5, 'июня':6, 'июля':7, 'августа':8, 'сентября':9, 'октября':10, 'ноября':11, 'декабря':12}
    time = '{}-{}-{} {}'.format(table_time[4], mon_con[table_time[3]], table_time[2], table_time[6])
    addit_wishes = request.POST['addit_wishes']
    if(addit_wishes == ''):
        addit_wishes = 'Не указано'
    meals = DBManager.SelectAllMeals()

    ord = Order(id=order_id, res=Reservation(table=Table(name=table), res_date=time), pref=addit_wishes)
    DBManager.CreateOrder(ord)
    for meal in meals:
        if request.POST[str(meal.id)] != '':
            DBManager.OrderAddMeal(order_id, meal.id, int(request.POST[str(meal.id)]))

    return HttpResponseRedirect('/')

def choose_date(request):
    return render(request, 'mainapp/chooseDate.html')

def booking_table(request):
    dt_beg = request.POST['date_time']
    stay_time = request.POST['stay']
    dt_end = (str(parse_datetime(dt_beg)+timedelta(hours=float(stay_time))))[:-3]
    dt_beg = dt_beg.replace('T', ' ')

    #print(11111111, order_id, table, time, addit_wishes, 11111111)
    #print(dt_beg)
    #print(dt_end)
    tables_avail = DBManager.SelectAllAlailableTables(dt_beg, dt_end)
    #print(tables_avail)
    return render(request, 'mainapp/booking.html', {'dt_beg': dt_beg, 'dt_end': dt_end, 'tables': tables_avail})

def submit_booking(request):
    reservation_id = DBManager.GetLastReservationID()+1
    res_beg = request.POST['beg']
    res_end = request.POST['end']
    res_table = request.POST['table_name']
    res_wishes = request.POST['addit_wishes']
    res_tel = request.POST['tel_no']
    ref_name = request.POST['ref_name']
    reserv = Reservation(id=reservation_id, table=Table(name=res_table), client=User(id=request.user.id), res_date=res_beg, leave_date=res_end, wishes=res_wishes, ref_name=ref_name, tel_no=res_tel)
    if(reserv.wishes == ''):
        reserv.wishes = 'Не указано'
    DBManager.CreateReservation(reserv)

    #DBManager.CreateOrder(order_id, table, time, addit_wishes)

    return HttpResponseRedirect('/')

def apply_arriv(request):
    return render(request, 'mainapp/applyariv.html', {'reservations': DBManager.SelectAllNonAppliedArrivals()})

def applyArriv(request):
    res_id = request.POST['res_id']
    DBManager.ApplyArrival(res_id)
    return HttpResponseRedirect('apply_arriv/')

def cancelArriv(request):
    res_id = request.POST['res_id']
    DBManager.CancelArrival(res_id)
    return HttpResponseRedirect('apply_arriv/')

def apply_payment(request):
    return render(request, 'mainapp/applypay.html', {'orders': DBManager.SelectAllNonAppliedPayment()})


def applyFinish(request):
    order_id = request.POST['order_id']
    DBManager.ApplyFinish(order_id)
    return HttpResponseRedirect('apply_payment/')

def cancelFinish(request):
    order_id = request.POST['order_id']
    DBManager.CancelFinish(order_id)
    return HttpResponseRedirect('apply_payment/')

def change_res(request):
    return render(request, 'mainapp/changeres.html', {'reservations': DBManager.SelectAllResertions()})

def applyLeave(request):
    res_id = request.POST['res_id']
    DBManager.ApplyLeave(res_id)
    return HttpResponseRedirect('change_res/')

def applyRequest(request):
    res_id = request.POST['res_id']
    DBManager.ApplyRequest(res_id)
    return HttpResponseRedirect('change_res/')

def cancelRequest(request):
    res_id = request.POST['res_id']
    DBManager.CancelRequest(res_id)
    return HttpResponseRedirect('change_res/')

def change_order(request):
    return render(request, 'mainapp/changeorder.html', {'orders': DBManager.SelectAllOrders()})

def applyOrderRequest(request):
    order_id = request.POST['order_id']
    DBManager.ApplyOrderRequest(order_id)
    return HttpResponseRedirect('change_order/')

def cancelOrderRequest(request):
    order_id = request.POST['order_id']
    DBManager.CancelOrderRequest(order_id)
    return HttpResponseRedirect('change_order/')

def applyCookingStart(request):
    order_id = request.POST['order_id']
    DBManager.ApplyCookingStart(order_id)
    return HttpResponseRedirect('change_order/')

def applyCookingFinish(request):
    order_id = request.POST['order_id']
    DBManager.ApplyCookingFinish(order_id)
    return HttpResponseRedirect('change_order/')

def add_meal(request):
    return render(request, 'mainapp/addMeal.html', {'categories': DBManager.SelectAllCategories()})

def submit_adding(request):
    meal_name = request.POST['meal_name']
    meal_descrip = request.POST['descrip']
    meal_categ = request.POST['categor']
    meal_cost = request.POST['cost']
    DBManager.AddNewMeal(meal_name, meal_descrip, meal_categ, meal_cost)
    return HttpResponseRedirect('/')

def top_meal(request):
    return render(request, 'mainapp/topMeals.html', {'meals': DBManager.TopMeals()})

@login_required
def afterlogin(request):
    return redirect('/')

@login_required
def logout_user(request):
    if request.user.is_active:
        logout(request)
    return redirect('/')






class RegistrationView(View):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(email=form.cleaned_data['email'],
                                             username=form.cleaned_data['login'],
                                             password=form.cleaned_data['password'])
            return HttpResponseRedirect('login/')

        return render(request, 'mainapp/register.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'mainapp/register.html', {'form': form})


class LoginView(View):
    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['login'], 
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/login')

        return render(request, 'mainapp/login.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'mainapp/login.html', {'form': form})


class CatalogView(View):
    def get(self, request):
        watches = Watch.objects.all().order_by('id').annotate(brand_name=F('brand__brand_name')) \
        .annotate(category_name=F('category__category_name')) \
        .annotate(mechanism_name=F('mechanism_type__mechanism_name')) \
        .annotate(glass_type_name=F('glass_type__glass_type_name')) \
        .annotate(strap_type_name=F('strap_type__strap_type_name')) \
        .annotate(case_type_name=F('case_band__case_type_name')) \
        .annotate(indication_type_name=F('indication_type__indication_type_name'))

        forms = []
        if watches != None and watches.count() > 0:
            for watch in watches:
                forms.append(CartItemForm())

        row = None
        con = connections['default']
        info = {}
        with con.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            # columns = [col[0] for col in cursor.description]
            # rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.execute("SELECT * FROM test_cat_sales")
            info['sales'] = cursor.fetchall()
            cursor.execute("SELECT * FROM test_cat_rating")
            info['rating'] = cursor.fetchall()
            
        print(info)

         

        return render(request, 'mainapp/catalog.html', {'watches': watches, 'forms': forms, 'info': json.dumps(info)})


class AddWatchView(View):
    def get(self, request):
        #initial={'mechanism_type': 1}
        form = AddWatchForm()
        return render(request, 'mainapp/add_watch.html', {'form': form})

    def post(self, request):
        form = AddWatchForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data['model_features'])
            # for i in form.cleaned_data['model_features']:
            #     print(i.id)

            #print(form.cleaned_data['mechanism_type'])
            new_watch = Watch(model_name=form.cleaned_data['model_name'],
                              model_cost=form.cleaned_data['model_cost'],
                              case_height=form.cleaned_data['case_width'],
                              case_width=form.cleaned_data['case_width'],
                              case_depth=form.cleaned_data['case_depth'],
                              weight=form.cleaned_data['weight'],
                              gender=form.cleaned_data['gender'],
                              waterproof_level=form.cleaned_data['waterproof_level'],
                              #backlight=form.cleaned_data['backlight'],
                              current_amount=form.cleaned_data['current_amount'],
                              mechanism_type=form.cleaned_data['mechanism_type'],
                              case_band=form.cleaned_data['case_band'],
                              glass_type=form.cleaned_data['glass_type'],
                              strap_type=form.cleaned_data['strap_type'],
                              indication_type=form.cleaned_data['indication_type'],
                              brand=form.cleaned_data['brand'],
                              category=form.cleaned_data['category'],
                              model_description=form.cleaned_data['model_description'])

            if form.cleaned_data['image'] != None and form.cleaned_data['image'] != '':
                new_watch.image = form.cleaned_data['image']

            feature_list = []
            for feature in form.cleaned_data['model_features']:
                feature_list.append(WatchHasFeature(watch=new_watch, feature=feature))
            
            new_watch.save()
            WatchHasFeature.objects.bulk_create(feature_list)
            return HttpResponseRedirect('/login')

        return render(request, 'mainapp/add_watch.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        form = ProfileForm(initial={'login': request.user.username,
                                    'email': request.user.email,
                                    'first_name': request.user.first_name,
                                    'last_name': request.user.last_name})
        return render(request, 'mainapp/profile.html', {'form': form})

class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm(initial={'user_id': request.user.id})
        return render(request, 'mainapp/change_password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return HttpResponseRedirect('login/')

        return render(request, 'mainapp/change_password.html', {'form': form})


class UserOrdersView(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.annotate(watches_list = GroupConcat(Concat('orderhasproduct__product_id__model_name', Value(' x '), 'orderhasproduct__quantity'), separator='\n')) \
        .filter(user_id=user.id).exclude(order_state__order_state_name='Корзина')
        #print(orders.count())
        #ohp = OrderHasProduct.objects.filter(order_id=OuterRef('id'))
        #order = Order.objects.annotate(watches_list = Subquery(ohp.values('quantity'))).first()
        #print(order.watches_list)
        
        return render(request, 'mainapp/my_orders.html', {'orders': orders})


class ChangeWatchView(View):
    def get(self, request, watch_id):
        #initial={'mechanism_type': 1}
        watch = Watch.objects.get(id=watch_id)
        form = AddWatchForm(initial={
            'model_name': watch.model_name, 'model_cost': watch.model_cost,
            'case_width': watch.case_width, 'case_depth': watch.case_depth,
            'weight': watch.weight, 'gender': watch.gender,
            'waterproof_level': watch.waterproof_level, #'backlight': watch.backlight,
            'current_amount': watch.current_amount, 'mechanism_type': watch.mechanism_type,
            'case_band': watch.case_band, 'glass_type': watch.glass_type,
            'strap_type': watch.strap_type, 'brand': watch.brand,
            'indication_type': watch.indication_type,
            'category': watch.category, 'model_description': watch.model_description,
            'image': watch.image,
            'model_features': Feature.objects.filter(watchhasfeature__watch=watch)
        })
        #print(Feature.objects.filter(watchhasfeature__watch=watch))
        #request.FILES['image'] = watch.image
        return render(request, 'mainapp/change_watch.html', {'form': form, 'watch_id': watch_id})

    def post(self, request, watch_id):
        form = AddWatchForm(request.POST, request.FILES)
        watch = Watch.objects.get(id=watch_id)
        if form.is_valid():
            # print(form.cleaned_data['model_features'])
            # for i in form.cleaned_data['model_features']:
            #     print(i.id)
            #print(form.cleaned_data['mechanism_type'])
            watch.model_name = form.cleaned_data['model_name']
            watch.model_cost = form.cleaned_data['model_cost']
            watch.case_width = form.cleaned_data['case_width']
            watch.case_height = form.cleaned_data['case_width']
            watch.case_depth = form.cleaned_data['case_depth']
            watch.weight = form.cleaned_data['weight']
            watch.gender = form.cleaned_data['gender']
            watch.waterproof_level = form.cleaned_data['waterproof_level']
            #watch.backlight = form.cleaned_data['backlight']
            watch.current_amount = form.cleaned_data['current_amount']
            watch.mechanism_type = form.cleaned_data['mechanism_type']
            watch.case_band = form.cleaned_data['case_band']
            watch.glass_type = form.cleaned_data['glass_type']
            watch.strap_type = form.cleaned_data['strap_type']
            watch.indication_type = form.cleaned_data['indication_type']
            watch.brand = form.cleaned_data['brand']
            watch.category = form.cleaned_data['category']
            watch.model_description = form.cleaned_data['model_description']
            if(form.cleaned_data['image'] != None and form.cleaned_data['image'] != ''):
                watch.image = form.cleaned_data['image']
            # print(1)
            # print(form.cleaned_data['image'])
            # print(1)
            feature_set = form.cleaned_data['model_features']

            watch.save()
            delete_set = WatchHasFeature.objects.filter(watch=watch).exclude(id__in=feature_set)
            if(delete_set != None):
                delete_set.delete()

            new_features = []
            for new_feature in feature_set.exclude(id__in=Feature.objects.filter(watchhasfeature__watch=watch)):
                new_features.append(WatchHasFeature(watch=watch, feature=new_feature))
            
            if(new_features != None):
                WatchHasFeature.objects.bulk_create(new_features)

            return HttpResponseRedirect('/login')

        return render(request, 'mainapp/change_watch.html', {'form': form, 'watch_id': watch_id})


class OrdersToProcessView(View):
    def get(self, request):
        orders = Order.objects.annotate(watches_list = GroupConcat(Concat('orderhasproduct__product_id__model_name', Value(' x '), 'orderhasproduct__quantity'), separator='\n'), user_username=F('user__username')) \
        .exclude(order_state__order_state_name__in=['Корзина', 'Отклонен', 'Оплачен', 'Не оплачен'])
        
        return render(request, 'mainapp/orders_to_process.html', {'orders': orders})


class MyCartView(View):
    def get(self, request):
        user = request.user
        cart = Order.objects.filter(user=user.id, order_state__order_state_name='Корзина').last()
        if(not cart):
            cart = Order.objects.create(order_state=OrderState.objects.get(order_state_name='Корзина'), user=user)
            cart.save()
        watches = OrderHasProduct.objects.annotate(total=F('product_id__model_cost')*F('quantity'), 
        model_id=F('product_id__id'), model_name=F('product_id__model_name'), model_cost=F('product_id__model_cost'), 
        model_description=F('product_id__model_description'), 
        brand_name=F('product_id__brand__brand_name'),
        image=F('product__image')).filter(order=cart.id)
        
        forms = []
        if watches != None and watches.count() > 0:
            for watch in watches:
                forms.append(CartItemForm(initial={'quantity':watch.quantity}))

        return render(request, 'mainapp/cart.html', {'watches': watches, 'forms': forms})


class ChangeOrderView(View):
    def get(self, request, order_id):
        order = Order.objects.annotate(order_state_name=F('order_state__order_state_name')).get(id=order_id)
        if order.order_state_name == 'Корзина':
            return HttpResponse(status=400)

        form = ChangeOrderForm(initial={
            'contact_name': order.contact_name,
            'contact_number': order.contact_number,
            'addit_wishes': order.addit_wishes,
            'order_address': order.order_address,
            'order_state': order.order_state
        })
        return render(request, 'mainapp/change_order.html', {'form': form, 'order_id': order_id})

    def post(self, request, order_id):
        form = ChangeOrderForm(request.POST)
        order = Order.objects.annotate(order_state_name=F('order_state__order_state_name')).get(id=order_id)
        if order.order_state_name == 'Корзина':
            return HttpResponse(status=400)
        elif form.is_valid():
            order.contact_name = form.cleaned_data['contact_name']
            order.contact_number = form.cleaned_data['contact_number']
            order.addit_wishes = form.cleaned_data['addit_wishes']
            order.order_address = form.cleaned_data['order_address']
            order.order_state = form.cleaned_data['order_state']
                        
            order.save()
            return HttpResponseRedirect('/login')

        return render(request, 'mainapp/change_order.html', {'form': form, 'order_id': order_id})


class MakeOrderView(View):
    def get(self, request):
        form = MakeOrderForm()
        return render(request, 'mainapp/make_order.html', {'form': form})

    def post(self, request):
        user = request.user
        form = MakeOrderForm(request.POST)
        order = Order.objects.filter(user=user, order_state__order_state_name='Корзина').last()
        if order == None:
            return HttpResponse(status=400)
        elif form.is_valid():
            order.contact_name = form.cleaned_data['contact_name']
            order.contact_number = form.cleaned_data['contact_number']
            order.addit_wishes = form.cleaned_data['addit_wishes']
            order.order_address = form.cleaned_data['order_address']
            order.order_state = OrderState.objects.get(order_state_name='Ожидает подтверждения')
            order.order_date = datetime.date.today()
                        
            order.save()
            return HttpResponseRedirect('/login')

        return render(request, 'mainapp/make_order.html', {'form': form})

class DeleteFromCartView(View):
    def post(self, request, watch_id):
        user = request.user
        watch_item = OrderHasProduct.objects.get(
            order_id__user=user, 
            order_id__order_state__order_state_name='Корзина',
            product_id__id=watch_id)
        watch_item.delete()

        return HttpResponseRedirect('/my_cart')

class AddToCartView(View):
    def post(self, request, watch_id):
        user = request.user
        form = CartItemForm(request.POST)
        order = Order.objects.get(user=user, order_state__order_state_name='Корзина')
        if form.is_valid():
            watch_item = OrderHasProduct(
                order=order, 
                product_id=watch_id,
                quantity=form.cleaned_data['quantity'])
            watch_item.save()

            return HttpResponseRedirect('/my_cart')

        return HttpResponse(status=400)

class ChangeQuantityInCartView(View):
    def post(self, request, watch_id):
        user = request.user
        form = CartItemForm(request.POST)
        #print(1)
        watch_item = OrderHasProduct.objects.annotate(model_id=F('product__id')).get(product__id=watch_id, order__user=user, order__order_state__order_state_name='Корзина')
        #print(2)
        #print(watch_item == None)
        if form.is_valid():
            watch_item.quantity = form.cleaned_data['quantity']
            watch_item.save()

            return HttpResponseRedirect('/my_cart')

        return HttpResponse(status=400)


class WatchView(View):
    def get(self, request, watch_id):
        user = request.user
        watch = Watch.objects.annotate(brand_name=F('brand__brand_name')) \
        .annotate(category_name=F('category__category_name')) \
        .annotate(mechanism_name=F('mechanism_type__mechanism_name')) \
        .annotate(glass_type_name=F('glass_type__glass_type_name')) \
        .annotate(strap_type_name=F('strap_type__strap_type_name')) \
        .annotate(case_type_name=F('case_band__case_type_name')) \
        .annotate(indication_type_name=F('indication_type__indication_type_name')) \
        .annotate(features_list = GroupConcat('watchhasfeature__feature__feature_name', separator='\n')) \
        .annotate(rating=Coalesce(Sum('rate__value') / Count('rate'), 0.0, output_field=DecimalField())) \
        .get(id=watch_id)

        in_cart = OrderHasProduct.objects.filter(order__order_state__order_state_name='Корзина',
                                                 order__user=user,
                                                 product=watch).aggregate(Sum('quantity'))['quantity__sum']
        if in_cart == None: in_cart = 0

        form = CartItemForm(initial={'quantity': in_cart})
        form.fields['quantity'].min_value = 100

        if watch == None:
            return HttpResponse(status=400)
        
        user_rating = Rate.objects.filter(user=user, watch=watch_id).aggregate(Sum('value'))['value__sum']
        rate_form = RateForm(initial={'value':(int(float(watch.rating)*2) if user_rating==None else int(float(user_rating)*2))})
        #print(user_rating)
        return render(request, 'mainapp/watch.html', {'watch': watch, 'form':form, 'in_cart':in_cart, 'rate_form':rate_form, 'user_rating':user_rating})


class RateView(View):
    def post(self, request, watch_id):
        user = request.user
        form = RateForm(request.POST)
        if Order.objects.filter(orderhasproduct__product_id=watch_id, user=user, order_state__order_state_name__in=['Оплачен', 'Не оплачен', 'Отклонен']).exists():
            return HttpResponse(status=403)

        rate = Rate.objects.filter(user=user, watch_id=watch_id).last()
        if rate == None:
            rate = Rate(user=user, watch_id=watch_id)

        if form.is_valid():
            rate.value = form.cleaned_data['value']/2
            print(form.cleaned_data['value'])
            rate.save()
            return HttpResponseRedirect('/watch/{}/'.format(watch_id))

        return HttpResponse(status=400)

class CatalogStatInfo(View):
    def get(self, request):
        return JsonResponse({'fg': 1})