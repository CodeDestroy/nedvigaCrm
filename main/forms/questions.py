from django import forms

from . import BaseModelForm
from ..models import Questions


class QuestionsForm(BaseModelForm):
    class Meta:
        model = Questions
        fields = ('district', 'budget', 'rooms', 'deadline', 'purpose', 'decoration', 'developer', 'payment', 'bank',
                  'maternity', 'birth_date', 'residence_place', 'residence_birth', 'marital_status', 'child_count',
                  'child_ages')
        widgets = {
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.TextInput(attrs={'class': 'form-control'}),
            'rooms': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
            'decoration': forms.Select(attrs={'class': 'form-select'}),
            'developer': forms.TextInput(attrs={'class': 'form-control'}),
            'payment': forms.Select(attrs={'class': 'form-select'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'maternity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'residence_place': forms.TextInput(attrs={'class': 'form-control'}),
            'residence_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'child_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'child_ages': forms.TextInput(attrs={'class': 'form-control'}),
        }
