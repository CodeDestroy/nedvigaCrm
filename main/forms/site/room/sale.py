from django import forms

from main.forms import BaseForm


class RoomSale(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Комнаты'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # OperationType = Продам
    HouseType = forms.ChoiceField(label='Тип дома', choices=(
        ('Кирпичный', 'Кирпичный'), ('Панельный', 'Панельный'), ('Блочный', 'Блочный'), ('Монолитный', 'Монолитный'),
        ('Деревянный', 'Деревянный')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Rooms = forms.ChoiceField(label='Количество комнат', required=True, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('> 9', '> 9')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    Floor = forms.IntegerField(min_value=1, max_value=99, label='Этаж', required=True,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Floors = forms.IntegerField(min_value=1, max_value=99, label='Этажей', required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Square = forms.FloatField(min_value=6, max_value=100, label='Площадь', required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # Необязательные поля
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    ContactMethod = forms.ChoiceField(label='Способ связи', required=False, choices=(
        ('По телефону и в сообщениях', 'По телефону и в сообщениях'),
        ('По телефону', 'По телефону'), ('В сообщениях', 'В сообщениях')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    SafeDemonstration = forms.ChoiceField(label='Онлайн показ', required=False, choices=(
        ('Могу провести', 'Могу провести'), ('Не хочу', 'Не хочу'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
