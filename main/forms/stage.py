from django import forms
from django.core.exceptions import ObjectDoesNotExist

from . import BaseModelForm
from ..models import Stage, Funnel


class StageForm(BaseModelForm):
    class Meta:
        model = Stage
        fields = ('parent', 'name', 'statistic', 'deal_close')
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'statistic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deal_close': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    funnel = None

    def __init__(self, funnel_id=None, *args, **kwargs):
        super(StageForm, self).__init__(*args, **kwargs)
        try:
            self.funnel = Funnel.objects.prefetch_related('stage_set').get(pk=funnel_id)
            qs = self.funnel.stage_set.all()
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            self.fields['parent'].queryset = qs
        except ObjectDoesNotExist:
            pass

    def save(self, commit=True):
        self.instance = super().save(False)
        self.instance.funnel = self.funnel
        prev_child = None
        try:
            if self.instance.parent:
                prev_child = Stage.objects.get(parent=self.instance.parent)
            else:
                prev_child = Stage.objects.get(parent=None, funnel=self.funnel)
        except ObjectDoesNotExist:
            pass

        self.instance.save()

        if prev_child and prev_child.pk != self.instance.pk:
            prev_child.parent = self.instance
            prev_child.save()
        return self.instance
