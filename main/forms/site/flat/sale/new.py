from django import forms

from main.forms import BaseForm


class FlatSaleNew(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Квартиры'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    MarketType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Новостройка'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Rooms = forms.ChoiceField(label='Количество комнат', choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('9', '9'), ('10 и более', '10 и более'), ('Свободная планировка', 'Свободная планировка')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    HouseType = forms.ChoiceField(label='Тип дома', choices=(
        ('Кирпичный', 'Кирпичный'), ('Панельный', 'Панельный'), ('Блочный', 'Блочный'), ('Монолитный', 'Монолитный'),
        ('Монолитно-кирпичный', 'Монолитно-кирпичный')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Floor = forms.IntegerField(min_value=1, max_value=99, label='Этаж', required=True,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Floors = forms.IntegerField(min_value=1, max_value=99, label='Этажей', required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Square = forms.FloatField(min_value=10, max_value=5000, label='Общая площадь', required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Status = forms.ChoiceField(label='Статус недвижимости', choices=(
        ('Квартира', 'Квартира'), ('Апартаменты', 'Апартаменты')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    NewDevelopmentId = forms.CharField(label='ID объекта новостройки',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник'), ('Застройщик', 'Застройщик')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Decoration = forms.ChoiceField(label='Отделка помещения', choices=(
        ('Без отделки', 'Без отделки'), ('Предчистовая', 'Предчистовая'), ('Чистовая', 'Чистовая')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    SaleMethod = forms.ChoiceField(label='Отделка помещения', required=False, choices=(
        ('Договор долевого участия', 'Договор долевого участия'),
        ('Договор уступки права требования', 'Договор уступки права требования'), ('Договор ЖСК', 'Договор ЖСК')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    ShareholderLastName = forms.CharField(label='Фамилия дольщика', help_text='При продаже по ДДУ', required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    ShareholderFirstName = forms.CharField(label='Имя дольщика', help_text='При продаже по ДДУ', required=False,
                                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    ShareholderPatronymic = forms.CharField(label='Отчество дольщика', help_text='При продаже по ДДУ', required=False,
                                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    ShareholderINN = forms.CharField(label='ИНН дольщика', help_text='При продаже по ДДУ', required=False,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
