from .models import *
from django.core.cache import cache
from django import forms
import requests
import json
import time
from functools import wraps


menu = [{'title': "О сайте", 'url_name': 'about'},
        # {'title': "Обратная связь", 'url_name': 'contact'},
        ]


def time_delay(func):
    '''
    Декоратор. Позволяет вызывать функцию не чаще 1 раз в 6 часов
    При первом вызове заносит данные в кеш.
    Если функция вызывается чаще установленного ограничения, то значения берет из кеша
    иначе переписывает содержимое кеша 
    '''
    hours = 6
    last_call = None
    cache = []
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal last_call
        curent_time = time.time()

        if not last_call or curent_time - last_call >= hours * 3600:
            last_call = curent_time
            usd, eur = func(*args, **kwargs)
            cache.clear()
            cache.append(usd)
            cache.append(eur)

        return cache
    
    return wrapper 



@time_delay
def get_currency():
    '''
    Получаем курс валют при помощи API ЦБ РФ
    функция обернута в декоратор блокирующий вызов функции чаще чем 1 раз в 6 часов
    '''
    URL_CB_VALUTE = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(URL_CB_VALUTE)
    usd = eur = None
    if response.status_code == 200:
        data = json.loads(response.text)
        usd = data['Valute']['USD']['Value']
        eur = data['Valute']['EUR']['Value']
    return round(usd, 2), round(eur, 2)


def get_currency_cacher(func):
    cache = []
    if not cache:
        usd, eur = func()
        cache.append(usd)
        cache.append(eur)
        return cache
    else:
        print('before try:', cache)
        try:
            usd, eur = func()
            cache.clear()
            cache.append(usd)
            cache.append(eur)
        except Exception:
            pass
        finally:
            print('after try:', cache)
            return cache


class DataMixin:
    '''
    Миксин для представлений.
    Добавляет в контекст главное и боковое меню сайта
    '''
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.all()
            cache.set('categories', categories, 1)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop()
    
        context['menu'] = user_menu
        context['categories'] = categories

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        usd, eur = get_currency()
        context['usd'], context['eur'] = usd, eur

        return context
    

class MultipleFileInput(forms.ClearableFileInput):
    '''
    Класс для реализации добавления нескольких фото одним полем. На данный момент не используется
    '''
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    '''
    Класс для реализации добавления нескольких фото одним полем. На данный момент не используется
    '''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        print('from MultipleFileField', data)
        '''
        метод валидизирует данные. 
        Если пользователь загружает несколько файлов, то циклом проходимся по ним и для каждого файла вызываем базовый метод
        single_file_clean который отсеивает не подходящие файлы.
        Если же загружен 1 файл то этот метод вызывается только для него
        возвращает список очищенных данных
        '''
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



