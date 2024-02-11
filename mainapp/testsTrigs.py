from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import User
from .models import *
from .forms import *
from .views import *
# from Cart.models import *
# from Watches.models import *
from django.db import OperationalError
from django.db import connection
from django.db.models import F, Func

from django.contrib.auth.models import AnonymousUser


class TriggerTest(TestCase):
    def setUp(self):
        self.create_db_instances()

    def test_change_order_trigger_amount(self):
        order = Order(id=1, order_state_id=1, user=self.user, locality_id=1, payment_type_id=1)
        order.save()
        self.assertEqual(self.watch.current_amount, 100)
        OrderHasProduct(order_id=1, product_id=1, quantity=4).save()
        order.order_state_id = 2
        order.save()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 96)
        # order.order_state_id = 1
        # order.save()
        # self.assertEqual(self.watch.current_amount, 100)

    def test_change_ohp_trigger_amount(self):
        order = Order(id=1, order_state_id=1, user=self.user)
        order.save()
        ohp = OrderHasProduct(order_id=1, product_id=1, quantity=10)
        ohp.save()
        order.order_state_id = 2
        order.save()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 90)
        ohp.quantity = 11
        ohp.save()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 89)
        ohp.quantity = 10
        ohp.save()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 90)


    def test_delete_ohp_trigger_amount(self):
        order = Order(id=1, order_state_id=1, user=self.user)
        order.save()
        ohp = OrderHasProduct(order_id=1, product_id=1, quantity=10)
        ohp.save()
        order.order_state_id = 2
        order.save()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 90)
        ohp.delete()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 100)
    

    def test_delete_order_trigger_amount(self):
        order = Order(id=1, order_state_id=1, user=self.user)
        order.save()
        OrderHasProduct(order_id=1, product_id=1, quantity=4).save()
        order.order_state_id = 2
        order.save()
        self.assertEqual(Watch.objects.get(id=1).current_amount, 96)
        order.delete()
        self.assertEqual(self.watch.current_amount, 100)

    def test_insert_cart_trigger(self):
        order = Order(id=1, order_state_id=1, user=self.user)
        order.save()
        self.assertEqual(Order.objects.filter(order_state_id=1).count(), 1)
        order2 = Order(id=2, order_state_id=1, user=self.user)
        try:
            with transaction.atomic():
                order2.save()
        except Exception as e:
            self.assertEqual(e.args[0], 30062)
        self.assertEqual(Order.objects.filter(order_state_id=1).count(), 1)


    def test_update_cart_trigger(self):
        order = Order(id=1, order_state_id=2, user=self.user)
        order.save()
        try:
            with transaction.atomic():
                order.order_state_id = 1
                order.save()
        except Exception as e:
            self.assertEqual(e.args[0], 30060)

        order = Order.objects.filter(id=1).last()
        self.assertEqual(order.order_state_id, 2)

    def test_update_noted_cost(self):
        order = Order(id=1, order_state_id=1, user=self.user)
        order.save()
        ohp = OrderHasProduct(order_id=1, product_id=1, quantity=10)
        ohp.save()
        self.assertEqual(ohp.noted_cost, 0)
        order.order_state_id = 2
        order.save()
        ohp = OrderHasProduct.objects.all().last()
        self.assertEqual(ohp.noted_cost, 5000)
        # self.assertEqual(Order.objects.filter(order_state_id=1).count(), 1)    


    def create_db_instances(self):
        self.user = User.objects.create_user(email='user.user@gmail.com',
                                             username='user',
                                             password='userpassword')
        OrderState(id=1, order_state_name='Корзина').save()
        OrderState(id=2, order_state_name='Ожидает подтверждения').save()
        OrderState(id=3, order_state_name='Не оплачен').save()
        OrderState(id=4, order_state_name='Отклонен').save()
        PaymentType(id=1, payment_type_name='name').save()
        Locality(id=1, locality_name='name').save()
        Gender(id=1, gender_name='name').save()
        Brand(id=1, brand_name='brand', manufacturer_country='country').save()
        Category(id=1, category_name='name').save()
        IndicationType(id=1, indication_type_name='name').save()
        MechanismType(id=1, mechanism_name='name').save()
        GlassType(id=1, glass_type_name='name').save()
        StrapType(id=1, strap_type_name='name').save()
        CaseBand(id=1, case_type_name='name').save()
        self.watch = Watch(id=1, model_name='name', model_description='desc', model_cost=5000, current_amount=100,
                           case_band_id=1, indication_type_id=1, mechanism_type_id=1, glass_type_id=1, 
                           strap_type_id=1, category_id=1, brand_id=1, gender_id=1,
                           case_width=2, case_height=2, weight=2)
        self.watch.save()