from django import forms

from main.forms import BaseForm


class CommerceSale(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Коммерческая недвижимость'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ObjectType = forms.ChoiceField(label='Вид объекта', choices=(
        ('Офисное помещение', 'Офисное помещение'),
        ('Помещение свободного назначения', 'Помещение свободного назначения'),
        ('Торговое помещение', 'Торговое помещение'), ('Складское помещение', 'Складское помещение'),
        ('Производственное помещение', 'Производственное помещение'),
        ('Помещение общественного питания', 'Помещение общественного питания'),
        ('Гостиница', 'Гостиница'), ('Автосервис', 'Автосервис'), ('Здание', 'Здание'), ('Коворкинг', 'Коворкинг')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    PropertyRights = forms.ChoiceField(
        label='Право собственности', choices=(('Собственник', 'Собственник'), ('Посредник', 'Посредник')),
        required=True, widget=forms.Select(attrs={'class': 'form-select'})
    )
    Entrance = forms.ChoiceField(label='Вход', choices=(
        ('С улицы', 'С улицы'), ('Со двора', 'Со двора')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Floor = forms.IntegerField(label='Этаж', min_value=1, max_value=99, required=True,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Layout = forms.MultipleChoiceField(label='Планировка', required=True, choices=(
        ('Кабинетная', 'Кабинетная'), ('Открытая', 'Открытая')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Square = forms.IntegerField(label='Общая площадь объекта', min_value=5, max_value=100000, required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Decoration = forms.ChoiceField(label='Отделка помещения', required=True, choices=(
        ('Без отделки', 'Без отделки'), ('Чистовая', 'Чистовая'), ('Офисная', 'Офисная')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    BuildingType = forms.ChoiceField(label='Тип здания', required=True, choices=(
        ('Бизнес-центр', 'Бизнес-центр'), ('Торговый центр', 'Торговый центр'),
        ('Административное здание', 'Административное здание'), ('Жилой дом', 'Жилой дом'), ('Другой', 'Другой')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    ParkingType = forms.ChoiceField(label='Тип парковки', required=True, choices=(
        ('Нет', 'Нет'), ('На улице', 'На улице'), ('В здании', 'В здании')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    TransactionType = forms.ChoiceField(label='Тип сделки', required=True, choices=(
        ('Продажа', 'Продажа'), ('Переуступка права аренды', 'Переуступка права аренды'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    Title = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoFileURL = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    PriceWithVAT = forms.BooleanField(label='НДС включен', required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    AdditionalObjectTypes = forms.MultipleChoiceField(label='Вид объекта', required=False, choices=(
        ('Офис', 'Офис'), ('Свободного назначения', 'Свободного назначения'),
        ('Торговое помещение', 'Торговое помещение'), ('Склад', 'Склад'), ('Производство', 'Производство'),
        ('Общепит', 'Общепит'), ('Гостиница', 'Гостиница'), ('Автосервис', 'Автосервис'), ('Здание', 'Здание'),
        ('Коворкинг', 'Коворкинг')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    PremisesType = forms.ChoiceField(label='Тип помещения', help_text='Только для торговых помещений', required=False,
                                     choices=(('Для уличной торговли', 'Для уличной торговли'),
                                              ('В торговом комплексе', 'В торговом комплексе'),),
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    EntranceAdditionally = forms.MultipleChoiceField(label='Вход дополнительно', required=False, choices=(
        ('Отдельный вход', 'Отдельный вход'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    FloorAdditionally = forms.MultipleChoiceField(label='Этаж дополнительно', required=False, choices=(
        ('Несколько этажей', 'Несколько этажей'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    CeilingHeight = forms.FloatField(label='Высота потолков', min_value=1, max_value=100, required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PowerGridCapacity = forms.IntegerField(label='Мощность электросети', required=False,
                                           widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PowerGridAdditionally = forms.MultipleChoiceField(label='Электросеть дополнительно', required=False, choices=(
        ('Возможно увеличение мощности', 'Возможно увеличение мощности'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Heating = forms.ChoiceField(label='Отопление', required=False, choices=(
        ('Нет', 'Нет'), ('Центральное', 'Центральное'), ('Автономное', 'Автономное'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    ReadinessStatus = forms.ChoiceField(label='Отопление', required=False, choices=(
        ('Проект', 'Проект'), ('Строится', 'Строится'), ('В эксплуатации', 'В эксплуатации'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    DistanceFromRoad = forms.ChoiceField(label='Отопление', required=False, choices=(
        ('Первая линия', 'Первая линия'), ('Вторая линия и дальше', 'Вторая линия и дальше'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    ParkingAdditionally = forms.MultipleChoiceField(label='Дополнительно о парковке', required=False, choices=(
        ('Бесплатная', 'Бесплатная'), ('Подходит для грузового транспорта', 'Подходит для грузового транспорта')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    ParkingSpaces = forms.IntegerField(label='Количество мест на парковке', max_value=10000, required=False,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    CurrentTenants = forms.MultipleChoiceField(label='Текущие арендаторы', required=False, choices=(
        ('Помещение занято', 'Помещение занято'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    PriceType = forms.ChoiceField(label='Вариант задания цены', required=False, choices=(
        ('в месяц', 'в месяц'), ('в месяц за м2', 'в месяц за м2'), ('в год', 'в год'), ('в год за м2', 'в год за м2')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    SaleOptions = forms.MultipleChoiceField(label='Способ продажи', required=False, choices=(
        ('Аукцион', 'Аукцион'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
