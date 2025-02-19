from django import forms

from . import BaseModelForm
from ..models import Passport


class PassportForm(BaseModelForm):
    class Meta:
        model = Passport
        fields = ('seria', 'number', 'date', 'whom', 'address_registration', 'address_actual')
        widgets = {
            'seria': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'whom': forms.TextInput(attrs={'class': 'form-control'}),
            'address_registration': forms.TextInput(attrs={'class': 'form-control'}),
            'address_actual': forms.TextInput(attrs={'class': 'form-control'})
        }
