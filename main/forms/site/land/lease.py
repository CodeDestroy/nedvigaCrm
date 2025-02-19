from django import forms

from main.forms import BaseForm


class LandLease(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Земельные участки'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Сдам'}))
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
    LeaseCommissionSize = forms.IntegerField(label='Размер комиссии в %', min_value=0, max_value=200, required=True,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LeaseDeposit = forms.ChoiceField(label='Залог', choices=(
        ('Без залога', 'Без залога'), ('0,5 месяца', '0,5 месяца'), ('1 месяц', '1 месяц'),
        ('1,5 месяца', '1,5 месяца'),
        ('2 месяца', '2 месяца'), ('2,5 месяца', '2,5 месяца'), ('3 месяца', '3 месяца')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    ObjectType = forms.ChoiceField(label='Категория земель', required=True, choices=(
        ('Поселений (ИЖС)', 'Поселений (ИЖС)'), ('Сельхозназначения (СНТ, ДНП)', 'Сельхозназначения (СНТ, ДНП)'),
        ('Промназначения', 'Промназначения'), ('Личное подсобное хозяйство (ЛПХ)', 'Личное подсобное хозяйство (ЛПХ)')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
