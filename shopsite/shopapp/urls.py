from django.urls import path
from .views import *

# добавить адреса для представлений форм 
urlpatterns = [
    path('', Home.as_view(), name='home'), # соответсвует маршруту http://127.0.0.1:8000/women/
    path('item/<slug:item_slug>', ShowItem.as_view(), name='item'),
    path('category/<slug:categ_slug>/', Categories.as_view(), name ='category'),
    path('request/', RequestItem.as_view(), name='request'),
    path('additem/', AddItem.as_view(), name='add_item'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('logout/', login, name='logout'),
    path('register/', register, name='register'),
]


