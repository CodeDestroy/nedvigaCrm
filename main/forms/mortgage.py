from django import forms

from . import BaseModelForm
from ..models import Mortgage


class MortgageForm(BaseModelForm):
    class Meta:
        model = Mortgage
        fields = ('max', 'sum', 'broker', 'broker_status')
        widgets = {
            'max': forms.NumberInput(attrs={'class': 'form-control'}),
            'sum': forms.NumberInput(attrs={'class': 'form-control'}),
            'broker': forms.Select(attrs={'class': 'form-select'}),
            'broker_status': forms.Select(attrs={'class': 'form-select'}),
        }
