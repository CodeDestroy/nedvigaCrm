from django import forms

from main.forms import BaseForm


class LandSale(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Земельные участки'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    LandArea = forms.FloatField(min_value=1, label='Площадь участка в сотках', required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ObjectType = forms.ChoiceField(label='Категория земель', choices=(
        ('Поселений (ИЖС)', 'Поселений (ИЖС)'), ('Сельхозназначения (СНТ, ДНП)', 'Сельхозназначения (СНТ, ДНП)'),
        ('Промназначения', 'Промназначения'), ('Личное подсобное хозяйство (ЛПХ)', 'Личное подсобное хозяйство (ЛПХ)')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
