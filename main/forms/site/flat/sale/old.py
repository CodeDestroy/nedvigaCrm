from django import forms

from main.forms import BaseForm


class FlatSaleOld(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Квартиры'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    MarketType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Вторичка'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
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
    Square = forms.FloatField(min_value=10, max_value=5000, label='Общая площадь недвижимости', required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    KitchenSpace = forms.FloatField(min_value=2, max_value=100, label='Общая площадь недвижимости', required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Status = forms.ChoiceField(label='Статус недвижимости', choices=(
        ('Квартира', 'Квартира'), ('Апартаменты', 'Апартаменты')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    RoomType = forms.MultipleChoiceField(label='Тип комнат', choices=(
        ('Изолированные', 'Изолированные'), ('Смежные', 'Смежные')
    ), required=True, widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Renovation = forms.ChoiceField(label='Ремонт', choices=(
        ('Требуется', 'Требуется'), ('Косметический', 'Косметический'), ('Евро', 'Евро'),
        ('Дизайнерский', 'Дизайнерский')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник'), ('Застройщик', 'Застройщик')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    DealType = forms.ChoiceField(label='Тип сделки', choices=(
        ('Прямая продажа', 'Прямая продажа'), ('Альтернативная', 'Альтернативная')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    # Необязательные поля
    SafeDemonstration = forms.ChoiceField(label='Онлайн показ', required=False, choices=(
        ('Могу провести', 'Могу провести'), ('Не хочу', 'Не хочу'),
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    BalconyOrLoggiaMulti = forms.MultipleChoiceField(label='Балкон или лоджия', required=False, choices=(
        ('Балкон', 'Балкон'), ('Лоджия', 'Лоджия')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    LeaseAppliances = forms.MultipleChoiceField(label='Бытовая техника', required=False, choices=(
        ('Кондиционер', 'Кондиционер'), ('Холодильник', 'Холодильник'), ('Стиральная машина', 'Стиральная машина'),
        ('Посудомоечная машина', 'Посудомоечная машина'), ('Водонагреватель', 'Водонагреватель')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    VideoFileURL = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    LivingSpace = forms.FloatField(label='Жилая площадь', min_value=5, max_value=5000, required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ApartmentNumber = forms.CharField(label='Номер квартиры', required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    ViewFromWindows = forms.MultipleChoiceField(label='Вид из окон', required=False, choices=(
        ('Во двор', 'Во двор'), ('На улицу', 'На улицу'), ('На солнечную сторону', 'На солнечную сторону'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    PassengerElevator = forms.ChoiceField(label='Пассажирский лифт', required=False, choices=(
        ('Нет', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    FreightElevator = forms.ChoiceField(label='Грузовой лифт', required=False, choices=(
        ('Нет', 'Нет'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    Courtyard = forms.MultipleChoiceField(label='Вид из окон', required=False, choices=(
        ('Закрытая территория', 'Закрытая территория'), ('Детская площадка', 'Детская площадка'),
        ('Спортивная площадка', 'Спортивная площадка'),
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Parking = forms.MultipleChoiceField(label='Парковка', required=False, choices=(
        ('Подземная', 'Подземная'), ('Наземная многоуровневая', 'Наземная многоуровневая'),
        ('Открытая во дворе', 'Открытая во дворе'), ('За шлагбаумом во дворе', 'За шлагбаумом во дворе')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    BathroomMulti = forms.MultipleChoiceField(label='Санузел', required=False, choices=(
        ('Совмещённый', 'Совмещённый'), ('Раздельный', 'Раздельный')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    SaleOptions = forms.MultipleChoiceField(label='Способ продажи дополнительно', required=False, choices=(
        ('Можно в ипотеку', 'Можно в ипотеку'), ('Продажа доли', 'Продажа доли'), ('Аукцион', 'Аукцион')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    CeilingHeight = forms.FloatField(label='Высота потолков', required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    NDAdditionally = forms.MultipleChoiceField(label='Дополнительно', required=False, choices=(
        ('Гардеробная', 'Гардеробная'), ('Панорамные окна', 'Панорамные окна')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    RepairAdditionally = forms.MultipleChoiceField(label='Ремонт дополнительные опции', required=False, choices=(
        ('Тёплый пол', 'Тёплый пол'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    RenovationProgram = forms.MultipleChoiceField(label='Реновация', required=False, choices=(
        ('Запланирован снос', 'Запланирован снос'),), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    InHouse = forms.MultipleChoiceField(label='В доме', required=False, choices=(
        ('Консьерж', 'Консьерж'), ('Мусоропровод', 'Мусоропровод'), ('Газоснабжение', 'Газоснабжение')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    SSAdditionally = forms.MultipleChoiceField(label='Дополнительно', required=False, choices=(
        ('Мебель', 'Мебель'), ('Бытовая техника', 'Бытовая техника'), ('Кондиционер', 'Кондиционер'),
        ('Гардеробная', 'Гардеробная'), ('Панорамные окна', 'Панорамные окна')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    Furniture = forms.MultipleChoiceField(label='Мебель', required=False, choices=(
        ('Кухня', 'Кухня'), ('Шкафы', 'Шкафы'), ('Спальные места', 'Спальные места')
    ), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    BuiltYear = forms.IntegerField(label='Год постройки', required=False,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
