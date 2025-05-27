from django import forms

from . import BaseModelForm
from ..models import Showing


class ShowingForm(BaseModelForm):
    class Meta:
        model = Showing
        fields = ('description', 'date_to')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date_to': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},
                                           format='%Y-%m-%dT%H:%M'),
        }
