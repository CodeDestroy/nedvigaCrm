from django import forms

from main.forms import BaseForm


class CommerceLease(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Коммерческая недвижимость'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Сдам'}))
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
    Entrance = forms.ChoiceField(label='Вход', choices=(('С улицы', 'С улицы'), ('Со двора', 'Со двора')),
                                 required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Floor = forms.IntegerField(label='Этаж', min_value=1, max_value=99, required=True,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Layout = forms.MultipleChoiceField(label='Планировка', required=True, choices=(
        ('Кабинетная', 'Кабинетная'), ('Открытая', 'Открытая')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Square = forms.IntegerField(label='Общая площадь объекта', min_value=5, max_value=100000, required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    CeilingHeight = forms.FloatField(label='Высота потолков', min_value=1, max_value=100, required=True,
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
    PlacesAmount = forms.IntegerField(label='Количество мест в коворкинге', required=True, min_value=1, max_value=1000,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    WeekendWork = forms.BooleanField(label='Работает ли в выходные', required=True,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    Working24Hours = forms.BooleanField(label='Работает ли круглосуточно', required=True,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    WorksFrom = forms.IntegerField(label='Работает С', min_value=0, max_value=24, required=True,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    WorksTill = forms.IntegerField(label='Работает До', min_value=0, max_value=24, required=True,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PlaceType = forms.ChoiceField(label='Статус рабочего места', required=True, choices=(
        ('Закреплённое место', 'Закреплённое место'), ('Плавающее место', 'Плавающее место'),
        ('Отдельный кабинет', 'Отдельный кабинет')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    RoomArea = forms.FloatField(label='Площадь кабинета', required=True, min_value=4, max_value=1000,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PlacesInRoom = forms.IntegerField(label='Количество рабочих мест в кабинете', required=True, min_value=4,
                                      max_value=1000, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    RentalType = forms.ChoiceField(label='Тип аренды', required=True, choices=(
        ('Прямая', 'Прямая'), ('Субаренда', 'Субаренда')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    Title = forms.CharField(label='Название', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    PriceWithVAT = forms.BooleanField(label='НДС включен', required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    AdditionalObjectTypes = forms.MultipleChoiceField(label='Вид объекта', required=False, choices=(
        ('Офис', 'Офис'), ('Свободного назначения', 'Свободного назначения'),
        ('Торговое помещение', 'Торговое помещение'), ('Склад', 'Склад'), ('Производство', 'Производство'),
        ('Общепит', 'Общепит'), ('Гостиница', 'Гостиница'), ('Автосервис', 'Автосервис'), ('Здание', 'Здание'),
        ('Коворкинг', 'Коворкинг')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', required=False, choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    PremisesType = forms.ChoiceField(label='Тип помещения', help_text='Только для торговых помещений', required=False,
                                     choices=(('Для уличной торговли', 'Для уличной торговли'),
                                              ('В торговом комплексе', 'В торговом комплексе'),),
                                     widget=forms.Select(attrs={'class': 'form-select'}))
    EntranceAdditionally = forms.MultipleChoiceField(label='Вход дополнительно', required=False, choices=(
        ('Отдельный вход', 'Отдельный вход'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    FloorAdditionally = forms.MultipleChoiceField(label='Этаж дополнительно', required=False, choices=(
        ('Несколько этажей', 'Несколько этажей'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    SquareAdditionally = forms.MultipleChoiceField(label='Площадь дополнительно', required=False, choices=(
        ('Возможная нарезка', 'Возможная нарезка'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Heating = forms.ChoiceField(label='Отопление', required=False, choices=(
        ('Нет', 'Нет'), ('Центральное', 'Центральное'), ('Автономное', 'Автономное'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    DistanceFromRoad = forms.ChoiceField(label='Отопление', required=False, choices=(
        ('Первая линия', 'Первая линия'), ('Вторая линия и дальше', 'Вторая линия и дальше'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    ParkingAdditionally = forms.MultipleChoiceField(label='Дополнительно о парковке', required=False, choices=(
        ('Бесплатная', 'Бесплатная'), ('Подходит для грузового транспорта', 'Подходит для грузового транспорта')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    ParkingSpaces = forms.IntegerField(label='Количество мест на парковке', max_value=10000, required=False,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    KeyConveniences = forms.MultipleChoiceField(label='Преимущества коворкинга', required=False, choices=(
        ('Современный ремонт', 'Современный ремонт'), ('Мебель', 'Мебель'), ('Wi-Fi', 'Wi-Fi'),
        ('Юридический адрес', 'Юридический адрес'), ('Охрана', 'Охрана'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    ConvenienceIncluded = forms.MultipleChoiceField(
        label='Включены ли в стоимость аренды преимущества коворкинга', required=False, choices=(
            ('Да', 'Да'), ('Нет', 'Нет'), ('Частично', 'Частично')
        ), widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    AvailableHardware = forms.MultipleChoiceField(label='Какое оборудование есть в коворкинге', required=False, choices=(
        ('Принтер', 'Принтер'), ('Сканер', 'Сканер'), ('Факс', 'Факс'), ('Флипчарт', 'Флипчарт')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    FoodAndDrinks = forms.MultipleChoiceField(label='Еда и напитки в коворкинге', required=False, choices=(
        ('Чай/Кофе', 'Чай/Кофе'), ('Фрукты и закуски', 'Фрукты и закуски'), ('Кухня', 'Кухня'), ('Кафе', 'Кафе')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    AvailableService = forms.MultipleChoiceField(label='Какие услуги у вас есть', required=False, choices=(
        ('Техническая поддержка', 'Техническая поддержка'), ('Ресепшн', 'Ресепшн'), ('Клининг', 'Клининг'),
        ('Специальные зоны', 'Специальные зоны'), ('Шкафчики', 'Шкафчики'), ('Телефонные будки', 'Телефонные будки'),
        ('Переговорные комнаты', 'Переговорные комнаты')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    AdditionalFacilities = forms.MultipleChoiceField(label='Что ещё вы предлагаете', required=False, choices=(
        ('Зоны отдыха', 'Зоны отдыха'), ('Участие в мероприятиях', 'Участие в мероприятиях'), ('Трансфер', 'Трансфер'),
        ('Парковка', 'Парковка'), ('Велопарковка', 'Велопарковка'), ('Спорт-зал', 'Спорт-зал')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    RentalHolidays = forms.MultipleChoiceField(label='Арендные каникулы', required=False, choices=(
        ('Арендные каникулы', 'Арендные каникулы'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    RentalMinimumPeriod = forms.IntegerField(label='Минимальный срок аренды', required=False,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LeasePriceOptions = forms.MultipleChoiceField(label='Цена', required=False, choices=(
        ('Оплата по счетчикам включена', 'Оплата по счетчикам включена'),
        ('Коммунальные услуги включены', 'Коммунальные услуги включены'),
        ('Эксплуатационные расходы включены', 'Эксплуатационные расходы включены')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    PriceType = forms.ChoiceField(label='Вариант задания цены', required=False, choices=(
        ('в месяц', 'в месяц'), ('в месяц за м2', 'в месяц за м2'), ('в год', 'в год'), ('в год за м2', 'в год за м2')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseDeposit = forms.ChoiceField(label='Залог', required=False, choices=(
        ('Без залога', 'Без залога'), ('0,5 месяца', '0,5 месяца'), ('1 месяц', '1 месяц'),
        ('1,5 месяца', '1,5 месяца'), ('2 месяца', '2 месяца'), ('2,5 месяца', '2,5 месяца'), ('3 месяца', '3 месяца')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseCommissionSize = forms.IntegerField(label='Размер комиссии в %', min_value=0, max_value=200, required=False,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
