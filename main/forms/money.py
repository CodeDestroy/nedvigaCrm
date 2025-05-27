from django import forms

from . import BaseModelForm
from ..models import Money


class MoneyForm(BaseModelForm):
    class Meta:
        model = Money
        fields = ('agent', 'paid', 'manager', 'get', 'get_date', 'status', 'bill_date', 'planned_date')
        widgets = {
            'agent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'manager': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'paid': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'get': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'get_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'bill_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'planned_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
