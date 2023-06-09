from .models import *
from django.core.cache import cache
from django import forms
import requests



menu = [{'title': "О сайте", 'url_name': 'about'},
        # {'title': "Обратная связь", 'url_name': 'contact'},
        ]
API_NASDAQ = '_RQPjdq7WzFumRdf1Tjw'

# def get_currency_rate(api_key):
#     '''
#     Функция получающая текущий курс рубля по api
#     '''
#     url = 'https://api.nasdaq.com/api/forex/rates'
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#     }
#     params = {
#         'base': 'USD',
#         'symbol': 'RUB',
#     }
#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         rate = data['data']['lastSalePrice']
#         return rate
#     else:
#         return None


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



