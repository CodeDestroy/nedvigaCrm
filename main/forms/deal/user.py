from django import forms

from main.forms import BaseModelForm
from main.fields import GroupedModelChoiceField
from main.models import Deal, Stage


class DealUserForm(BaseModelForm):
    class Meta:
        model = Deal
        fields = ('stage', 'buy_object', 'name', 'paytype', 'legal_status', 'price',
                  'developer', 'office', 'solution', 'bank', 'frm', 'sell_date', 'reserved', 'spam')
        widgets = {
            'buy_object': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'paytype': forms.Select(attrs={'class': 'form-select'}),
            'legal_status': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'developer': forms.TextInput(attrs={'class': 'form-control'}),
            'office': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'solution': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bank': forms.Select(attrs={'class': 'form-select'}),
            'frm': forms.Select(attrs={'class': 'form-select'}),
            'sell_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'reserved': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'spam': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(DealUserForm, self).__init__(*args, **kwargs)
        self.fields['stage'] = GroupedModelChoiceField(
            queryset=Stage.objects.all(), choices_groupby='funnel', widget=forms.Select(attrs={'class': 'form-select'}),
            empty_label='Стадия не выбрана', label='Стадия продажи', required=False
        )
