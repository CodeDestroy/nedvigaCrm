from django.conf import settings
from django.db import models
from django.urls import reverse

from . import CreatedUpdatedMixin

class Complex(CreatedUpdatedMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    """ image = models.ImageField(upload_to='complex_images/', null=True, blank=True) """

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

    def __str__(self):
        return f"{self.complex.name} - {self.name}"
    
    class Meta(object):
        app_label = 'main'
        db_table = 'buildings'
        verbose_name = 'Дома'
        verbose_name_plural = 'Дома'

class Apartment(CreatedUpdatedMixin):
    STATUS_CHOICES = [
        ('available', 'В продаже'),
        ('sold', 'Продана')
    ]
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
    floor = models.IntegerField()
    str = models.IntegerField()
    col = models.IntegerField()
    number = models.CharField(max_length=10)
    rooms = models.IntegerField()
    window_orientation = models.CharField(max_length=255)
    apartment_type = models.CharField(max_length=255)
    area = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    section = models.IntegerField(null=True, default=1)
    def __str__(self):
        return f"Квартира {self.number} - {self.building.name}"
    
    class Meta(object):
        app_label = 'main'
        db_table = 'apartments'
        verbose_name = 'Квартиры'
        verbose_name_plural = 'Квартиры'




    
