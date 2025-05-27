from django import forms

from . import BaseModelForm
from ..models import MessageTemplate


class MessageTemplateForm(BaseModelForm):
    class Meta:
        model = MessageTemplate
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control'})}
