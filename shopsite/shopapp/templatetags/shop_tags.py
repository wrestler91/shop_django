from django import template
from shopapp.models import *

register = template.Library()

def get_categories():
    return Category.objects.all()

@register.inclusion_tag('shop/include_tags/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"categories": cats, "cat_selected": cat_selected}

@register.inclusion_tag('shop/include_tags/list_menu.html')
def show_menu():
    menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
       
        ]
    return {'menu': menu,}