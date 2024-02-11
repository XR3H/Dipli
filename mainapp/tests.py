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





class MakeOrderPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/make_order/')
        self.form_class = MakeOrderForm
        self.view = MakeOrderView
        self.prepare_db()

    def test_correct_data(self):
        # print(Locality.objects.filter(id=1).last()
        valid_data = {'contact_name': 'testname', 
                    'contact_number': '380507326483', 
                    'addit_wishes': 'test wishes', 
                    'order_address': 'test adress 0',
                    'locality' : Locality.objects.filter(id=1).last(),
                    'payment_type' : PaymentType.objects.filter(id=1).last()}

        self.form = self.form_class(data=valid_data)
        # print(self.form.errors)
        # print('--',self.form.errors['locality'][0], '--')

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.errors == {})

    def test_incorrect_data(self):
        invalid_data = valid_data = {'contact_name': 'test_name0', 
                                     'contact_number': '480507326483', 
                                     'addit_wishes': 'test wishes0', 
                                     'order_address': 'test adress 0' + 's'*255,
                                     'locality' : Locality.objects.filter(id=2).last(),
                                     'payment_type' : PaymentType.objects.filter(id=2).last()}

        self.form = self.form_class(data=invalid_data)

        self.assertFalse(self.form.is_valid())
        # print(self.form.errors)
        # print('--',self.form.errors['locality'][0], '--')

        self.assertEqual(self.form.errors['contact_name'][0],
                         'Контактное имя состоит из букв латиницы или кириллицы')
        self.assertEqual(self.form.errors['contact_number'][0],
                         'Контактный телефон состоит из цифр и начинается с 380')
        self.assertEqual(self.form.errors['addit_wishes'][0],
                         'Примечания состоят из букв латиницы или кириллицы')
        self.assertEqual(self.form.errors['order_address'][0],
                         'Адрес не может превышать 255 симолов')
        self.assertEqual('locality' in self.form.errors.keys(), True)
        self.assertEqual('payment_type' in self.form.errors.keys(), True)

    def test_request_anon(self):
        self.request.user = AnonymousUser()
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 403)

    def test_request_manager(self):
        self.request.user = self.superuser
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 403)

    def test_request_client(self):
        self.request.user = self.user
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def prepare_db(self):
        self.user = User.objects.create_user(email='user.user@gmail.com',
                                             username='user',
                                             password='userpassword')
        self.superuser = User.objects.create_superuser(email='superuser.superuser@gmail.com',
                                                       username='superuser',
                                                       password='superuserpassword')
        PaymentType(id=1, payment_type_name='test_payment').save()
        Locality(id=1, locality_name='test_locality').save()

class ChangeOrderPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/order/')
        self.form_class = ChangeOrderForm
        self.view = OrderView
        self.prepare_db()

    def test_correct_data(self):
        # print(Locality.objects.filter(id=1).last()
        valid_data = {'contact_name': 'testname', 
                    'contact_number': '380507326483', 
                    'addit_wishes': 'test wishes', 
                    'order_address': 'test adress 0',
                    'locality' : Locality.objects.filter(id=1).last(),
                    'payment_type' : PaymentType.objects.filter(id=1).last(),
                    'order_state' : OrderState.objects.filter(id=1).last()}

        self.form = self.form_class(data=valid_data)
        # print(self.form.errors)
        # print('--',self.form.errors['locality'][0], '--')

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.errors == {})

    def test_incorrect_data(self):
        invalid_data = valid_data = {'contact_name': 'test_name0', 
                                    'contact_number': '480507326483', 
                                    'addit_wishes': 'test wishes0', 
                                    'order_address': 'test adress 0' + 's'*255,
                                    'locality' : Locality.objects.filter(id=2).last(),
                                    'payment_type' : PaymentType.objects.filter(id=2).last(),
                                    'order_state' : OrderState.objects.filter(id=2).last()}

        self.form = self.form_class(data=invalid_data)

        self.assertFalse(self.form.is_valid())
        # print('--',self.form.errors['locality'][0], '--')

        self.assertEqual(self.form.errors['contact_name'][0],
                         'Контактное имя состоит из букв латиницы или кириллицы')
        self.assertEqual(self.form.errors['contact_number'][0],
                         'Контактный телефон состоит из цифр и начинается с 380')
        self.assertEqual(self.form.errors['addit_wishes'][0],
                         'Примечания состоят из букв латиницы или кириллицы')
        self.assertEqual(self.form.errors['order_address'][0],
                         'Адрес не может превышать 255 симолов')
        self.assertEqual('locality' in self.form.errors.keys(), True)
        self.assertEqual('payment_type' in self.form.errors.keys(), True)
        self.assertEqual('order_state' in self.form.errors.keys(), True)

    def test_request_anon(self):
        self.request.user = AnonymousUser()
        self.request.method = 'POST'
        response = self.view.as_view()(self.request, self.order.id)
        self.assertEqual(response.status_code, 403)

    def test_request_manager(self):
        self.request.user = self.superuser
        self.request.method = 'POST'
        response = self.view.as_view()(self.request, self.order.id)
        self.assertEqual(response.status_code, 200)

    def test_request_client(self):
        self.request.user = self.user
        self.request.method = 'POST'
        response = self.view.as_view()(self.request, self.order.id)
        self.assertEqual(response.status_code, 403)

    def prepare_db(self):
        self.user = User.objects.create_user(email='user.user@gmail.com',
                                             username='user',
                                             password='userpassword')
        self.superuser = User.objects.create_superuser(email='superuser.superuser@gmail.com',
                                                       username='superuser',
                                                       password='superuserpassword')
        PaymentType(id=1, payment_type_name='test_payment').save()
        Locality(id=1, locality_name='test_locality').save()
        OrderState(id=1, order_state_name='test_state').save()
        self.order = Order(id=1, order_state_id=1, user=self.user)
        self.order.save()

class AddWatchPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/add_watch/')
        self.form_class = AddWatchForm
        self.view = AddWatchView
        self.prepare_db()

    def test_correct_data(self):
        # print(Locality.objects.filter(id=1).last()
        valid_data = {'model_name': 'test_name', 
                    'model_cost': 2000.0, 
                    'case_width': 42.0, 
                    'case_height': 42.0,
                    'weight' : 95.0,
                    'gender' : Gender.objects.filter(id=1).last(),
                    'waterproof_level' : 20,
                    'current_amount' : 90,
                    'indication_type' : IndicationType.objects.filter(id=1).last(),
                    'mechanism_type' : MechanismType.objects.filter(id=1).last(),
                    'case_band' : CaseBand.objects.filter(id=1).last(),
                    'glass_type' : GlassType.objects.filter(id=1).last(),
                    'strap_type' : StrapType.objects.filter(id=1).last(),
                    'brand' : Brand.objects.filter(id=1).last(),
                    'category' : Category.objects.filter(id=1).last(),
                    'model_description': 'testdescription',
                    'image': 'test_image'}

        self.form = self.form_class(data=valid_data)
        # print(self.form.errors)
        # print(self.form.errors)
        # print('--',self.form.errors['locality'][0], '--')

        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.errors == {})

    def test_incorrect_data(self):
        invalid_data = {'model_name': 'test_name*', 
                    'model_cost': -1, 
                    'case_width': -1, 
                    'case_height': -1,
                    'weight' : -1,
                    'gender' : Gender.objects.filter(id=2).last(),
                    'waterproof_level' : 2000,
                    'current_amount' : 2000,
                    'indication_type' : IndicationType.objects.filter(id=100).last(),
                    'mechanism_type' : MechanismType.objects.filter(id=2).last(),
                    'case_band' : CaseBand.objects.filter(id=2).last(),
                    'glass_type' : GlassType.objects.filter(id=2).last(),
                    'strap_type' : StrapType.objects.filter(id=2).last(),
                    'brand' : Brand.objects.filter(id=2).last(),
                    'category' : Category.objects.filter(id=2).last(),
                    'model_description': 'testdescription*',
                    'image': 'test_image'}

        self.form = self.form_class(data=invalid_data)
        # print(self.form.errors)
        # print(self.form.errors)
        # print('--',self.form.errors['locality'][0], '--')

        self.assertEqual(self.form.errors['model_name'][0],
                         'Название модели состоит из букв латиницы, кириллицы или цифр')
        self.assertEqual(self.form.errors['model_cost'][0],
                         'Цена не может быть ниже 1')
        self.assertEqual(self.form.errors['case_width'][0],
                         'Ширина корпуса не может быть ниже 1')
        self.assertEqual(self.form.errors['case_height'][0],
                         'Высота корпуса не может быть ниже 1')
        self.assertEqual(self.form.errors['weight'][0],
                         'Вес не может быть ниже 1')
        self.assertEqual(self.form.errors['waterproof_level'][0],
                         'Уровень водонепроницаемости не может превышать 300')
        self.assertEqual(self.form.errors['current_amount'][0],
                         'Кол-во не может превышать 1000')
        self.assertEqual(self.form.errors['model_description'][0],
                         'Описание состоит из букв латиницы или кириллицы')
        # print(self.form.errors.keys())
        self.assertEqual('mechanism_type' in self.form.errors.keys(), True)
        self.assertEqual('indication_type' in self.form.errors.keys(), True)
        self.assertEqual('case_band' in self.form.errors.keys(), True)
        self.assertEqual('glass_type' in self.form.errors.keys(), True)
        self.assertEqual('strap_type' in self.form.errors.keys(), True)
        self.assertEqual('gender' in self.form.errors.keys(), True)
        self.assertEqual('brand' in self.form.errors.keys(), True)
        self.assertEqual('category' in self.form.errors.keys(), True)

    def test_request_anon(self):
        self.request.user = AnonymousUser()
        self.request.method = 'POST'
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 403)

    def test_request_manager(self):
        self.request.user = self.superuser
        self.request.method = 'POST'
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_request_client(self):
        self.request.user = self.user
        self.request.method = 'POST'
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 403)

    def prepare_db(self):
        self.user = User.objects.create_user(email='user.user@gmail.com',
                                             username='user',
                                             password='userpassword')
        self.superuser = User.objects.create_superuser(email='superuser.superuser@gmail.com',
                                                       username='superuser',
                                                       password='superuserpassword')
        Gender(id=1, gender_name='test').save()
        Brand(id=1, brand_name='brand', manufacturer_country='country').save()
        Category(id=1, category_name='name').save()
        IndicationType(id=1, indication_type_name='name').save()
        MechanismType(id=1, mechanism_name='name').save()
        GlassType(id=1, glass_type_name='name').save()
        StrapType(id=1, strap_type_name='name').save()
        CaseBand(id=1, case_type_name='name').save()

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