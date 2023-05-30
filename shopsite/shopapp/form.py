from django import forms
from .models import *
from django.contrib.auth.models import User

# дорабоать форму
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
