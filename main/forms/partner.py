from django import forms

from . import BaseModelForm
from ..models import Partner


class PartnerForm(BaseModelForm):
    class Meta:
        model = Partner
        fields = ('surname', 'name', 'patronymic', 'phone', 'email', 'company')
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'data-phone-pattern': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        phone = ''.join(filter(lambda i: i.isdigit(), self.cleaned_data['phone']))
        if phone[0] == 8:
            self.instance.phone = '7' + phone[1:]
        else:
            self.instance.phone = phone
        return super().save(commit=commit)
