from django import forms
from django.forms.widgets import FileInput
from .models import *
from django.contrib.auth.models import User
from .utils import MultipleFileField
from multiupload.fields import MultiFileField, MultiImageField


class RequestItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categ'].empty_label = "Категория не выбрана"
        
    class Meta:
        model = RequestedItem
        fields = ['title', 'size', 'url', 'count', 'comments', 'photo',  'categ']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'comments': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }



# прописать форму добавления товара для администратора и работников.
# форма для товара
class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'size', 'price', 'count', 'discount', 'categ', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'comments': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

# форма для фото товара
class AddPhotoForm(forms.Form):
    # photos = MultipleFileField(label ='Фотографии')
    photos = MultiImageField(min_num=1, max_num=5, label ='Фотографии')

    # def __init__(self, *args, **kwargs):
    #     # print('From AddPhotoForm', 'kwargs:', kwargs, 'args:', args)
    #     if 'request' in kwargs:
    #         self.request = kwargs.pop('request')
    #     super(AddPhotoForm, self).__init__(*args, **kwargs)


    # def clean_photos(self):
    #     '''
    #     Выполняет валидацию поля.
    #     Извлекает из запроса self.request список файлов и берет только те эллементы которые являются изображениями.
    #     Затем проверяет есть ли в списке хоть 1 файл, если нет то вызывает исключение, а иначе возвращает список загруженных изображений 
    #     '''
    #     # print('from AddPhotoForm', self.request.FILES.getlist('photos'))
    #     # Остаются только картинки
    #     photos = [photo for photo in self.request.FILES.getlist('photos') if 'photo' in photo.content_type]
    #     # photos = [photo for photo in self.photos]
    #     # Если среди загруженных файлов картинок нет, то исключение
    #     if len(photos) == 0:
    #         raise forms.ValidationError(u'Not found uploaded photos')
    #     return photos

    def save_for(self, item):
        '''
        Метод сохраняет фотографии в модель ItemPhoto проходя по спику циклом.
        '''
        for photo in self.cleaned_data['photos']:
            ItemPhoto(photo=photo, item=item).save()

