# Generated by Django 4.2.1 on 2023-05-29 17:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('size', models.CharField(max_length=50, verbose_name='Размер')),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('count', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
                ('discount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Скидка')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('categ', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shopapp.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='RequestedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Наименование')),
                ('comments', models.TextField(blank=True, verbose_name='Комментарии')),
                ('size', models.CharField(max_length=50, verbose_name='Размер')),
                ('count', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
                ('url', models.URLField(blank=True, verbose_name='Ссылка')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время создания заявки')),
                ('photo', models.ImageField(blank=True, upload_to='photos_requested/%Y/%m/%d/', verbose_name='Фото')),
                ('categ', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shopapp.category', verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='ItemPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shopapp.item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фотографии',
            },
        ),
    ]
