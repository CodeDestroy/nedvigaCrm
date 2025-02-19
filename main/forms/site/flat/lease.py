from django import forms

from main.forms import BaseForm


class FlatLease(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Квартиры'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Сдам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Rooms = forms.ChoiceField(label='Количество комнат', choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('9', '9'), ('10 и более', '10 и более'), ('Свободная планировка', 'Свободная планировка')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    RoomType = forms.MultipleChoiceField(label='Тип комнат', choices=(
        ('Изолированные', 'Изолированные'), ('Смежные', 'Смежные')
    ), required=True, widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Renovation = forms.ChoiceField(label='Ремонт', choices=(
        ('Требуется', 'Требуется'), ('Косметический', 'Косметический'),
        ('Евро', 'Евро'), ('Дизайнерский', 'Дизайнерский')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseType = forms.ChoiceField(label='Тип аренды', choices=(
        ('На длительный срок', 'На длительный срок'), ('Посуточно', 'Посуточно')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    HouseType = forms.ChoiceField(label='Тип дома', choices=(
        ('Кирпичный', 'Кирпичный'), ('Панельный', 'Панельный'), ('Блочный', 'Блочный'), ('Монолитный', 'Монолитный'),
        ('Монолитно-кирпичный', 'Монолитно-кирпичный'), ('Деревянный', 'Деревянный')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    Floor = forms.IntegerField(min_value=1, max_value=99, label='Этаж', required=True,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Floors = forms.IntegerField(min_value=1, max_value=99, label='Этажей', required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Square = forms.FloatField(min_value=10, max_value=5000, label='Общая площадь', required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LeaseDeposit = forms.ChoiceField(label='Залог', choices=(
        ('Без залога', 'Без залога'), ('0,5 месяца', '0,5 месяца'), ('1 месяц', '1 месяц'), ('1,5 месяца', '1,5 месяца'),
        ('2 месяца', '2 месяца'), ('2,5 месяца', '2,5 месяца'), ('3 месяца', '3 месяца')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseCommissionSize = forms.IntegerField(label='Размер комиссии в %', min_value=0, max_value=200, required=True,
                                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    KitchenSpace = forms.IntegerField(label='Площадь кухни', min_value=2, max_value=100, required=True,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    UtilityMeters = forms.ChoiceField(label='Оплата по счетчикам', choices=(
        ('Оплачивается арендатором', 'Оплачивается арендатором'),
        ('Оплачивается собственником', 'Оплачивается собственником')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    OtherUtilities = forms.ChoiceField(label='Другие ЖКУ', choices=(
        ('Оплачивается арендатором', 'Оплачивается арендатором'),
        ('Оплачивается собственником', 'Оплачивается собственником')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    OtherUtilitiesPayment = forms.IntegerField(label='Плата за другие ЖКУ', required=True,
                                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    SmokingAllowed = forms.BooleanField(label='Можно курить', required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    ChildrenAllowed = forms.BooleanField(label='Можно с детьми', required=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    PetsAllowed = forms.BooleanField(label='Можно с животными', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    # Необязательные поля
    SafeDemonstration = forms.ChoiceField(label='Онлайн показ', required=False, choices=(
        ('Могу провести', 'Могу провести'), ('Не хочу', 'Не хочу'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    BalconyOrLoggiaMulti = forms.MultipleChoiceField(label='Балкон или лоджия', required=False, choices=(
        ('Балкон', 'Балкон'), ('Лоджия', 'Лоджия')), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseAppliances = forms.MultipleChoiceField(label='Бытовая техника', required=False, choices=(
        ('Кондиционер', 'Кондиционер'), ('Холодильник', 'Холодильник'), ('Стиральная машина', 'Стиральная машина'),
        ('Посудомоечная машина', 'Посудомоечная машина'), ('Водонагреватель', 'Водонагреватель'), ('Плита', 'Плита'),
        ('Микроволновка', 'Микроволновка'), ('Телевизор', 'Телевизор')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    ApartmentNumber = forms.CharField(label='Номер квартиры', required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    Status = forms.ChoiceField(label='Статус недвижимости', required=False, choices=(
        ('Квартира', 'Квартира'), ('Апартаменты', 'Апартаменты')), widget=forms.Select(attrs={'class': 'form-select'}))
    PassengerElevator = forms.ChoiceField(label='Пассажирский лифт', required=False, choices=(
        ('Нет', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    FreightElevator = forms.ChoiceField(label='Грузовой лифт', required=False, choices=(
        ('Нет', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    Parking = forms.MultipleChoiceField(label='Парковка', required=False, choices=(
        ('Подземная', 'Подземная'), ('Наземная многоуровневая', 'Наземная многоуровневая'),
        ('Открытая во дворе', 'Открытая во дворе'), ('За шлагбаумом во дворе', 'За шлагбаумом во дворе')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    BathroomMulti = forms.MultipleChoiceField(label='Санузел', required=False, choices=(
        ('Совмещённый', 'Совмещённый'), ('Раздельный', 'Раздельный')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    NDAdditionally = forms.MultipleChoiceField(label='Дополнительно', required=False, choices=(
        ('Гардеробная', 'Гардеробная'), ('Панорамные окна', 'Панорамные окна')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Furniture = forms.MultipleChoiceField(label='Мебель', required=False, choices=(
        ('Кухня', 'Кухня'), ('Шкафы', 'Шкафы'), ('Спальные места', 'Спальные места')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    BuiltYear = forms.IntegerField(label='Год постройки', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LivingSpace = forms.FloatField(label='Жилая площадь', min_value=5, max_value=5000, required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    LeaseSleepingPlaces = forms.ChoiceField(label='Количество спальных мест', required=False, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8 и более', '8 и более'),
        ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'),
        ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'),
        ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'),
        ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'),
        ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'),
        ('16+', '16+')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseBeds = forms.ChoiceField(label='Количество кроватей', required=False, choices=(
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8+', '8+')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    LeaseMultimedia = forms.MultipleChoiceField(label='Мультимедиа', required=False, choices=(
        ('Wi-Fi', 'Wi-Fi'), ('Телевидение', 'Телевидение'), ('Телевизор', 'Телевизор'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseComfort = forms.MultipleChoiceField(label='Комфорт', required=False, choices=(
        ('Кондиционер', 'Кондиционер'), ('Камин', 'Камин'), ('Балкон / лоджия', 'Балкон / лоджия'),
        ('Парковочное место', 'Парковочное место')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseAdditionally = forms.MultipleChoiceField(label='Комфорт', required=False, choices=(
        ('Можно с питомцами', 'Можно с питомцами'), ('Можно с детьми', 'Можно с детьми'),
        ('Можно для мероприятий', 'Можно для мероприятий'), ('Можно курить', 'Можно курить')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    ParkingType = forms.MultipleChoiceField(label='Тип парковки', required=False, choices=(
        ('Нет', 'Нет'), ('На улице', 'На улице'), ('В здании', 'В здании')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    ParkingAdditionally = forms.MultipleChoiceField(label='Тип парковки', required=False, choices=(
        ('Бесплатная', 'Бесплатная'), ('Подходит для грузового транспорта', 'Подходит для грузового транспорта')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseComfortMulti = forms.MultipleChoiceField(label='Комфорт', required=False, choices=(
        ('Постельное белье', 'Постельное белье'), ('Полотенца', 'Полотенца'), ('Средства гигиены', 'Средства гигиены')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    PartiesAllowed = forms.BooleanField(label='Разрешены вечеринки и мероприятия', required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    Documents = forms.BooleanField(label='Есть отчётные документы', required=False,
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    LeaseDepositPrice = forms.IntegerField(min_value=0, max_value=999999, label='Сумма залога', required=False,
                                           widget=forms.NumberInput(attrs={'class': 'form-control'}))
