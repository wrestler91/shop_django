from django import forms
from .models import *
from django.contrib.auth.models import User
from multiupload.fields import MultiImageField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from captcha.fields import CaptchaField

class RequestItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categ'].empty_label = "Категория не выбрана"
        
    class Meta:
        model = RequestedItem
        fields = ['title', 'size', 'url', 'count', 'comments', 'photo',  'categ']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название бренда и модель'}),
            'comments': forms.Textarea(attrs={'cols': 60, 'rows': 10,}),
            'url': forms.TextInput(attrs={'size': 70, 'placeholder': 'Введите ссылку на товар'}),
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
        # print('from AddPhotoForm', self.request.FILES.getlist('photos'))
        # Остаются только картинки
    #     photos = [photo for photo in self.request.FILES.getlist('photos') if 'photo' in photo.content_type]
    #     # photos = [photo for photo in self.photos]
    #     # Если среди загруженных файлов картинок нет, то исключение
    #     if len(photos) == 0:
    #         raise forms.ValidationError(u'Not found uploaded photos')
    #     return photos

    # def save_for(self, photos, item):
    #     '''
    #     Метод сохраняет фотографии в модель ItemPhoto проходя по спику циклом.
    #     '''
    #     for photo in photos:
    #         file_type = magic.from_buffer(photo.read(), mime=True)
    #         if not file_type.startswith('image'):
    #             raise forms.ValidationError('Недопустимый тип файла. Пожалуйста, загрузите только изображения.')
    #     else:
    #         for photo in photos:
    #             ItemPhoto(photo=photo, item=item).save()

        # for photo in self.cleaned_data['photos']:
        #     ItemPhoto(photo=photo, item=item).save()

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2', 'email')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-input', 'label': 'Старый пароль'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-input', 'label': 'Новый пароль'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-input', 'label': 'Подтверждение пароля'})
