from django import forms

from main.forms import BaseForm


class HouseSale(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Дома, дачи, коттеджи'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Rooms = forms.ChoiceField(label='Количество комнат', choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('9', '9'), ('10 и более', '10 и более'), ('Свободная планировка', 'Свободная планировка')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    ObjectType = forms.ChoiceField(label='Вид объекта', choices=(
        ('Дом', 'Дом'), ('Дача', 'Дача'), ('Коттедж', 'Коттедж'), ('Таунхаус', 'Таунхаус')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Floors = forms.ChoiceField(label='Количество этажей', choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4 и более', '4 и более')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    WallsType = forms.ChoiceField(label='Материал стен', choices=(
        ('Кирпич', 'Кирпич'), ('Брус', 'Брус'), ('Бревно', 'Бревно'), ('Газоблоки', 'Газоблоки'),
        ('Металл', 'Металл'), ('Пеноблоки', 'Пеноблоки'), ('Сэндвич-панели', 'Сэндвич-панели'),
        ('Ж/б панели', 'Ж/б панели'), ('Экспериментальные материалы', 'Экспериментальные материалы')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Square = forms.FloatField(label='Площадь дома', required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LandArea = forms.FloatField(label='Площадь участка', help_text='В сотках', required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LandStatus = forms.ChoiceField(label='Статус участка', choices=(
        ('Индивидуальное жилищное строительство (ИЖС)', 'Индивидуальное жилищное строительство (ИЖС)'),
        ('Садовое некоммерческое товарищество(СНТ)', 'Садовое некоммерческое товарищество(СНТ)'),
        ('Дачное некоммерческое партнёрство(ДНП)', 'Дачное некоммерческое партнёрство(ДНП)'),
        ('Фермерское хозяйство', 'Фермерское хозяйство'),
        ('Личное подсобное хозяйство(ЛПХ)', 'Личное подсобное хозяйство(ЛПХ)')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Renovation = forms.ChoiceField(label='Ремонт', choices=(
        ('Требуется', 'Требуется'), ('Косметический', 'Косметический'),
        ('Евро', 'Евро'), ('Дизайнерский', 'Дизайнерский')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    ContactMethod = forms.ChoiceField(label='Способ связи', required=False, choices=(
        ('По телефону и в сообщениях', 'По телефону и в сообщениях'),
        ('По телефону', 'По телефону'), ('В сообщениях', 'В сообщениях')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    SafeDemonstration = forms.ChoiceField(label='Онлайн показ', required=False, choices=(
        ('Могу провести', 'Могу провести'), ('Не хочу', 'Не хочу')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LandAdditionally = forms.MultipleChoiceField(label='Дополнительно (на участке)', required=False, choices=(
        ('Баня или сауна', 'Баня или сауна'), ('Бассейн', 'Бассейн')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    BathroomMulti = forms.MultipleChoiceField(label='Санузел', required=False, choices=(
        ('В доме', 'В доме'), ('На улице', 'На улице')), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    HouseAdditionally = forms.MultipleChoiceField(label='Дополнительно (в доме)', required=False, choices=(
        ('Терраса или веранда', 'Терраса или веранда'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Electricity = forms.ChoiceField(label='Электричество', required=False, choices=(('Нет', 'Нет'), ('Есть', 'Есть')),
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    GasSupply = forms.ChoiceField(label='Газ', required=False, choices=(
        ('Нет', 'Нет'), ('По границе участка', 'По границе участка'), ('В доме', 'В доме')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    Heating = forms.ChoiceField(label='Отопление', required=False, choices=(('Нет', 'Нет'), ('Есть', 'Есть')),
                                widget=forms.Select(attrs={'class': 'form-select'}))
    HeatingType = forms.MultipleChoiceField(label='Виды отопления', required=False, choices=(
        ('Центральное', 'Центральное'), ('Газовое', 'Газовое'), ('Электрическое', 'Электрическое'),
        ('Жидкотопливный котёл', 'Жидкотопливный котёл'), ('Печь', 'Печь'), ('Камин', 'Камин'), ('Другое', 'Другое')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    WaterSupply = forms.ChoiceField(label='Водоснабжение', required=False, choices=(
        ('Нет', 'Нет'), ('Центральное', 'Центральное'), ('Скважина', 'Скважина'), ('Колодец', 'Колодец')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    Sewerage = forms.ChoiceField(label='Канализация', required=False, choices=(
        ('Центральная', 'Центральная'), ('Септик', 'Септик'), ('Выгребная яма', 'Выгребная яма'),
        ('Станция биоочистки', 'Станция биоочистки'), ('Нет', 'Нет')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    TransportAccessibility = forms.MultipleChoiceField(label='Транспортная доступность', required=False, choices=(
        ('Асфальтированная дорога', 'Асфальтированная дорога'),
        ('Остановка общественного транспорта', 'Остановка общественного транспорта'),
        ('Железнодорожная станция', 'Железнодорожная станция')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Infrastructure = forms.MultipleChoiceField(label='Инфраструктура', required=False, choices=(
        ('Магазин', 'Магазин'), ('Аптека', 'Аптека'), ('Детский сад', 'Детский сад'), ('Школа', 'Школа'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    ParkingType = forms.ChoiceField(label='Тип парковки', required=False, choices=(
        ('Нет', 'Нет'), ('Гараж', 'Гараж'), ('Парковочное место', 'Парковочное место')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    BuiltYear = forms.IntegerField(label='Год постройки', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LeaseMultimedia = forms.MultipleChoiceField(label='Мультимедиа', required=False, choices=(
        ('Wi-Fi', 'Wi-Fi'), ('Телевидение', 'Телевидение'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    SaleOptions = forms.MultipleChoiceField(label='Способ продажи дополнительно', required=False, choices=(
        ('Можно в ипотеку', 'Можно в ипотеку'), ('Продажа доли', 'Продажа доли'), ('Аукцион', 'Аукцион')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
