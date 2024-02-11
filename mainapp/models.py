from django.db import models
from django.contrib.auth.models import * 
from django.db.models.fields.related import ForeignKey


from django.db.models.constraints import *
import datetime


# Create your models here.
class MechanismType(models.Model):
    class Meta:
        db_table = 'mechanism_type'
    
    mechanism_name = models.CharField(max_length=40, null=False)
    def __str__(self):
        return self.mechanism_name


class CaseBand(models.Model):
    class Meta:
        db_table = 'case_band'
    
    case_type_name = models.CharField(max_length=55, null=False)
    def __str__(self):
        return self.case_type_name


class GlassType(models.Model):
    class Meta:
        db_table = 'glass_type'
    
    glass_type_name = models.CharField(max_length=20, null=False)
    def __str__(self):
        return self.glass_type_name


class StrapType(models.Model):
    class Meta:
        db_table = 'strap_type'
    
    strap_type_name = models.CharField(max_length=55, null=False)
    def __str__(self):
        return self.strap_type_name


class IndicationType(models.Model):
    class Meta:
        db_table = 'indication_type'
    
    indication_type_name = models.CharField(max_length=65, null=False)
    def __str__(self):
        return self.indication_type_name


class Brand(models.Model):
    class Meta:
        db_table = 'brand'

    brand_name = models.CharField(max_length=45, null=False)
    manufacturer_country = models.CharField(max_length=45, null=False)

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    class Meta:
        db_table = 'category'

    category_name = models.CharField(max_length=40, null=False)

    def __str__(self):
        return self.category_name





class Gender(models.Model):
    class Meta:
        db_table = 'gender'

    gender_name = models.CharField(max_length=8, null=False)

    def __str__(self):
        return self.gender_name


class Feature(models.Model):
    class Meta:
        db_table = 'feature'

    feature_name = models.CharField(max_length=75, null=False)

    def __str__(self):
        return self.feature_name


class Watch(models.Model):
    class Meta:
        db_table = 'watch'
    
    # class Gender(models.TextChoices):
    #     MALE = 'M', 'Male'
    #     FEMALE = 'F', 'Female'

    model_name = models.CharField(max_length=45, null=False)
    model_description = models.TextField(null=False, blank=False)
    model_cost = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    case_width = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    case_height = models.DecimalField(max_digits=3, decimal_places=1, null=False)
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=False)
    #backlight = models.BooleanField(default=False, null=False)
    waterproof_level = models.IntegerField(default=0, null=True, blank=True)
    # gender = models.CharField(
    #     max_length=2,
    #     choices=Gender.choices,
    #     default=Gender.MALE,
    #     null=False
    # )
    gender = models.ForeignKey(Gender, models.RESTRICT, null=False, default=1)
    current_amount = models.PositiveIntegerField(default=0, null=False)
    
    mechanism_type = models.ForeignKey(MechanismType, models.RESTRICT, null=False)
    case_band = models.ForeignKey(CaseBand, models.RESTRICT, null=False)
    glass_type = models.ForeignKey(GlassType, models.RESTRICT, null=False)
    strap_type = models.ForeignKey(StrapType, models.RESTRICT, null=False)
    indication_type = models.ForeignKey(IndicationType, models.RESTRICT, null=False)
    brand = models.ForeignKey(Brand, models.RESTRICT, null=False)
    category = models.ForeignKey(Category, models.RESTRICT, null=False)
    image = models.ImageField(null=True, blank=True, default='images/default_watch.jpg', upload_to='images/')
    add_date = models.DateField(null=False, blank=False, default=datetime.date.today())
    #feature_list = models.ManyToManyField(Feature, through='WatchHasFeature')

    @property
    def features(self):
        features_set = Feature.objects.filter(watchhasfeature__watch=self)
        return features_set

    def split_features_list(self):
        if self.features_list == None:
            return None
        return self.features_list.split('\n')

    @property
    def is_new(self):
        print('date1', self.add_date, type(self.add_date))
        print('date2', datetime.date.today(), type(datetime.date.today()))
        return (datetime.date.today() - self.add_date).days <= 14



class WatchHasFeature(models.Model):
    class Meta:
        db_table = 'watch_has_feature'
        unique_together=['watch', 'feature']

    watch = models.ForeignKey(Watch, models.CASCADE, null=False)
    feature = models.ForeignKey(Feature, models.RESTRICT, null=False)





class Rate(models.Model):
    class Meta:
        db_table = 'rate'
        unique_together=['watch', 'user']

    value = models.DecimalField(default=0, max_digits=2, decimal_places=1, null=False)
    watch = models.ForeignKey(Watch, models.CASCADE, null=False)
    user = models.ForeignKey(User, models.RESTRICT, null=True)
    date = models.DateField(null=True, blank=True, default=datetime.date.today())



class Locality(models.Model):
    class Meta:
        db_table = 'locality'

    locality_name = models.CharField(max_length=75, null=False)

    def __str__(self):
        return self.locality_name

class PaymentType(models.Model):
    class Meta:
        db_table = 'payment_type'

    payment_type_name = models.CharField(max_length=12, null=False)

    def __str__(self):
        return self.payment_type_name

class OrderState(models.Model):
    class Meta:
        db_table = 'order_state'

    order_state_name = models.CharField(max_length=35, null=False)
        
    def __str__(self):
        return self.order_state_name


class Order(models.Model):
    class Meta:
        db_table = 'order'

    order_date = models.DateField(null=True, blank=True)
    contact_name = models.CharField(max_length=45, null=True, blank=True)
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    addit_wishes = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, models.RESTRICT, null=False)
    order_state = models.ForeignKey(OrderState, models.RESTRICT, null=False)
    order_address = models.CharField(max_length=80, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, models.RESTRICT, null=False, default=1)
    locality = models.ForeignKey(Locality, models.RESTRICT, null=False, default=1)

    @property
    def products(self):
        ohp_set = OrderHasProduct.objects.filter(order_id__id=self.id)
        return ohp_set

    def split_watches_list(self):
        return self.watches_list.split('\n')




class OrderHasProduct(models.Model):
    class Meta:
        db_table = 'order_has_product'
        unique_together=['order', 'product']

    quantity = models.PositiveIntegerField(default=1, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Watch, on_delete=models.RESTRICT, null=False)
    noted_cost = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=False)