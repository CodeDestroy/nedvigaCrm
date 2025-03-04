from django import forms
from . import BaseModelForm
from ..models import Complex, Building, Apartment

class ApartmentForm(BaseModelForm):
    class Meta:
        model = Apartment
        fields = ('number', 'window_orientation', 'area', 'rooms', 'apartment_type', 'price', 'status')  # Поля для редактирования

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'window_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),  
            'apartment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'status': forms.Select(attrs={'class': 'form-control'}, choices=Apartment.STATUS_CHOICES),

            #building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
            #floor = models.IntegerField()
            #str = models.IntegerField()
            #col = models.IntegerField()
            #number = models.CharField(max_length=10)
            #rooms = models.IntegerField()
            #window_orientation = models.CharField(max_length=255)
            #apartment_type = models.CharField(max_length=255)
            #area = models.FloatField()
            #price = models.DecimalField(max_digits=12, decimal_places=2)
            #status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
            #section = models.IntegerField(null=True, default=1)
        }
class ApartmentCreateForm(BaseModelForm):
    class Meta:
        model = Apartment
        fields = ('number', 'window_orientation', 'area', 'rooms', 'apartment_type', 'price', 'status', 'floor', 'str', 'col', 'section')  # Поля для редактирования

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'window_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),  
            'apartment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'status': forms.Select(attrs={'class': 'form-control'}, choices=Apartment.STATUS_CHOICES),
            'floor': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'str': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'col': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'section': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),

            #building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
            #floor = models.IntegerField()
            #str = models.IntegerField()
            #col = models.IntegerField()
            #number = models.CharField(max_length=10)
            #rooms = models.IntegerField()
            #window_orientation = models.CharField(max_length=255)
            #apartment_type = models.CharField(max_length=255)
            #area = models.FloatField()
            #price = models.DecimalField(max_digits=12, decimal_places=2)
            #status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
            #section = models.IntegerField(null=True, default=1)
        }
class BuildingCreateForm(BaseModelForm):
    class Meta:
        model = Building
        fields = ('name', 'total_floors', 'total_apartments')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),  
            'total_apartments': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
        }
class ComplexCreateForm(BaseModelForm):
    class Meta:
        model = Complex
        fields = ('name', 'description')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),  
        }