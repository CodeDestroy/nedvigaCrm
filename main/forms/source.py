from django import forms

from . import BaseModelForm
from ..models import Source


class SourceForm(BaseModelForm):
    class Meta:
        model = Source
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
