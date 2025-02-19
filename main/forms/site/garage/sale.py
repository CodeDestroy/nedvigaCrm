from django import forms

from main.forms import BaseForm


class GarageSale(BaseForm):
    Category = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Гаражи и машиноместа'}))
    OperationType = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'Продам'}))
    # Обязательные поля
    Description = forms.CharField(label='Описание', required=True,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    Address = forms.CharField(label='Адрес', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Price = forms.IntegerField(label='Цена', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    PropertyRights = forms.ChoiceField(label='Право собственности', choices=(
        ('Собственник', 'Собственник'), ('Посредник', 'Посредник')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    ObjectType = forms.ChoiceField(label='Вид объекта', choices=(
        ('Гараж', 'Гараж'), ('Машиноместо', 'Машиноместо')
    ), required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    ObjectSubtype = forms.ChoiceField(label='Тип машиноместа', choices=(
        ('Многоуровневый паркинг', 'Многоуровневый паркинг'), ('Подземный паркинг', 'Подземный паркинг'),
        ('Крытая стоянка', 'Крытая стоянка'), ('Открытая стоянка', 'Открытая стоянка'),
        ###
        ('Железобетонный', 'Железобетонный'), ('Кирпичный', 'Кирпичный'), ('Металлический', 'Металлический')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
    Secured = forms.BooleanField(label='Охрана объекта', required=True,
                                 widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    # Необязательные поля
    VideoUrl = forms.CharField(label='Ссылка на видео', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    VideoFileUrl = forms.CharField(label='Ссылка на видеофайл', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    Square = forms.ChoiceField(label='Общая площадь', required=False, choices=(
        ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'),
        ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'),
        ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('> 30', '> 30')
    ), widget=forms.Select(attrs={'class': 'form-select'}))
