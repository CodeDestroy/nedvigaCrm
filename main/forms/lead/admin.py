from django import forms
from django.db.models import Q

from main.forms import BaseModelForm
from main.models import Lead, User


class LeadAdminForm(BaseModelForm):
    class Meta:
        model = Lead
        fields = ('phone', 'surname', 'name', 'patronymic', 'email', 'processed', 'client', 'partner', 'warm',
                  'deferred', 'responsible', 'spam')
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'data-phone-pattern': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'client': forms.HiddenInput(attrs={'class': 'form-select'}),
            'partner': forms.HiddenInput(attrs={'class': 'form-select'}),
            'processed': forms.Select(attrs={'class': 'form-select'}),
            'warm': forms.Select(attrs={'class': 'form-select'}),
            'deferred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'responsible': forms.Select(attrs={'class': 'form-select'}),
            'spam': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(LeadAdminForm, self).__init__(*args, **kwargs)
        self.fields['responsible'].queryset = User.objects.filter(
            Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        self.fields['processed'].choices = (
            ('in_work', 'Взят в работу'),
            ('not', 'Не обработано'),
            ('complete', 'Обработано'),
            ('pre', 'Предварительно обработано'),
            ('redo', 'Возвращено в обработку')
        )

    def save(self, commit=True):
        phone = ''.join(filter(lambda i: i.isdigit(), self.cleaned_data['phone']))
        if phone[0] == 8:
            self.instance.phone = '7' + phone[1:]
        else:
            self.instance.phone = phone
        return super().save(commit=commit)
