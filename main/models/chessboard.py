from django.conf import settings
from django.db import models
from django.urls import reverse

from . import CreatedUpdatedMixin

class Complex(CreatedUpdatedMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')
    region = models.CharField(max_length=255, null=True, blank=True, verbose_name='Регион')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name='Город')
    avito_id = models.CharField(max_length=255, null=True, blank=True)
    alternative_description = models.TextField(null=True, blank=True, verbose_name='Альтернативное описание (перезаписывает всё описание)')
    """ image = models.ImageField(upload_to='complex_images/', null=True, blank=True) """
    def total_apartments(self):
        return Apartment.objects.filter(building__complex=self).count()
    def __str__(self):
        return self.name
    
    class Meta(object):
        app_label = 'main'
        db_table = 'complex'
        verbose_name = 'ЖК'
        verbose_name_plural = 'ЖК'

class Building(CreatedUpdatedMixin):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=255)
    total_floors = models.IntegerField()
    total_apartments = models.IntegerField()
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')
    region = models.CharField(max_length=60, verbose_name='Регион', blank=True, null=True)
    city = models.CharField(max_length=60, verbose_name='Город', blank=True, null=True)
    material = models.CharField(max_length=20, verbose_name='Материал стен', choices=(
        ('Кирпичный', 'Кирпичный'),
        ('Панельный', 'Панельный'),
        ('Блочный', 'Блочный'),
        ('Монолитный', 'Монолитный'),
        ('Монолитно-кирпичный', 'Монолитно-кирпичный')
    ), blank=True, null=True)
    avito_id = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True,
                                   help_text='Если описание квартир перезаписывать не надо, то лучше оставить пустым')
    alternative_description = models.TextField(verbose_name='Описание', blank=True, null=True,
                                               help_text='Если описание квартир перезаписывать не надо, то лучше оставить пустым')
    def __str__(self):
        return f"{self.complex.name} - {self.name}"
    
    class Meta(object):
        app_label = 'main'
        db_table = 'buildings'
        verbose_name = 'Дома'
        verbose_name_plural = 'Дома'

class Apartment(CreatedUpdatedMixin):
    STATUS_CHOICES = [
        ('available', 'Свободно'),
        ('reserved', 'Платная бронь'),
        ('shortReserved', 'Короткая бронь'),
        ('sold', 'Продана'),
        ('closedToSell', 'Закрыто к продажу'),
    ]
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
    floor = models.IntegerField(verbose_name='Этаж')
    str = models.IntegerField(verbose_name='Строка (для шахматки, она же этаж)')
    col = models.IntegerField(verbose_name='Колонка (для шахматки)')
    number = models.CharField(verbose_name='Номер квартиры', max_length=10)
    
    window_orientation = models.CharField(verbose_name='Вид из окна', max_length=255)
    apartment_type = models.CharField(verbose_name='Тип', max_length=255, choices=(
        ('Студия', 'Студия'), ('1-комнатная', '1-комнатная'), ('2Е – евродвушка', '2Е – евродвушка'),
        ('2-комнатная', '2-комнатная'), ('3Е – евротрешка', '3Е – евротрешка'),
        ('3-комнатная', '3-комнатная'), ('4Е - еврочетырешка', '4Е - еврочетырешка'),
        ('4-комнатная', '4-комнатная'), ('5Е – пятикомнатная евро', '5Е – пятикомнатная евро'), ('Многокомнатная', 'Многокомнатная'), ('Свободная планировка', 'Свободная планировка')
    ), default='Студия')
    area = models.FloatField(verbose_name='Площадь')
    living_square = models.FloatField(verbose_name='Жилая площадь', default=0)
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    status = models.CharField(verbose_name='Статус', max_length=15, choices=STATUS_CHOICES, default='available')
    section = models.IntegerField(verbose_name='Секция (подъезд)', null=True, default=1)
    terrace = models.BooleanField(verbose_name='Терраса', default=False)

    import_id = models.BigIntegerField(verbose_name='Import ID', default=0)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    
    kitchen_space = models.FloatField(default=0, verbose_name='Площадь кухни')
    decoration = models.CharField(verbose_name='Отделка', choices=(
        ('Без отделки', 'Без отделки'), ('Предчистовая', 'Предчистовая'), ('Чистовая', 'Чистовая')
    ), default='Без отделки', max_length=13)
    rooms = models.CharField(verbose_name='Количество комнат', default='1', choices=(
        ('Студия', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
        ('8', '8'), ('9', '9'), ('10 и более', '10 и более'), ('Своб.планировка', 'Своб.планировка')
    ))
    published = models.BooleanField(verbose_name='Публиковать в фид', default=True)
    def __str__(self):
        if self.rooms in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return f'{self.rooms}-комнатная квартира'
        return self.rooms
    def get_description(self):
        if self.description:
            return self.description
        elif self.building.description:
            return self.building.description
        elif self.building.complex and self.building.complex.description:
            return self.building.complex.description
        return ''


    def get_alternative_description(self):
        if self.description and len(self.description) > 0:
            return self.description
        elif self.building.alternative_description:
            return self.building.alternative_description
        elif self.building.complex and self.building.complex.alternative_description:
            return self.building.complex.alternative_description
        return ''

    class Meta(object):
        app_label = 'main'
        db_table = 'apartments'
        verbose_name = 'Квартиры'
        verbose_name_plural = 'Квартиры'

class ApartmentTypes(CreatedUpdatedMixin):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, related_name='apartment_types')
    name = models.CharField(verbose_name='Название', max_length=255)
    basePrice = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2)
    def __str__(self):
        return f"{self.complex.name} - {self.name}"
    
    class Meta(object):
        app_label = 'main'
        db_table = 'apartment_types'
        verbose_name = 'Типы квартир'
        verbose_name_plural = 'Типы квартир'

class VisionTypes(CreatedUpdatedMixin):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, related_name='vision_types')
    name = models.CharField(verbose_name='Название', max_length=255)
    coefficient = models.FloatField(verbose_name='Коэффициент', default=1)
    def __str__(self):
        return f"{self.complex.name} - {self.name}"
    
    class Meta(object):
        app_label = 'main'
        db_table = 'vision_types'
        verbose_name = 'Виды'
        verbose_name_plural = 'Виды'

class Coefficients(CreatedUpdatedMixin):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, related_name='coefficients')
    name = models.CharField(verbose_name='Название', max_length=255)
    coefficient = models.FloatField(verbose_name='Коэффициент', default=1)
    def __str__(self):
        return f"{self.complex.name} - {self.name}"
    
    class Meta(object):
        app_label = 'main'
        db_table = 'coefficients'
        verbose_name = 'Остальные коэфиценты'
        verbose_name_plural = 'Остальные коэфиценты'