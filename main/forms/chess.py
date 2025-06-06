from django import forms
from . import BaseModelForm
from ..models import Complex, Building, Apartment, VisionTypes, Coefficients, ApartmentTypes

class ApartmentForm(BaseModelForm):
    class Meta:
        model = Apartment
        fields = ('number', 'window_orientation', 'area', 'rooms', 'apartment_type', 'price', 'status', 'terrace', 'kitchen_space', 'decoration')  # Поля для редактирования
        
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'window_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'rooms': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Студия', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                ('8', '8'), ('9', '9'), ('10 и более', '10 и более'), ('Своб.планировка', 'Своб.планировка'))),
            'apartment_type': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Студия', 'Студия'), ('1-комнатная', '1-комнатная'), ('2Е – евродвушка', '2Е – евродвушка'),
                ('2-комнатная', '2-комнатная'), ('3Е – евротрешка', '3Е – евротрешка'),
                ('3-комнатная', '3-комнатная'), ('4Е - еврочетырешка', '4Е - еврочетырешка'),
                ('4-комнатная', '4-комнатная'), ('5Е – пятикомнатная евро', '5Е – пятикомнатная евро'), 
                ('Многокомнатная', 'Многокомнатная'), ('Свободная планировка', 'Свободная планировка'))),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'status': forms.Select(attrs={'class': 'form-control'}, choices=Apartment.STATUS_CHOICES),
            'terrace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kitchen_space': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'decoration': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Без отделки', 'Без отделки'), ('Предчистовая', 'Предчистовая'), ('Чистовая', 'Чистовая'))),
        }

class ApartmentDetailForm(BaseModelForm):
    class Meta:
        model = Apartment
        fields = ('number', 'window_orientation', 'area', 'rooms', 'apartment_type', 'price', 'status', 'terrace', 'kitchen_space', 'decoration', 'description', 'published' , 'living_square')  # Поля для редактирования
        
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'window_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'living_square': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'rooms': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Студия', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                ('8', '8'), ('9', '9'), ('10 и более', '10 и более'), ('Своб.планировка', 'Своб.планировка'))),
            'apartment_type': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Студия', 'Студия'), ('1-комнатная', '1-комнатная'), ('2Е – евродвушка', '2Е – евродвушка'),
                ('2-комнатная', '2-комнатная'), ('3Е – евротрешка', '3Е – евротрешка'),
                ('3-комнатная', '3-комнатная'), ('4Е - еврочетырешка', '4Е - еврочетырешка'),
                ('4-комнатная', '4-комнатная'), ('5Е – пятикомнатная евро', '5Е – пятикомнатная евро'), 
                ('Многокомнатная', 'Многокомнатная'), ('Свободная планировка', 'Свободная планировка'))),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'status': forms.Select(attrs={'class': 'form-control'}, choices=Apartment.STATUS_CHOICES),
            'terrace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kitchen_space': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'decoration': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Без отделки', 'Без отделки'), ('Предчистовая', 'Предчистовая'), ('Чистовая', 'Чистовая'))),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class ApartmentCreateForm(BaseModelForm):
    class Meta:
        model = Apartment
        fields = ('number', 'window_orientation', 'area', 'rooms', 'apartment_type', 'price', 'status', 'floor', 'str', 'col', 'section', 'terrace', 'kitchen_space', 'decoration', 'living_square')  # Поля для редактирования

        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'window_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'living_square': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'rooms': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Студия', 'Студия'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                ('8', '8'), ('9', '9'), ('10 и более', '10 и более'), ('Своб.планировка', 'Своб.планировка'))),
            'apartment_type': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Студия', 'Студия'), ('1-комнатная', '1-комнатная'), ('2Е – евродвушка', '2Е – евродвушка'),
                ('2-комнатная', '2-комнатная'), ('3Е – евротрешка', '3Е – евротрешка'),
                ('3-комнатная', '3-комнатная'), ('4Е - еврочетырешка', '4Е - еврочетырешка'),
                ('4-комнатная', '4-комнатная'), ('5Е – пятикомнатная евро', '5Е – пятикомнатная евро'), 
                ('Многокомнатная', 'Многокомнатная'), ('Свободная планировка', 'Свободная планировка'))),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
            'status': forms.Select(attrs={'class': 'form-control'}, choices=Apartment.STATUS_CHOICES),
            'floor': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'str': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'col': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'section': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
            'terrace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kitchen_space': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'decoration': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('Без отделки', 'Без отделки'), ('Предчистовая', 'Предчистовая'), ('Чистовая', 'Чистовая'))),
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
        
class BuildingUpdateForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('name', 'total_floors', 'total_apartments', 'address', 'region', 'city', 'material', 'description', 'alternative_description', 'avito_id')
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_apartments': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'alternative_description': forms.Textarea(attrs={'class': 'form-control'}),
            'avito_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ComplexCreateForm(BaseModelForm):
    class Meta:
        model = Complex
        fields = ('name', 'description')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),  
        }

class ComplexUpdateForm(BaseModelForm):
    class Meta:
        model = Complex
        fields = ('name', 'description', 'address', 'region', 'city', 'alternative_description', 'avito_id')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),  
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_description': forms.Textarea(attrs={'class': 'form-control'}),
            'avito_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VisionTypeForm(BaseModelForm):
    class Meta:
        model = VisionTypes
        fields = ('name', 'coefficient')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
        }
class ApartmentTypeForm(BaseModelForm):
    class Meta:
        model = ApartmentTypes
        fields = ('name', 'basePrice')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'basePrice': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),  
        } 

class CoefficentForm(BaseModelForm):
    class Meta:
        model = Coefficients
        fields = ('name', 'coefficient')  # Поля для редактирования

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),  
        }  