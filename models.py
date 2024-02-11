# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    supercategory = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    category_name = models.CharField(unique=True, max_length=20)
    category_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'category'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Meal(models.Model):
    meal_name = models.CharField(max_length=20)
    meal_description = models.TextField()
    id = models.DecimalField(primary_key=True, max_digits=18, decimal_places=0)
    meal_cost = models.DecimalField(max_digits=18, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'meal'


class Mealhascategory(models.Model):
    category = models.OneToOneField(Category, models.DO_NOTHING, primary_key=True)
    meal = models.ForeignKey(Meal, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mealhascategory'
        unique_together = (('category', 'meal'),)


class Orderhasmeal(models.Model):
    order = models.OneToOneField('Orders', models.DO_NOTHING, primary_key=True)
    amount = models.IntegerField()
    preference = models.TextField()
    order_datetime = models.DateField()
    meal = models.ForeignKey(Meal, models.DO_NOTHING)
    cost = models.DecimalField(max_digits=18, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'orderhasmeal'
        unique_together = (('order', 'meal'),)


class Orders(models.Model):
    id = models.IntegerField(primary_key=True)
    reservation = models.ForeignKey('Reservation', models.DO_NOTHING)
    status = models.ForeignKey('Orderstatus', models.DO_NOTHING)
    addit_preferences = models.TextField()

    class Meta:
        managed = False
        db_table = 'orders'


class Orderstatus(models.Model):
    id = models.IntegerField(primary_key=True)
    order_status_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'orderstatus'


class Reservation(models.Model):
    table = models.ForeignKey('Tabless', models.DO_NOTHING)
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey('Users', models.DO_NOTHING)
    status = models.ForeignKey('Reservationstatus', models.DO_NOTHING)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    addit_wishes = models.TextField()
    reservation_datetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'reservation'


class Reservationstatus(models.Model):
    id = models.IntegerField(primary_key=True)
    reservation_status_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'reservationstatus'


class Roles(models.Model):
    id = models.IntegerField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'roles'


class Tabless(models.Model):
    id = models.IntegerField(primary_key=True)
    table_name = models.CharField(max_length=20)
    max_client_capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tabless'


class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    user_name = models.CharField(max_length=20)
    user_sername = models.CharField(max_length=20)
    user_login = models.CharField(unique=True, max_length=20)
    user_password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
