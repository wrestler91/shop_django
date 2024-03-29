from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.contrib.auth import login, logout
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

from .models import *
from .utils import ItemAPIListPagination, DataMixin, menu
from .form import *

from rest_framework import viewsets
from .serializers import *
from .permissions import IsAdminOrReadOnly




class Home(DataMixin, ListView):
    '''
    Главная страница. 
    Отображает список последних поступлений 
    '''
    model = Item
    template_name = 'shop/index.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return {**cont, **c_def}
    
    def get_queryset(self):
        # фильтр который выводит товары добавленные за последний месяц
        last_month = datetime.now() - timedelta(days=30)
        return Item.objects.filter(time_update__gte=last_month).prefetch_related('photos').select_related('categ')
        

class Categories(DataMixin, ListView):
    '''
    Выводит список товаров по категориям.
    '''
    model = Item
    template_name = 'shop/categories.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['categ_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return {**cont, **c_def}
    
    def get_queryset(self):
        return Item.objects.filter(categ__slug=self.kwargs['categ_slug']).prefetch_related('photos', 'photos__item').select_related('categ')
        
        # ниже была попытка оптимизировать запросы, чтобы получить первые фото товаров сразу, а не в цикле шаблона.
        # item_ids = Item.objects.filter(categ__slug=self.kwargs['categ_slug']).values_list('id', flat=True)
        # item_photos_subquery = ItemPhoto.objects.filter(item_id__in=item_ids).order_by('item_id', 'id').values('item_id', 'photo')
        # subquery_dict = {}
        # for item_id, photo in item_photos_subquery:
        #     if item_id not in subquery_dict:
        #         subquery_dict[item_id] = photo
        # queryset = Item.objects.filter(categ__slug=self.kwargs['categ_slug']).annotate(first_photo=Subquery(subquery_dict.values(), output_field=models.ImageField()))
        # return queryset
    
class ShowItem(DataMixin, DetailView):
    '''
    Детальное представление товара
    '''
    model = Item
    template_name = 'shop/item.html'
    context_object_name = 'item'
    slug_url_kwarg = 'item_slug'

    
    def get_context_data(self, **kwargs) -> dict:
        '''
        Переопределяем контекст, для добавления в него элементов для главного и бокового меню из класса DataMixin
        А так же добавляем вычисляемое значение price_with_discount 
        '''
        cont = super().get_context_data(**kwargs)
        # в контектс добавляем вычисляеое значение цены со скидкой
        item = cont['item']
        item.price_with_discount = item.price - (item.price * (item.discount/100))
        cont['price_with_discount'] = item.price_with_discount

        # проверка, добавлен ли продукт в избранное для вывода нужной кнопки меню
        is_notfavorite = {'id': str(item.id)} not in self.request.session.get('favorites', [])
        # print('session:', self.request.session.get('favorites', []))
        # print('is_notfavorite:', is_notfavorite)
        
        cont['is_notfavorite'] = is_notfavorite
        c_def = self.get_user_context(title=cont['item'])
        return {**cont, **c_def}

   

# представление формы для запроса пользователем некоторого товара
# доработать представление 
class RequestItem(LoginRequiredMixin, DataMixin, CreateView):
    '''
    Представление формы для запроса товара обычным пользователем. 
    Связан с отдельной моделью
    '''
    form_class = RequestItemForm
    template_name = 'shop/request.html'
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Запрос товара')
        return {**cont, **c_def}

class AddItem(DataMixin, CreateView):
    '''
    Представления формы для добавления товара на сайт пользователем с правами администратора или работника
    '''
    template_name = 'shop/additem.html'
    form_class = AddItemForm
    form_photos_class = AddPhotoForm
    model = Item
    raise_exception = True

    # def get(self, request):
    #     '''
    #     переопределяем метод гет для передачи двух форм в контекст
    #     '''
    #     form = self.form_class()
    #     form_photos = self.form_photos_class()
    #     return render(request, self.template_name, {'form': form, 'form_photos': form_photos})
    
    def post(self, request):
        '''
        Переопределяем метод пост для сохранения полученных данных в соответсвующие ДБ
        '''
        form = self.form_class(request.POST)
        form_photos = self.form_photos_class(request.POST, request.FILES)
        # if form.is_valid() and form_photos.is_valid():
        if form.is_valid():
            item = form.save()
            for photo in self.request.FILES.getlist('photos'):
                ItemPhoto(photo=photo, item=item).save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form, 'form_photos': form_photos})

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление товара')
        cont['form'] = self.form_class
        cont['form_photos'] = self.form_photos_class
        return {**cont, **c_def}

class RegisterUser(DataMixin, CreateView):
    '''
    Представление формы регистрации пользователя
    '''
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return {**context, **c_def}
    
    def form_valid(self, form):
        '''
        Он отрабатывает при успешной проверки формы регистрации, а значит, при успешной регистрации. 
        Здесь мы самостоятельно сохраняем форму (добавляем пользователя в БД), 
        а затем, вызываем стандартную функцию фреймворка Django login для авторизации пользователя. 
        После этого, делаем перенаправление на главную страницу.
        '''
        user = form.save()
        login(self.request, user)
        return redirect('home')
    

class LoginUser(DataMixin, LoginView):
    '''
    Представление формы авторизации пользователя
    '''
    form_class = LoginUserForm
    template_name = 'shop/login.html'
 
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')

class ProfileEditView(DataMixin, LoginRequiredMixin, UpdateView):
    '''
    Представление отображает форму для изменения данных пользователя
    '''
    model = User
    form_class = ProfileEditForm
    template_name = 'shop/edit_profile.html'
    
    change_password = {'title': "Изменение пароля", 'url_name': 'password'}
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование профиля")
        context['change_password'] = self.change_password
        return {**context, **c_def}
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('profile')



def logout_user(request):
    '''
    Представлени для разлогирования пользователя на основе базовой функции джанго
    '''
    logout(request)
    return redirect('login')



class ProfileView(DataMixin, LoginRequiredMixin, DetailView):
    '''
    Отображает профиль пользователя
    '''
    model = User
    template_name = 'shop/profile.html'
    context_object_name = 'profile'
    edit = {'title': "Редактирование профиля", 'url_name': 'edit_profile'}

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Просмотр профиля')
        cont['edit'] = self.edit
        return {**cont, **c_def}
    
    
    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(DataMixin, LoginRequiredMixin, PasswordChangeView):
    '''
    Для формы изменения пароля
    '''
    form_class = ChangePasswordForm
    success_url = reverse_lazy('profile')
    template_name = 'shop/password.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Изменение пароля")
        return {**context, **c_def}



class AboutView(TemplateView):
    '''
    Страничка о нас.
    '''
    template_name = 'shop/about.html'
    
    menu = [
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_menu = menu.copy()
        context['menu'] = user_menu
        context['title'] = 'О нас'
        return context

class FavoriteLiist(DataMixin, ListView):
    '''
    Выводит список товаров добавленных в избранное.
    Список реализован через Сессию и отдельное приложение
    '''
    model = Item
    template_name = 'shop/favorite_list.html'
    context_object_name = 'favor_list'

    def get(self, request, *args, **kwargs):
        # Получение значения из сессии
        self.favorites = request.session.get('favorites', [])
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Избранные товары")
        return {**cont, **c_def}

    def get_queryset(self):
        '''
        получаем список избранного по id товара
        '''
        ids = [item['id'] for item in self.favorites]
        items = Item.objects.filter(id__in=ids)
        return items

def contact(request):
    '''
    Представление контактов. Будет дорабатываться. Планирую прикрутить туда ссылку на телеграмм бот. 
    Возможно сделаю форму обратной связи с привязкой к почте
    '''
    return HttpResponse('<h1>contact</h1>')



def pageNotFound(request, exception):
    '''
    функция для обработки исключения отсутсвия страницы"
    '''
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')




################################################# API VIEWS #################################################

class ItemAPIViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = ItemAPIListPagination



class RequestedItemApiViewSet(viewsets.ModelViewSet):
    queryset = RequestedItem.objects.all().order_by('time_update')
    serializer_class = RequestedItemSerializer
    pagination_class = ItemAPIListPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return RequestedItem.objects.filter(user=self.request.user).order_by('time_update')
        else:
            return RequestedItem.objects.none()