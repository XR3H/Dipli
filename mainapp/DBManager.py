from django.db import connection
from .models import *
import datetime
from django.db import transaction
from django.db.models import F, Func
from django.db.models import Subquery, OuterRef
from django_mysql.models import GroupConcat
from django.db.models.functions import Concat
from django.db.models.functions import Coalesce
from django.db.models import *

from MySQLdb.cursors import DictCursor
from django.db import connections

class DBManager:

    @staticmethod
    def get_order_by_id(order_id):
        order = Order.objects.select_related('order_state', 'payment_type') \
        .filter(id=order_id).last()
        return order


    @staticmethod
    def order_set_data(order, form):
        order.contact_name = form.cleaned_data['contact_name']
        order.contact_number = form.cleaned_data['contact_number']
        order.addit_wishes = form.cleaned_data['addit_wishes']
        order.order_address = form.cleaned_data['order_address']
        order.payment_type = form.cleaned_data['payment_type']
        order.locality = form.cleaned_data['locality']

    @staticmethod
    def make_order(order, form):
        DBManager.order_set_data(order, form)
        order.order_state = OrderState.objects.get(
            order_state_name='Ожидает подтверждения'
            )
        order.order_date = datetime.date.today()
        order.save()
        OrderHasProduct.objects.filter(order=order).update(
            noted_cost=Subquery(Watch.objects.filter(
                id=OuterRef('product_id')
            ).values('model_cost')[:1])
        )
        return order

    @staticmethod
    def update_order(order, form):
        DBManager.order_set_data(order, form)
        order.order_state = form.cleaned_data['order_state']
        order.save()


    @staticmethod
    def get_user_cart(user):
        return Order.objects.filter(
            user=user, 
            order_state__order_state_name='Корзина'
            ).last()

    @staticmethod
    def stat_watch_rates_info(watch_id):
        watch_rates = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.execute("SELECT rates.* " 
            + f"FROM (SELECT @watch_id:={watch_id}) i, test_watch_rates rates;")
            watch_rates = cursor.fetchall()
        return watch_rates

    @staticmethod
    def stat_watch_top_locals(watch_id):
        top_local_ordered = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.execute(f"SELECT top_local.* FROM (SELECT @watch_id:={watch_id}) i, test_watch_top_localities top_local;")
            top_local = cursor.fetchall()            
            if(len(top_local) >= 5):
                for i in range(len(top_local)):
                    item = {
                        'id': top_local[i]['id'], 
                        'locality_name': top_local[i]['locality_name'], 
                        'place': len(top_local)-i}
                    if(i%2 == 1):
                        top_local_ordered.insert(0, item)
                    else:
                        top_local_ordered.append(item)
        return top_local_ordered

        

    @staticmethod
    def get_order_content(order_id):
        watches = OrderHasProduct.objects.annotate(
            total=F('product_id__model_cost')*F('quantity'), 
            model_id=F('product_id__id'), 
            model_name=F('product_id__model_name'), 
            model_cost=F('product_id__model_cost'), 
            model_category=F('product__category__category_name'), 
            brand_name=F('product_id__brand__brand_name'),
            image=F('product__image')
        ).filter(order_id=order_id)
        return watches


#         info = {}
#         comparing_res = None
#         if(len(watch_ids) >= 2):
#             prep_list_str = ''
#             prep_list_str += str(watch_ids)[1:-1]
#             con = connections['default']
#             with con.connection.cursor(DictCursor) as cursor:
#                 cursor.callproc('Compare', [prep_list_str])
#                 comparing_res = cursor.fetchall()
#                 # print(comparing_res)
#                 sales_ceil = max([item['amount'] for item in comparing_res])
#                 if(sales_ceil > 0):
#                     for item in comparing_res:
#                         item['amount'] /= sales_ceil/100
#                 info['compare_sales'] = comparing_res
#         # print(comparing_res)
#         return info



    @staticmethod
    def get_ratings():
        res_ratings = {}
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM test_get_ratings")
            ratings = cursor.fetchall()
            formated_ratings = []
            curr_id = ratings[0]['user']
            user_ids = [curr_id]
            watch_ids = []
            watch_flag = True
            temp_list = []
            ceil_watch = max([rate['watch'] for rate in ratings])
            for rate in ratings:
                if(rate['user'] != curr_id):
                    curr_id = rate['user']
                    user_ids.append(curr_id)
                    watch_flag = False
                    temp_list = []
                temp_list.append(rate['rate'])
                if(watch_flag):
                    watch_ids.append(rate['watch'])
                if(rate['watch'] == ceil_watch):
                    formated_ratings.append(temp_list)
            # print(user_ids)
            # print(watch_ids)
            res_ratings['user_ids'] = user_ids
            res_ratings['watch_ids'] = watch_ids
            res_ratings['rates'] = formated_ratings
        return res_ratings

    @staticmethod
    def get_similar_watches(watch, amount):
        watches = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.callproc('GetSimilarWatches', [
                watch.id, watch.gender_id,
                watch.category_id, watch.model_cost,
                watch.case_band_id, watch.mechanism_type_id,
                watch.indication_type_id, watch.glass_type_id,
                watch.strap_type_id, watch.brand_id, amount
                ])
            watches = cursor.fetchall()
            # print(watches)
        return watches

    @staticmethod
    def get_user_acquainted(user_id):
        watch_list = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.callproc('UserAcquainted', [user_id])
            query = cursor.fetchall()            
            watch_list = [i['id'] for i in query]
            # print(watch_list)
        return watch_list

    @staticmethod
    def get_watches_by_id(ids):
        watches = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.callproc('GetWatchesById', [str(ids)[1:-1]])
            watches = cursor.fetchall()            
        return watches


    @staticmethod
    def get_watch_by_id(watch_id):
        return Watch.objects.filter(id=watch_id).last()

    @staticmethod
    def clear_user_cart(user):
        OrderHasProduct.objects.filter(order__user=user, order__order_state__order_state_name='Корзина').delete()


        # watches = Watch.objects.all().order_by('id').annotate(brand_name=F('brand__brand_name')) \
        # .annotate(category_name=F('category__category_name')) \
        # .annotate(mechanism_name=F('mechanism_type__mechanism_name')) \
        # .annotate(glass_type_name=F('glass_type__glass_type_name')) \
        # .annotate(strap_type_name=F('strap_type__strap_type_name')) \
        # .annotate(case_type_name=F('case_band__case_type_name')) \
        # .annotate(indication_type_name=F('indication_type__indication_type_name'))

    @staticmethod
    def get_all_watches():
        watches = Watch.objects.all().order_by('id').select_related('brand', 'category', 'gender')
        return watches

    @staticmethod
    def create_watch(form):
        new_watch = Watch(model_name=form.cleaned_data['model_name'],
                              model_cost=form.cleaned_data['model_cost'],
                              case_height=form.cleaned_data['case_height'],
                              case_width=form.cleaned_data['case_width'],
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
        new_watch.save()
        return new_watch

    @staticmethod
    def update_watch(watch, form):
        watch.model_name = form.cleaned_data['model_name']
        watch.model_cost = form.cleaned_data['model_cost']
        watch.case_width = form.cleaned_data['case_width']
        watch.case_height = form.cleaned_data['case_width']
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
        watch.save()

    @staticmethod
    def watch_set_features(watch_id, feature_set):
        # feature_list = []
        # for feature in features:
        #     feature_list.append(WatchHasFeature(watch_id=watch_id, feature=feature))
            
        # WatchHasFeature.objects.bulk_create(feature_list)
        delete_set = WatchHasFeature.objects.filter(watch_id=watch_id).exclude(id__in=feature_set)
        if(delete_set != None):
            delete_set.delete()

        new_features = []
        for new_feature in feature_set.exclude(id__in=Feature.objects.filter(watchhasfeature__watch_id=watch_id)):
            new_features.append(WatchHasFeature(watch_id=watch_id, feature=new_feature))
            
        if(new_features != None):
            WatchHasFeature.objects.bulk_create(new_features)

        # watch = Watch.objects.annotate(brand_name=F('brand__brand_name')) \
        # .annotate(category_name=F('category__category_name')) \
        # .annotate(mechanism_name=F('mechanism_type__mechanism_name')) \
        # .annotate(glass_type_name=F('glass_type__glass_type_name')) \
        # .annotate(strap_type_name=F('strap_type__strap_type_name')) \
        # .annotate(case_type_name=F('case_band__case_type_name')) \
        # .annotate(indication_type_name=F('indication_type__indication_type_name')) \
        # .annotate(features_list = GroupConcat('watchhasfeature__feature__feature_name', separator='\n')) \
        # .annotate(rating=Coalesce(Sum('rate__value') / Count('rate'), 0.0, output_field=DecimalField())) \
        # .annotate(gender_name=F('gender__gender_name')) \
        # .get(id=watch_id)


    @staticmethod
    def get_watch_info(watch_id):
        watch = Watch.objects.select_related(
            'brand', 'category',
            'mechanism_type', 'glass_type',
            'strap_type', 'case_band',
            'indication_type', 'gender') \
            .annotate(features_list = GroupConcat(
                'watchhasfeature__feature__feature_name', 
                separator='\n')) \
            .annotate(rating=Coalesce(
                Sum('rate__value') / Count('rate'), 0.0, 
                output_field=DecimalField())) \
            .annotate(gender_name=F('gender__gender_name')) \
            .get(id=watch_id)
        return watch

    @staticmethod
    def get_orders(user_id=None):
        orders = Order.objects.select_related(
            'order_state', 'payment_type', 'locality'
        ).annotate(watches_list = GroupConcat(
            Concat(
                'orderhasproduct__product_id__model_name', Value(' x '), 
                'orderhasproduct__quantity'), separator='\n'
            )
        )
        if(user_id):
            orders = orders.filter(user_id=user_id).exclude(
                order_state__order_state_name='Корзина'
            )
        else:
            orders = orders.annotate( 
                user_username=F('user__username')
            ).exclude(order_state__order_state_name__in=[
                'Корзина', 'Отклонен', 
                'Оплачен', 'Не оплачен'
            ])
        return orders

    @staticmethod
    def watch_in_cart(watch_id, user_id):
        in_cart = OrderHasProduct.objects.filter(
            order__order_state__order_state_name='Корзина',
            order__user_id=user_id,
            product_id=watch_id
        ).aggregate(Sum('quantity'))['quantity__sum']
        in_cart = 0 if in_cart == None else in_cart
        return in_cart

    @staticmethod
    def user_watch_rating(watch_id, user_id):
        rating = Rate.objects.filter(
            user_id=user_id, 
            watch=watch_id
        ).aggregate(Sum('value'))['value__sum']
        return rating

    @staticmethod
    def user_bought_watch(user_id, watch_id):
        if_bought = Order.objects.filter(
            orderhasproduct__product_id=watch_id, 
            user_id=user_id, 
            order_state__order_state_name__in=['Оплачен', 'Не оплачен', 'Отклонен']
        ).exists()
        return if_bought

    # @staticmethod
    # def stat_compare_by_rating(watch_ids):
    #     info = {}
    #     comparing_res = None
    #     if(len(watch_ids) >= 2):
    #         con = connections['default']
    #         with con.connection.cursor(DictCursor) as cursor:
    #             cursor.callproc('CompareByRates', [str(watch_ids)[1:-1], 14])
    #             comparing_res = cursor.fetchall()
    #             format_res = {}
    #             curr_watch = comparing_res[0]['model_name']
    #             model_curve = ()
    #             for item in comparing_res:
    #                 temp_dict = {}
    #                 if(item['model_name'] != curr_watch):
    #                     curr_watch = item['model_name']
    #                     model_curve = ()
    #                 temp_dict['date_inter'] = item['date_inter']
    #                 temp_dict['avg_rate'] = item['avg_rate']
    #                 model_curve = (*model_curve, temp_dict)
    #                 if item['n'] == 0:
    #                     format_res[item['model_name']] = model_curve
    #             print(format_res)
    #             info['compare_rates'] = format_res
    #     return info

    # @staticmethod
    # def get_compare_info(watch_ids):
    #     info = {}
    #     comparing_res = None
    #     if(len(watch_ids) >= 2):
    #         prep_list_str = ''
    #         prep_list_str += str(watch_ids)[1:-1]
    #         con = connections['default']
    #         with con.connection.cursor(DictCursor) as cursor:
    #             cursor.callproc('Compare', [prep_list_str])
    #             comparing_res = cursor.fetchall()
    #             sales_ceil = max([item['amount'] for item in comparing_res])
    #             format_res = {}
    #             curr_watch = comparing_res[0]['model_name']
    #             model_curve = ()
    #             for item in comparing_res:
    #                 temp_dict = {}
    #                 if(item['model_name'] != curr_watch):
    #                     curr_watch = item['model_name']
    #                     model_curve = ()
    #                 temp_dict['date_inter'] = item['date_inter']
    #                 temp_dict['amount'] = item['amount']
    #                 if(sales_ceil > 0):
    #                     temp_dict['amount'] /= sales_ceil/100
    #                 model_curve = (*model_curve, temp_dict)
    #                 if item['n'] == 0:
    #                     format_res[item['model_name']] = model_curve
    #             info['compare_sales'] = format_res
    #     return info

    @staticmethod
    def stat_compare_by_rating(watch_ids):
        comparing = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.callproc('CompareByRates', [str(watch_ids)[1:-1], 14])
            comparing = cursor.fetchall()
        return comparing

    @staticmethod
    def stat_compare_by_sales(watch_ids):
        comparing = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.callproc('CompareBySales', [str(watch_ids)[1:-1], 14])
            comparing = cursor.fetchall()
        return comparing

    @staticmethod
    def stat_catalog_sales_info():
        top_sales = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor: 
            cursor.execute("SELECT * FROM test_cat_sales")
            top_sales = cursor.fetchall()
        return top_sales

    @staticmethod
    def stat_catalog_rating_info():
        top_rating = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM test_cat_rating")
            top_rating = cursor.fetchall()
        return top_rating
    
    @staticmethod
    def stat_cost_categ_info():
        cost_categs = []
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM test_watch_cost_categ")
            cost_categs = cursor.fetchall()
        return cost_categs
