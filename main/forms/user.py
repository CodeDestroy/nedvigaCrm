from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

from . import BaseModelForm
from ..models import User


class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone', 'birth', 'first_name', 'last_name', 'sip', 'funnel',
                  'is_staff', 'return_to_list', 'debetor', 'in_stat', 'broker', 'can_be_responsible', 'telegram_id',
                  'telegram_username', 'can_change_exclusive_responsible')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sip': forms.Select(attrs={'class': 'form-select'}),
            'funnel': forms.Select(attrs={'class': 'form-select'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'return_to_list': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'debetor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'in_stat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'broker': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_be_responsible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_change_exclusive_responsible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telegram_id': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].label = 'Является администратором?'
        self.fields['is_staff'].help_text = None

    def save(self, commit=True):
        phone = ''.join(filter(lambda i: i.isdigit(), self.cleaned_data['phone']))
        if phone[0] == 8:
            self.instance.phone = '7' + phone[1:]
        else:
            self.instance.phone = phone
        if self.instance.sip:
            try:
                user = User.objects.get(sip=self.instance.sip)
                user.sip = None
                user.save()
            except ObjectDoesNotExist:
                pass
        self.instance.password = make_password(self.cleaned_data['password'])
        return super().save(commit=commit)


class UserUpdateForm(BaseModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'birth', 'first_name', 'last_name', 'sip', 'funnel', 'fired',
                  'is_staff', 'return_to_list', 'debetor', 'in_stat', 'broker', 'can_be_responsible', 'telegram_id',
                  'telegram_username', 'can_change_exclusive_responsible')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sip': forms.Select(attrs={'class': 'form-select'}),
            'funnel': forms.Select(attrs={'class': 'form-select'}),
            'fired': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'return_to_list': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'debetor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'in_stat': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'broker': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_be_responsible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_change_exclusive_responsible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telegram_id': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].label = 'Является администратором?'
        self.fields['is_staff'].help_text = None

    def save(self, commit=True):
        phone = ''.join(filter(lambda i: i.isdigit(), self.cleaned_data['phone']))
        if phone[0] == 8:
            self.instance.phone = '7' + phone[1:]
        else:
            self.instance.phone = phone
        if self.instance.sip:
            try:
                user = User.objects.get(sip=self.instance.sip)
                user.sip = None
                user.save()
            except ObjectDoesNotExist:
                pass
        return super().save(commit=commit)
