from django import forms

from main.forms import BaseForm


class HouseLeaseDay(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Дома, дачи, коттеджи'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Сдам'}))
    LeaseType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Посуточно'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Rooms = forms.ChoiceField(label='Количество комнат', choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('9', '9'), ('10 и более', '10 и более'), ('Свободная планировка', 'Свободная планировка')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    ObjectType = forms.ChoiceField(label='Вид объекта', choices=(
        ('Дом', 'Дом'), ('Дача', 'Дача'), ('Коттедж', 'Коттедж'), ('Таунхаус', 'Таунхаус')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Floors = forms.ChoiceField(label='Количество этажей', choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4 и более', '4 и более')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Square = forms.FloatField(label='Площадь дома', required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LandArea = forms.FloatField(label='Площадь участка', help_text='В сотках', required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    SmokingAllowed = forms.BooleanField(label='Можно курить',
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    ChildrenAllowed = forms.BooleanField(label='Можно с детьми',
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    PetsAllowed = forms.BooleanField(label='Можно с животными',
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    PartiesAllowed = forms.BooleanField(label='Разрешены вечеринки и мероприятия',
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    Documents = forms.BooleanField(label='Есть отчётные документы',
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    LeaseDepositPrice = forms.IntegerField(label='Сумма залога', min_value=0, max_value=999999,
                                           widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # Необязательные поля
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    ContactMethod = forms.ChoiceField(label='Способ связи', required=False, choices=(
        ('По телефону и в сообщениях', 'По телефону и в сообщениях'),
        ('По телефону', 'По телефону'), ('В сообщениях', 'В сообщениях')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    LandAdditionally = forms.MultipleChoiceField(label='Дополнительно (на участке)', required=False, choices=(
        ('Баня или сауна', 'Баня или сауна'), ('Бассейн', 'Бассейн')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    BathroomMulti = forms.MultipleChoiceField(label='Санузел', required=False, choices=(
        ('В доме', 'В доме'), ('На улице', 'На улице')), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    HouseAdditionally = forms.MultipleChoiceField(label='Дополнительно (в доме)', required=False, choices=(
        ('Терраса или веранда', 'Терраса или веранда'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    HouseServices = forms.MultipleChoiceField(label='Коммуникации', required=False, choices=(
        ('Электричество', 'Электричество'), ('Газ', 'Газ'), ('Отопление', 'Отопление'), ('Канализация', 'Канализация'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
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
    LeaseMultimedia = forms.MultipleChoiceField(label='Мультимедиа', required=False, choices=(
        ('Wi-Fi', 'Wi-Fi'), ('Телевидение', 'Телевидение'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseBeds = forms.ChoiceField(label='Количество кроватей', required=False, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8+', '8+')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseSleepingPlaces = forms.ChoiceField(label='Количество спальных мест', required=False, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8 и более', '8 и более'),
        ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'),
        ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'),
        ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'),
        ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'),
        ('48', '48'), ('49', '49'), ('50 и более', '50 и более')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseAppliances = forms.MultipleChoiceField(label='Бытовая техника', required=False, choices=(
        ('Кондиционер', 'Кондиционер'), ('Холодильник', 'Холодильник'), ('Плита', 'Плита'),
        ('Микроволновка', 'Микроволновка'), ('Стиральная машина', 'Стиральная машина'),
        ('Посудомоечная машина', 'Посудомоечная машина'), ('Водонагреватель', 'Водонагреватель'),
        ('Телевизор', 'Телевизор'), ('Утюг', 'Утюг'), ('Фен', 'Фен')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseComfort = forms.MultipleChoiceField(label='Комфорт', required=False, choices=(
        ('Кондиционер', 'Кондиционер'), ('Камин', 'Камин'), ('Бассейн', 'Бассейн'), ('Баня / сауна', 'Баня / сауна')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
