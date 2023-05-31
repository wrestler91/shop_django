from django import forms
from django.forms.widgets import FileInput
from .models import *
from django.contrib.auth.models import User

# дорабоать форму
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        '''
        метод валидизирует данные. 
        Если пользователь загружает несколько файлов, то циклом проходимся по ним и для каждого файла вызываем базовый метод
        single_file_clean который отсеивает не подходящие файлы.
        Если же загружен 1 файл то этот метод вызывается только для него
        возвращает список очищенных данных
        '''
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
    photos = MultipleFileField(label ='Фотографии')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(AddPhotoForm, self).__init__(*args, **kwargs)

    
    def clean_photos(self):
        '''
        Выполняет валидацию поля.
        Извлекает из запроса self.request список файлов и берет только те эллементы которые являются изображениями.
        Затем проверяет есть ли в списке хоть 1 файл, если нет то вызывает исключение, а иначе возвращает список загруженных изображений 
        '''
        # Остаются только картинки
        photos = [photo for photo in self.request.FILES.getlist('photos') if 'photo' in photo.content_type]
        # Если среди загруженных файлов картинок нет, то исключение
        if len(photos) == 0:
            raise forms.ValidationError(u'Not found uploaded photos.')
        return photos

    def save_for(self, item):
        '''
        Метод сохраняет фотографии в модель ItemPhoto проходя по спику циклом.
        '''
        for photo in self.cleaned_data['photos']:
            ItemPhoto(photo=photo, item=item).save()

 