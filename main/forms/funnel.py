from django import forms

from . import BaseModelForm
from ..models import Funnel


class FunnelForm(BaseModelForm):
    class Meta:
        model = Funnel
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
