from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.contrib.auth import login, logout
from .models import *
from datetime import datetime, timedelta
from .utils import *
from .form import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

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
        return Item.objects.filter(time_update__gte=last_month).select_related('categ')
        

class Categories(DataMixin, ListView):
    model = Item
    template_name = 'shop/categories.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['categ_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return {**cont, **c_def}
    
    def get_queryset(self):
        return Item.objects.filter(categ__slug=self.kwargs['categ_slug']).select_related('categ')
        


class ShowItem(DataMixin, DetailView):
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
        item = cont['item']
        item.price_with_discount = item.price - (item.price * (item.discount/100))
        cont['price_with_discount'] = item.price_with_discount
        c_def = self.get_user_context(title=cont['item'])
        return {**cont, **c_def}

   

# представление формы для запроса пользователем некоторого товара
# доработать представление 
class RequestItem(LoginRequiredMixin, DataMixin, CreateView):
    form_class = RequestItemForm
    template_name = 'shop/request.html'
    raise_exception = True

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Запрос товара')
        return {**cont, **c_def}

class AddItem(DataMixin, CreateView):
    template_name = 'shop/additem.html'
    form_class = AddItemForm
    form_photos_class = AddPhotoForm
    model = Item
    raise_exception = True
    # success_url = reverse_lazy('home')

    def get(self, request):
        form = self.form_class()
        form_photos = self.form_photos_class()
        return render(request, self.template_name, {'form': form, 'form_photos': form_photos})
    
    def post(self, request):
    
        # print('From AddItem (view)', request.FILES)
        form = self.form_class(request.POST)
        # form_photos = self.form_photos_class(request.POST, request.FILES, request=request)
        form_photos = self.form_photos_class(request.POST, request.FILES)
        # if form.is_valid() and form_photos.is_valid():
        if form.is_valid():
            
            # form.save()
            # form_photos.save()
            item = form.save()
            # form_photos.save_for(item)
            for photo in self.request.FILES.getlist('photos'):
                ItemPhoto(photo=photo, item=item).save()
            # form_photos.save_for(photos=self.request.FILES.getlist('photos'), item=item)
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form, 'form_photos': form_photos})

    def get_context_data(self, **kwargs) -> dict:
        cont = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление товара')
        return {**cont, **c_def}

class RegisterUser(DataMixin, CreateView):
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

def contact(request):
    return HttpResponse('<h1>contact</h1>')



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
