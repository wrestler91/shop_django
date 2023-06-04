from django.db import models
from django.core import validators
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
# добавить функционал обавления товара в избранное
class Item(models.Model):
    title = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    size = models.CharField(max_length=50, verbose_name='Размер')
    price = models.FloatField(validators = [validators.MinValueValidator(0)], default=0, verbose_name='Цена')
    count = models.IntegerField(validators = [validators.MinValueValidator(0)], default=1, verbose_name='Количество')
    discount = models.FloatField(validators= [validators.MinValueValidator(0)], default=0, verbose_name='Скидка')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    categ = models.ForeignKey('Category', on_delete=models.DO_NOTHING, verbose_name='Категория', related_name='categ')
    

    

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('item', kwargs={'item_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'categ_slug': self.slug})

# необходимо создать связь этого представления и товара
# в шаблонах поменять ссылку на фото (сейчас там ссылка на атрибут класса Item)
class ItemPhoto(models.Model):
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    # photo2 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото 2')
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, verbose_name='Товар', related_name='photos')
    # related_name='photos' используется для обращения к этому полю через класс Item (for photo in item.photos)
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
        
    def __str__(self):
        return self.item.title
    
    def get_absolute_url(self):
        return reverse('photo', kwargs={'photo_pk': self.pk})

# представление для формы запроса товара
# необходимо привязать форму к пользователю
class RequestedItem(models.Model):
    title = models.CharField(max_length=300, verbose_name='Наименование')
    comments = models.TextField(verbose_name='Комментарии', blank=True)
    size = models.CharField(max_length=50, verbose_name='Размер')
    count = models.IntegerField(validators = [validators.MinValueValidator(0)], default=1, verbose_name='Количество')
    url = models.URLField(blank=True, verbose_name='Ссылка')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время создания заявки')
    categ = models.ForeignKey('Category', on_delete=models.DO_NOTHING, verbose_name='Категория')
    photo = models.ImageField(upload_to="photos_requested/%Y/%m/%d/", verbose_name='Фото', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('request', kwargs={'user_pk': self.pk})



