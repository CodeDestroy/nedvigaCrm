from django import forms

from . import BaseModelForm
from ..models import Task


class TaskForm(BaseModelForm):
    class Meta:
        model = Task
        fields = ('priority', 'name', 'text', 'date_to')
        widgets = {
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'step': 1, 'min': 1, 'max': 5}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'date_to': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'},
                                           format='%Y-%m-%dT%H:%M')
        }
