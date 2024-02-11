from django import forms
from django.views.generic import FormView

from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.core.validators import *

from django.contrib.auth import authenticate
from django.core.validators import *
from decimal import Decimal
from .models import *


class UserCreationFormFixed(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormFixed, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class RegistrationFormView(FormView):
    form_class = UserCreationFormFixed
    template_name = "mainapp/register.html"
    success_url = "/login"

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

class AuthenticationFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'mainapp/login.html'
    success_url = '/afterloginredirect'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(AuthenticationFormView, self).form_valid(form)





class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[0-9A-Za-zА-Яа-яЁёІіЇїЄє]{1,45}$',
    'Логин состоит из букв латиницы, кириллицы или цифр')],
    label='Имя пользователя', 
    widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))

    email = forms.EmailField(max_length=45, required=True,
    label='Email-адрес', 
    widget=forms.TextInput(attrs={'placeholder': 'Введите email'}))

    password = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[A-Za-z0-9]{1,128}$', 
    'Пароль состоит из букв латиницы и цифр, его длинна не превышвает 128 символов')],
    label='Пароль', 
    widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class AuthenticationForm(forms.Form):
    login = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[0-9A-Za-zА-Яа-яЁёІіЇїЄє]{1,45}$',
    'Логин состоит из букв латиницы, кириллицы или цифр')],
    label='Имя пользователя', 
    widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))

    password = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[A-Za-z0-9]{1,128}$', 
    'Пароль состоит из букв латиницы и цифр, его длинна не превышвает 128 символов')],
    label='Пароль', 
    widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    def clean(self):
        username = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Указаные данные некорректны")
        return self.cleaned_data

        
class AddWatchForm(forms.Form):
    model_name = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[-_0-9A-Za-zА-Яа-яЁёІіЇїЄє]{1,45}$',
    'Название модели состоит из букв латиницы, кириллицы или цифр')],
    label='Название модели', 
    widget=forms.TextInput(attrs={'placeholder': 'Введите название модели'}))

    model_cost = forms.DecimalField(max_digits=8, decimal_places=2, required=True,
    validators=[MinValueValidator(1, 
    'Цена не может быть ниже 1'),
    MaxValueValidator(999999.99, 
    'Цена не может превышать 999999.99')],
    label='Стоимость модели')

    case_width = forms.DecimalField(max_digits=3, decimal_places=1, required=True,
    validators=[MinValueValidator(1, 
    'Ширина корпуса не может быть ниже 1'),
    MaxValueValidator(99.9, 
    'Ширина корпуса не может превышать 99.9')],
    label='Ширина корпуса')    

    case_height = forms.DecimalField(max_digits=3, decimal_places=1, required=True,
    validators=[MinValueValidator(1, 
    'Высота корпуса не может быть ниже 1'),
    MaxValueValidator(99.99, 
    'Высота корпуса не может превышать 99.9')],
    label='Высота корпуса')

    weight = forms.DecimalField(max_digits=4, decimal_places=2, required=True,
    validators=[MinValueValidator(1, 
    'Вес не может быть ниже 1'),
    MaxValueValidator(99.99, 
    'Вес не может превышать 999999.99')],
    label='Вес')

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label=None,
    label='Пол')

    waterproof_level = forms.IntegerField(max_value=300, min_value=0, required=True,
    validators=[MaxValueValidator(300, 
    'Уровень водонепроницаемости не может превышать 300')],
    label='Водонепроницаемость')

    #backlight = forms.BooleanField(label='Подсветка')

    current_amount = forms.IntegerField(max_value=1000, min_value=0, required=True,
    validators=[MaxValueValidator(1000, 
    'Кол-во не может превышать 1000')],
    label='Кол-во')

    mechanism_type = forms.ModelChoiceField(queryset=MechanismType.objects.all(), empty_label=None,
    label='Тип механизма')

    case_band = forms.ModelChoiceField(queryset=CaseBand.objects.all(), empty_label=None,
    label='Тип корпуса')

    glass_type = forms.ModelChoiceField(queryset=GlassType.objects.all(), empty_label=None,
    label='Тип стекла')

    strap_type = forms.ModelChoiceField(queryset=StrapType.objects.all(), empty_label=None,
    label='Тип браслета')

    indication_type = forms.ModelChoiceField(queryset=IndicationType.objects.all(), empty_label=None,
    label='Тип индикации')

    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label=None,
    label='Бренд')

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None,
    label='Категория')

    model_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите название модели'}), 
    required=True,
    validators=[RegexValidator(r'^[ .,A-Za-zА-Яа-яЁёІіЇїЄє]*$',
    'Описание состоит из букв латиницы или кириллицы')],
    label='Описание модели')

    image = forms.ImageField(
        required=False,
        label='Изображение'
        )

    model_features = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(), required=False)


class ProfileForm(forms.Form):
    login = forms.CharField(max_length=45, required=True,
    label='Имя пользователя', 
    widget=forms.TextInput(attrs={'readonly' : True}))

    email = forms.CharField(max_length=45, required=True,
    label='Email', 
    widget=forms.TextInput(attrs={'placeholder': 'Не указан', 'readonly' : True}))

    first_name = forms.CharField(max_length=45, required=True,
    label='Имя', 
    widget=forms.TextInput(attrs={'placeholder': 'Не указано', 'readonly' : True}))

    last_name = forms.CharField(max_length=45, required=True,
    label='Фамилия', 
    widget=forms.TextInput(attrs={'placeholder': 'Не указано', 'readonly' : True}))


class ChangePasswordForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : True}))

    old_password = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[A-Za-z0-9]{1,128}$', 
    'Пароль состоит из букв латиницы и цифр, его длинна не превышвает 128 символов')],
    label='Текущий пароль', 
    widget=forms.PasswordInput(attrs={'placeholder': 'Введите текущий пароль'}))

    new_password = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[A-Za-z0-9]{1,128}$', 
    'Пароль состоит из букв латиницы и цифр, его длинна не превышвает 128 символов')],
    label='Новый пароль', 
    widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))

    def clean(self):
        print(self.cleaned_data.get('user_id'))
        print(self.cleaned_data.get('old_password'))
        old_password = self.cleaned_data.get('old_password')
        if(not User.objects.get(id=self.cleaned_data.get('user_id')).check_password(old_password)):
            raise forms.ValidationError("Указан неверный пароль")
        return self.cleaned_data


class MakeOrderForm(forms.Form):
    contact_name = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^[A-Za-zА-Яа-яЁёІіЇїЄє]{1,45}$',
    'Контактное имя состоит из букв латиницы или кириллицы')],
    label='Контактное имя',
    widget=forms.TextInput(attrs={'placeholder': 'Введите контактное имя'}))

    contact_number = forms.CharField(max_length=45, required=True, 
    validators=[RegexValidator(r'^380[0-9]{9}$', 
    'Контактный телефон состоит из цифр и начинается с 380')],
    label='Контактный телефон',
    widget=forms.TextInput(attrs={'placeholder': 'Введите контактный номер'}))

    order_address = forms.CharField(max_length=45, required=True,
    validators=[RegexValidator(r'^[ .,0-9A-Za-zА-Яа-яЁёІіЇїЄє]{1,255}$',
    'Адрес не может превышать 255 симолов')],
    label='Адрес доставки',
    widget=forms.TextInput(attrs={'placeholder': 'Введите адрес доставки'}))

    locality = forms.ModelChoiceField(queryset=Locality.objects.all(), 
    required=True,
    empty_label=None,
    label='Населенный пункт')

    payment_type = forms.ModelChoiceField(queryset=PaymentType.objects.all(), 
    required=True,
    empty_label=None,
    label='Тип оплаты')

    addit_wishes = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите примечания'}), 
    required=True,
    validators=[RegexValidator(r'^[ .,A-Za-zА-Яа-яЁёІіЇїЄє]*$',
    'Примечания состоят из букв латиницы или кириллицы')],
    label='Примечания')


class ChangeOrderForm(MakeOrderForm):
    order_state = forms.ModelChoiceField(queryset=OrderState.objects.all().exclude(order_state_name='Корзина'), 
    empty_label=None,
    label='Статус заказа')

    def pass_perm(self, user):
        if(not user.is_authenticated or not user.is_staff):
            for field in self.fields.keys():
                self.fields[field].widget.attrs['disabled'] = 'disabled'

    # def __init__(self, for_read=False, *args, **kwargs):
    #     super(ChangeOrderForm, self).__init__(*args, **kwargs)
    #     if(for_read == True):
    #         for field in self.fields.keys():
    #             self.fields[field].widget.attrs['disabled'] = 'disabled'


class CartItemForm(forms.Form):
    quantity = forms.IntegerField(max_value=1000, min_value=0, required=True,
    validators=[MaxValueValidator(1000, 
    'Кол-во не может превышать 1000')],
    label='')


class RateForm(forms.Form):
    value = forms.IntegerField(max_value=10, min_value=0, required=True,
    validators=[MaxValueValidator(10, 
    'Оценка не может превышать 5.0')],
    label='')







# class AddWatchForm(forms.Form):
#     model_name = forms.CharField(max_length=45, required=True, 
#     validators=[RegexValidator(r'^[-_0-9A-Za-zА-Яа-яЁёІіЇїЄє]{1,45}$',
#     'Название модели состоит из букв латиницы, кириллицы или цифр')],
#     label='Название модели', 
#     widget=forms.TextInput(attrs={'placeholder': 'Введите название модели'}))

#     model_cost = forms.DecimalField(max_digits=8, decimal_places=2, required=True,
#     validators=[MinValueValidator(1, 
#     'Цена не может быть ниже 1'),
#     MaxValueValidator(999999.99, 
#     'Цена не может превышать 999999.99')],
#     label='Стоимость модели')

#     case_width = forms.DecimalField(max_digits=3, decimal_places=1, required=True,
#     validators=[MinValueValidator(1, 
#     'Ширина корпуса не может быть ниже 1'),
#     MaxValueValidator(99.9, 
#     'Ширина корпуса не может превышать 99.9')],
#     label='Ширина корпуса')    

#     case_height = forms.DecimalField(max_digits=3, decimal_places=1, required=True,
#     validators=[MinValueValidator(1, 
#     'Высота корпуса не может быть ниже 1'),
#     MaxValueValidator(99.99, 
#     'Высота корпуса не может превышать 99.9')],
#     label='Высота корпуса')

#     weight = forms.DecimalField(max_digits=4, decimal_places=2, required=True,
#     validators=[MinValueValidator(1, 
#     'Вес не может быть ниже 1'),
#     MaxValueValidator(99.99, 
#     'Вес не может превышать 999999.99')],
#     label='Вес')

#     gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label=None,
#     label='Пол')

#     waterproof_level = forms.IntegerField(max_value=300, min_value=0, required=True,
#     validators=[MaxValueValidator(300, 
#     'Уровень водонепроницаемости не может превышать 300')],
#     label='Водонепроницаемость')

#     #backlight = forms.BooleanField(label='Подсветка')

#     current_amount = forms.IntegerField(max_value=1000, min_value=0, required=True,
#     validators=[MaxValueValidator(1000, 
#     'Кол-во не может превышать 1000')],
#     label='Кол-во')

#     mechanism_type = forms.ModelChoiceField(queryset=MechanismType.objects.all(), empty_label=None,
#     label='Тип механизма')

#     case_band = forms.ModelChoiceField(queryset=CaseBand.objects.all(), empty_label=None,
#     label='Тип корпуса')

#     glass_type = forms.ModelChoiceField(queryset=GlassType.objects.all(), empty_label=None,
#     label='Тип стекла')

#     strap_type = forms.ModelChoiceField(queryset=StrapType.objects.all(), empty_label=None,
#     label='Тип браслета')

#     indication_type = forms.ModelChoiceField(queryset=IndicationType.objects.all(), empty_label=None,
#     label='Тип индикации')

#     brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label=None,
#     label='Бренд')

#     category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None,
#     label='Категория')

#     model_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите название модели'}), 
#     required=True,
#     validators=[RegexValidator(r'^[ ,A-Za-zА-Яа-яЁёІіЇїЄє]*$',
#     'Описание состоит из букв латиницы или кириллицы')],
#     label='Описание модели')

#     image = forms.ImageField(
#         required=False,
#         label='Изображение'
#         )

#     model_features = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(), required=False)