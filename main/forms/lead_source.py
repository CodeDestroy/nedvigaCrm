from django import forms

from . import BaseModelForm
from ..models import LeadSource


class LeadSourceForm(BaseModelForm):
    class Meta:
        model = LeadSource
        fields = ('source',)
        widgets = {'source': forms.Select(attrs={'class': 'form-select'})}
