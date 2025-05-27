from django import forms

from main.forms import BaseForm


class RoomLease(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Комнаты'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Сдам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ResidenceType = forms.ChoiceField(label='Тип жилья', required=True, choices=(
        ('Комната', 'Комната'), ('Койко-место', 'Койко-место'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    RoomLocationType = forms.ChoiceField(label='Расположение комнаты', required=True, choices=(
        ('Квартира', 'Квартира'), ('Хостел', 'Хостел'), ('Гостиница', 'Гостиница')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    BedLocationType = forms.ChoiceField(label='Расположение койко-места', required=True, choices=(
        ('Квартира', 'Квартира'), ('Хостел', 'Хостел')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
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
    LeaseType = forms.ChoiceField(label='Тип аренды', required=True, choices=(
        ('На длительный срок', 'На длительный срок'), ('Посуточно', 'Посуточно')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseDeposit = forms.ChoiceField(label='Залог', required=True, choices=(
        ('Без залога', 'Без залога'), ('0,5 месяца', '0,5 месяца'), ('1 месяц', '1 месяц'), ('1,5 месяца', '1,5 месяца'),
        ('2 месяца', '2 месяца'), ('2,5 месяца', '2,5 месяца'), ('3 месяца', '3 месяца')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseCommissionSize = forms.IntegerField(label='Размер комиссии в %', min_value=0, max_value=200, required=True,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # Необязательные поля
    LeaseBeds = forms.ChoiceField(label='Количество кроватей', required=False, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8+', '8+')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseSleepingPlaces = forms.ChoiceField(label='Количество спальных мест', required=False, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16+', '16+'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseMultimedia = forms.MultipleChoiceField(label='Мультимедиа', required=False, choices=(
        ('Wi-Fi', 'Wi-Fi'), ('Телевизор', 'Телевизор'), ('Кабельное / цифровое ТВ', 'Кабельное / цифровое ТВ')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseAppliances = forms.MultipleChoiceField(label='Бытовая техника', required=False, choices=(
        ('Плита', 'Плита'), ('Микроволновка', 'Микроволновка'), ('Холодильник', 'Холодильник'),
        ('Стиральная машина', 'Стиральная машина'), ('Фен', 'Фен'), ('Утюг', 'Утюг')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseComfort = forms.MultipleChoiceField(label='Комфорт', required=False, choices=(
        ('Кондиционер', 'Кондиционер'), ('Камин', 'Камин'), ('Балкон / лоджия', 'Балкон / лоджия'),
        ('Парковочное место', 'Парковочное место')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseAdditionally = forms.MultipleChoiceField(label='Комфорт', required=False, choices=(
        ('Можно с питомцами', 'Можно с питомцами'), ('Можно с детьми', 'Можно с детьми'),
        ('Можно для мероприятий', 'Можно для мероприятий'), ('Можно курить', 'Можно курить')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
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
