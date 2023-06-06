from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

# добавить адреса для представлений форм 
urlpatterns = [
    path('', Home.as_view(), name='home'), # соответсвует маршруту http://127.0.0.1:8000/
    path('item/<slug:item_slug>', ShowItem.as_view(), name='item'),
    # path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('category/<slug:categ_slug>/', cache_page(120)(Categories.as_view()), name ='category'),
    path('request/', RequestItem.as_view(), name='request'),
    path('additem/', AddItem.as_view(), name='add_item'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('password/', ChangePasswordView.as_view(), name='password'),
    path('about/', cache_page(6000)(AboutView.as_view()), name='about'),
]


