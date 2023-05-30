from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from datetime import datetime, timedelta
from .utils import *
from .form import *


# Create your views here.
# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
# ]


class Home(DataMixin, ListView):
    model = Item
    template_name = 'shop/home.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return {**cont, **c_def}
    
    def get_queryset(self):
        # здесь прописать фильтр который будет выводит  товары добавленные за последний месяц
        last_month = datetime.now() - timedelta(days=30)
        # return Item.objects.filter(time_update__gte=last_month).select_related('categ')
        return Item.objects.all()

class Categories(DataMixin, ListView):
    model = Item
    template_name = 'shop/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['categ_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return {**cont, **c_def}
    
    def get_queryset(self):
        return Item.objects.filter(categ__slug=self.kwargs['categ_slug'])

class ShowItem(DataMixin, DetailView):
    model = Item
    template_name = 'shop/item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=cont['item'])
        return {**cont, **c_def}

    def get_queryset(self):
        return Item.objects.get(categ__slug=self.kwargs['categ_slug'])

# представление формы для запроса пользователем некоторого товара
# доработать представление 
class RequestItem(LoginRequiredMixin, DataMixin, CreateView):
    form_class = RequestItemForm
    template_name = 'shop/request.html'
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Запрос товара')
        context = dict(list(cont.items()) + list(c_def.items()))
        return context
    

def about(request):
    return HttpResponse('<h1>about</h1>')

def contact(request):
    return HttpResponse('<h1>contact</h1>')

def login(request):
    return HttpResponse('<h1>login</h1>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
