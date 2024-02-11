from django.urls import path
from django.conf.urls import url
from . import views
from . import forms

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    url('register/', views.RegistrationView.as_view(), name = 'register'),
    url('login/', views.LoginView.as_view(), name = 'login'),
    url('catalog/', views.CatalogView.as_view(), name = 'catalog'),
    url('add_watch/', views.AddWatchView.as_view(), name = 'add_watch'),
    url('profile/', views.ProfileView.as_view(), name = 'profile'),
    url('change_password/', views.ChangePasswordView.as_view(), name = 'change_password'),
    url('my_orders/', views.UserOrdersView.as_view(), name = 'my_orders'),
    path('change_watch/<int:watch_id>/', views.ChangeWatchView.as_view(), name = 'change_watch'),
    url('orders_to_process/', views.OrdersToProcessView.as_view(), name = 'orders_to_process'),
    url('cart/', views.MyCartView.as_view(), name = 'cart'),
    url('clearCart/', login_required(views.ClearCartView.as_view()), name='clearCart'),
    path('order/<int:order_id>/', views.OrderView.as_view(), name = 'order'),
    url('make_order/', login_required(views.MakeOrderView.as_view()), name = 'make_order'),
    path('delete_item/<int:watch_id>/', views.DeleteFromCartView.as_view(), name = 'delete_item'),
    path('add/<int:watch_id>/', views.AddToCartView.as_view(), name = 'add'),
    path('cha/<int:watch_id>/', views.ChangeQuantityInCartView.as_view(), name = 'cha'),
    path('watch/<int:watch_id>/', views.WatchView.as_view(), name = 'watch'),
    path('rate/<int:watch_id>/', views.RateView.as_view(), name = 'rate'),
    # url('testinf/', views.CatalogStatInfo.as_view(), name = 'testinf'),

    url('afterloginredirect/', views.afterlogin, name = 'afterloginredirect'),
    url('logout/', views.logout_user, name = 'logout'),
]
