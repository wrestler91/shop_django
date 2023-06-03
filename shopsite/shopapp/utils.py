from .models import *
from django.core.cache import cache
from django import forms

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]



class DataMixin:
    paginate_by = 5
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.all()
            cache.set('categories', categories, 60)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop()
 
        context['menu'] = user_menu
        context['categories'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
    

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
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
