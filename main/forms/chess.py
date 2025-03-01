from django import forms
from . import BaseModelForm
from ..models import Complex, Building, Apartment

class ApartmentForm(BaseModelForm):
    class Meta:
        model = Apartment
        fields = ('number', 'window_orientation', 'area', 'rooms', 'apartment_type', 'price')  # Поля для редактирования

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'window_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'apartment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

