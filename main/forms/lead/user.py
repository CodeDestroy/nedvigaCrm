from django import forms

from main.forms import BaseModelForm
from main.models import Lead


class LeadUserForm(BaseModelForm):
    class Meta:
        model = Lead
        fields = ('phone', 'surname', 'name', 'patronymic', 'email', 'processed', 'warm', 'deferred', 'spam')
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'data-phone-pattern': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'processed': forms.Select(attrs={'class': 'form-select'}),
            'warm': forms.Select(attrs={'class': 'form-select'}),
            'deferred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spam': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(LeadUserForm, self).__init__(*args, **kwargs)
        self.fields['processed'].choices = (
            ('in_work', 'Взят в работу'),
            ('not', 'Не обработано'),
            ('pre', 'Предварительно обработано'),
        )

    def save(self, commit=True):
        phone = ''.join(filter(lambda i: i.isdigit(), self.cleaned_data['phone']))
        if phone[0] == 8:
            self.instance.phone = '7' + phone[1:]
        else:
            self.instance.phone = phone
        return super().save(commit=commit)
