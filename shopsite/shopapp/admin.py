from django.contrib import admin
from .models import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    # поля которые отображаются в админ панели
    list_display = ('id', 'title', 'description', 'size', 'price', 'count', 'discount', 'available', 'time_update', 'categ')
    # указываются поля при нажатии на которые происходи тпереход к записи
    list_display_links = ('id', 'title')
    # здесь указывается дополнительное поле для поиска по названию или описанию товара
    search_fields = ('title', 'description')
    # указываются поля которые можно менять в админ панели
    list_editable = ('available', 'price', 'discount', 'count')
    # поля по кторым можно фильтровать список товаров
    list_filter = ('price', 'time_update', 'categ', 'size')

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemPhoto)
admin.site.register(Category)