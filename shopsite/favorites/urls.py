from django.urls import path, include
from .views import *

app_name ='favorites'

urlpatterns = [ 
    path('favorites', include([
    path('<id>/add/', add_to_favorites, name = 'add'),
    path('<id>/remove/', remove_from_favorites, name='remove'),
    path('delete/', delete_favorites, name='delete'),
    ])),
    ]
# urlpatterns =  [
#     path('<id>/add/', add_to_favorites, name = 'add'),
#     path('<id>/remove/', remove_from_favorites, name='remove'),
#     path('delete/', delete_favorites, name='delete'),
#     ]
    