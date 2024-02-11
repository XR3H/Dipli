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


from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import *

from .StatistSystem import *
from .DBManager import *

from django.core.paginator import Paginator


def index(request):
    row = DBManager.SelectAllMeals()
    return render(request, 'mainapp/index.html')

@login_required
def afterlogin(request):
    return redirect('/')

@login_required
def logout_user(request):
    if request.user.is_active:
        logout(request)
    return redirect('/login/')






class RegistrationView(View): #V
    form = RegistrationForm
    template = 'mainapp/register.html'
    success_url = '/login'

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password']
            )
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template, {'form': form})

    def get(self, request):
    #     for i in range(30):
    #         User.objects.create_user(username='kararotto'+str(i), password='11111111', email='mrvladoh1337@gmail.com')

        #User.objects.create_superuser(username='evergreeen', password='11111111', email='mrvladoh1337@gmail.com')
        form = self.form()
        return render(request, self.template, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if(self.request.user.is_authenticated):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)


class LoginView(View): #V
    form = AuthenticationForm
    template = 'mainapp/login.html'
    success_url = '/catalog'

    def post(self, request):
        # if(request.user.is_authenticated):
        #     return HttpResponse(status=403)
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(request, 
                username=form.cleaned_data['login'], 
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(self.success_url)

        return render(request, self.template, {'form': form})

    # if a GET (or any other method) we'll create a blank form
    def get(self, request):
        # if(request.user.is_authenticated):
        #     return HttpResponse(status=403)
        # Order.objects.filter(id=29).last().delete()
        form = self.form()
        return render(request, self.template, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if(self.request.user.is_authenticated):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

# class CatalogView(View):
#     def get(self, request):
#         watches = DBManager.get_all_watches()
#         info = DBManager.get_top_catalog_info()
#         return render(request, 'mainapp/catalog.html', {'watches': watches, 'info': json.dumps(info)})

class CatalogView(TemplateView):
    template_name = 'mainapp/catalog.html'
    
    def get_context_data(self, **kwargs):
        watches = DBManager.get_all_watches()
        paginator = Paginator(watches, 9)
        page_number = self.request.GET.get('page')
        print(page_number)
        watches = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['watches'] = watches
        # context['page_obj'] = page_obj
        info = StatistSystem.get_top_catalog_info()
        context['info'] = json.dumps(info)
        # print(self.request.user.username)
        return context



class AddWatchView(View):
    form = AddWatchForm
    template = 'mainapp/add_watch.html'
    success_url = '/watch/{}'

    def get(self, request):
        # if(not request.user.is_authenticated or not request.user.is_staff):
        #     return HttpResponse(status=403)
        form = self.form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        # if(not request.user.is_authenticated or not request.user.is_staff):
        #     return HttpResponse(status=403)
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            new_watch = DBManager.create_watch(form)
            DBManager.watch_set_features(new_watch.id, form.cleaned_data['model_features'])
            return HttpResponseRedirect(self.success_url.format(new_watch.id))

        return render(request, self.template, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or not self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)


class ChangeWatchView(View):
    def get(self, request, watch_id):
        # if(not request.user.is_authenticated or not request.user.is_staff):
        #     return HttpResponse(status=403)
        watch = DBManager.get_watch_by_id(watch_id)
        form = AddWatchForm(initial={
            'model_name': watch.model_name, 'model_cost': watch.model_cost,
            'case_width': watch.case_width, 'case_height': watch.case_height,
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
        return render(request, 'mainapp/change_watch.html', {'form': form, 'watch_id': watch_id})

    def post(self, request, watch_id):
        # if(not request.user.is_authenticated or not request.user.is_staff):
        #     return HttpResponse(status=403)
        form = AddWatchForm(request.POST, request.FILES)
        watch = DBManager.get_watch_by_id(watch_id)
        if form.is_valid():
            DBManager.update_watch(watch, form)
            DBManager.watch_set_features(watch.id, form.cleaned_data['model_features'])     
            return HttpResponseRedirect('/login')

        return render(request, 'mainapp/change_watch.html', {'form': form, 'watch_id': watch_id})

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or not self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)




# class ProfileView(View):
#     def get(self, request):
#         user = request.user
#         form = ProfileForm(initial={'login': user.username,
#                                     'email': user.email,
#                                     'first_name': user.first_name,
#                                     'last_name': user.last_name})
#         return render(request, 'mainapp/profile.html', {'form': form})

class ProfileView(TemplateView):
    template_name = 'mainapp/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['form'] = ProfileForm(initial={
            'login': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)


# class UserOrdersView(View):
#     def get(self, request):
#         user = request.user
#         orders = Order.objects.annotate(
#             watches_list = GroupConcat(Concat('orderhasproduct__product_id__model_name', Value(' x '), 'orderhasproduct__quantity'), separator='\n'),
#             order_state_name = F('order_state__order_state_name'),
#             payment_type_name = F('payment_type__payment_type_name'),
#             locality_name = F('locality__locality_name')
#         ).filter(user_id=user.id).exclude(order_state__order_state_name='Корзина')
#         return render(request, 'mainapp/my_orders.html', {'orders': orders})


class UserOrdersView(TemplateView):
    template_name = 'mainapp/my_orders.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['orders'] = DBManager.get_orders(user.id)        
        return context

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

        # context['orders'] = Order.objects.annotate(
        #     watches_list = GroupConcat(Concat('orderhasproduct__product_id__model_name', Value(' x '), 'orderhasproduct__quantity'), separator='\n'),
        #     order_state_name = F('order_state__order_state_name'),
        #     payment_type_name = F('payment_type__payment_type_name'),
        #     locality_name = F('locality__locality_name')
        # ).filter(user_id=user.id).exclude(order_state__order_state_name='Корзина')



# class OrdersToProcessView(View):
#     def get(self, request):
#         orders = Order.objects.annotate(watches_list = GroupConcat(Concat('orderhasproduct__product_id__model_name', Value(' x '), 'orderhasproduct__quantity'), separator='\n'), user_username=F('user__username')) \
#         .exclude(order_state__order_state_name__in=['Корзина', 'Отклонен', 'Оплачен', 'Не оплачен'])
        
#         return render(request, 'mainapp/orders_to_process.html', {'orders': orders})

class OrdersToProcessView(TemplateView):
    template_name = 'mainapp/orders_to_process.html'
    # permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # if(not user.is_staff):
        #     return HttpResponse(status=403)
        context['orders'] = DBManager.get_orders()        
        return context

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or not self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

# context['orders'] = Order.objects.annotate(watches_list = GroupConcat(Concat('orderhasproduct__product_id__model_name', Value(' x '), 'orderhasproduct__quantity'), separator='\n'), user_username=F('user__username')) \
#         .exclude(order_state__order_state_name__in=['Корзина', 'Отклонен', 'Оплачен', 'Не оплачен'])


# class MyCartView(View):
#     def get(self, request):
#         user = request.user
#         cart = Order.objects.filter(user=user.id, order_state__order_state_name='Корзина').last()
#         if(not cart):
#             cart = Order.objects.create(order_state=OrderState.objects.get(order_state_name='Корзина'), user=user)
#             cart.save()
#         watches = OrderHasProduct.objects.annotate(total=F('product_id__model_cost')*F('quantity'), 
#         model_id=F('product_id__id'), model_name=F('product_id__model_name'), model_cost=F('product_id__model_cost'), 
#         model_description=F('product_id__model_description'), 
#         brand_name=F('product_id__brand__brand_name'),
#         image=F('product__image')).filter(order=cart.id)

#         total_cost = watches.aggregate(total_cost=Sum(F('quantity')*F('model_cost')))['total_cost']
#         info = DBManager.get_compare_info([watch.product_id for watch in watches])

#         return render(request, 'mainapp/cart.html', {'watches': watches, 'total_cost':total_cost, 'info': json.dumps(info)})

class MyCartView(TemplateView):
    template_name = 'mainapp/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = DBManager.get_user_cart(user)
        if(not cart):
            order = Order(user=user, order_state_id=1)
            order.save()
        watches = DBManager.get_order_content(cart.id)
        # info = DBManager.get_compare_info([watch.product_id for watch in watches])
        info = StatistSystem.get_watch_comparing_info([watch.product_id for watch in watches])
        context['watches'] = watches
        context['total_cost'] = watches.aggregate(total_cost=Sum(F('quantity')*F('model_cost')))['total_cost']
        context['info'] = json.dumps(info)
        # DBManager.stat_compare_by_rating([watch.product_id for watch in watches])
        return context

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)


#   def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         cart = Order.objects.filter(user=user.id, order_state__order_state_name='Корзина').last()
#         if(not cart):
#             cart = Order.objects.create(order_state=OrderState.objects.get(order_state_name='Корзина'), user=user)
#             cart.save()
#         watches = OrderHasProduct.objects.annotate(total=F('product_id__model_cost')*F('quantity'), 
#             model_id=F('product_id__id'), model_name=F('product_id__model_name'), model_cost=F('product_id__model_cost'), 
#             model_description=F('product_id__model_description'), 
#             brand_name=F('product_id__brand__brand_name'),
#             image=F('product__image')).filter(order=cart.id)
#         info = DBManager.get_compare_info([watch.product_id for watch in watches])
#         context['watches'] = watches
#         context['total_cost'] = watches.aggregate(total_cost=Sum(F('quantity')*F('model_cost')))['total_cost']
#         context['info'] = json.dumps(info)
#         return context


class OrderView(View):
    form = ChangeOrderForm
    template = 'mainapp/order.html'
    success_url = '/order/{}'

    def get(self, request, order_id):
        order = DBManager.get_order_by_id(order_id)
        if order.order_state == 'Корзина':
            return HttpResponse(status=400)

        form = self.form(initial={
            'contact_name': order.contact_name,
            'contact_number': order.contact_number,
            'addit_wishes': order.addit_wishes,
            'locality' : order.locality,
            'order_address': order.order_address,
            'payment_type' : order.payment_type,
            'order_state': order.order_state
        })
        form.pass_perm(request.user)
        watches = DBManager.get_order_content(order_id)
        return render(request, self.template, {'form': form, 'order_id': order_id, 'watches':watches})

    def post(self, request, order_id):
        form = self.form(request.POST)
        order = DBManager.get_order_by_id(order_id)
        if order.order_state == 'Корзина':
            return HttpResponse(status=400)
        elif form.is_valid():
            DBManager.update_order(order, form)
            return HttpResponseRedirect(self.success_url.format(order_id))

        return render(request, self.template, {'form': form, 'order_id': order_id})

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or (request.method == 'POST' and not self.request.user.is_staff)):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)


class MakeOrderView(View):
    form = MakeOrderForm
    template = 'mainapp/make_order.html'
    success_url = '/order/{}'

    def get(self, request):
        form = self.form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        user = request.user
        form = self.form(request.POST)
        if form.is_valid():
            order = DBManager.get_user_cart(user)
            if order == None:
                return HttpResponse(status=400)
                
            order = DBManager.make_order(order, form)
            return HttpResponseRedirect(self.success_url.format(order.id))

        return render(request, self.template, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

class DeleteFromCartView(View):
    def post(self, request, watch_id):
        user = request.user
        watch_item = OrderHasProduct.objects.get(
            order_id__user=user, 
            order_id__order_state__order_state_name='Корзина',
            product_id__id=watch_id)
        watch_item.delete()
        return HttpResponseRedirect('/my_cart')

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

class AddToCartView(View):
    def post(self, request, watch_id):
        user = request.user
        form = CartItemForm(request.POST)
        order = Order.objects.filter(user=user, order_state__order_state_name='Корзина').last()
        if(order==None):
                order = Order(user=user, order_state_id=1)
                order.save()
        if form.is_valid():
            watch_item = OrderHasProduct(
                order=order, 
                product_id=watch_id,
                quantity=form.cleaned_data['quantity'])
            watch_item.save()
            return HttpResponseRedirect('/my_cart')
        return HttpResponse(status=400)

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)


class WatchView(View):
    template = 'mainapp/watch.html'

    def get(self, request, watch_id):
        user = request.user
        watch = DBManager.get_watch_info(watch_id)
        if watch == None:
            return HttpResponse(status=400)
        context = {
            'watch': watch
        }
        
        if(user.is_authenticated and not user.is_staff):
            in_cart = DBManager.watch_in_cart(watch.id, user.id)
            user_rating = DBManager.user_watch_rating(watch_id, user.id)
            context['in_cart'] = in_cart
            context['form'] = CartItemForm(initial={'quantity': in_cart})
            context['user_rating'] = user_rating
            context['rate_form'] = RateForm(initial={'value':(int(float(watch.rating)*2) if user_rating==None else int(float(user_rating)*2))})

        info = StatistSystem.get_watch_addit_info(watch_id)
        context['info'] = json.dumps(info)
        # print(user.id)
        if(user.is_authenticated and not user.is_staff):
            recommends = StatistSystem.get_user_recommendations(user.id, watch)
            context['recommends'] = json.dumps(recommends)
        else:
            context['recommends'] = json.dumps([])

        return render(request, self.template, context)


class RateView(View):
    success_url = '/watch/{}/'

    def post(self, request, watch_id):
        user = request.user
        form = RateForm(request.POST)
        if DBManager.user_bought_watch(user.id, watch_id):
            return HttpResponse(status=403)

        if form.is_valid():
            rate = Rate.objects.filter(user=user, watch_id=watch_id).last()
            if rate == None:
                rate = Rate(user=user, watch_id=watch_id)
            rate.value = form.cleaned_data['value']/2
            rate.save()
            return HttpResponseRedirect(self.success_url.format(watch_id))

        return HttpResponse(status=400)

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

class ClearCartView(View):
    success_url = '/cart/'

    # @login_required
    def post(self, request):
        user = request.user
        DBManager.clear_user_cart(user)
        return HttpResponseRedirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated or self.request.user.is_staff):
            return HttpResponse(status=403)
        return super().dispatch(request, *args, **kwargs)

# class CatalogStatInfo(View):
#     def get(self, request):
#         return JsonResponse({'fg': 1})