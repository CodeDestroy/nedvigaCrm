""" from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import TaskForm, CommentForm, ShowingForm, MoneyForm, MortgageForm
from main.forms.deal import DealAdminForm, DealUserForm"""
from main.models import Complex, Building, Apartment
from main.views import BaseView, BaseDetailView 


""" class ChessListView(ListView, BaseView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            leads = Lead.objects.distinct().filter(
                responsible=request.user, whatsappmessage__created_at__gte=datetime.date.today() - timedelta(days=10))
        else:
            leads = Lead.objects.distinct().filter(
                whatsappmessage__created_at__gte=datetime.date.today() - timedelta(days=10))
        return render(request, 'chess/page.html', {'title': 'Шахматка'}) """

from django.conf import settings
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView

""" class ResidentialComplex(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Building(models.Model):
    complex = models.ForeignKey(ResidentialComplex, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=255)
    total_floors = models.IntegerField()
    total_apartments = models.IntegerField()

    def __str__(self):
        return f"{self.complex.name} - {self.name}"

class Apartment(models.Model):
    STATUS_CHOICES = [
        ('available', 'В продаже'),
        ('sold', 'Продана')
    ]
    
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
    floor = models.IntegerField()
    number = models.CharField(max_length=10)
    rooms = models.IntegerField()
    window_orientation = models.CharField(max_length=255)
    apartment_type = models.CharField(max_length=255)
    area = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Квартира {self.number} - {self.building.name}"
 """
# Представления
class ResidentialComplexListView(ListView, BaseView):
    def get(self, request):
        complexes = Complex.objects.all()
        return render(request, 'chessboard/residential_complex_list.html', {'complexes': complexes})

class ResidentialComplexDetailView(ListView, BaseView):
    def get(self, request, complex_id):
        complex_instance = get_object_or_404(Complex, pk=complex_id)
        buildings = Building.objects.filter(complex_id=complex_id)

        context = {
            'complex': complex_instance,
            'buildings': buildings
        }
        return render(request, 'chessboard/residential_complex_detail.html', context)


class BuildingDetailView(View):
    def get(self, request, building_id):
        building_instance = get_object_or_404(Building, pk=building_id)
        apartments = Apartment.objects.filter(building_id=building_id).order_by('-floor', 'col')

        floors = {}
        column_range = set()

        for apartment in apartments:
            floor = apartment.floor
            col = apartment.col

            if floor not in floors:
                floors[floor] = {}
            if col not in floors[floor]:
                floors[floor][col] = []
            
            floors[floor][col].append(apartment)
            column_range.add(col)

        column_range = sorted(column_range)  # Сортируем колонки для правильного отображения в таблице

        context = {
            'building': building_instance,
            'floors': floors,
            'column_range': column_range
        }
        return render(request, 'chessboard/building_detail.html', context)

    
    """ model = Building
    template_name = 'building_detail.html'
    context_object_name = 'building'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем все квартиры данного дома и группируем их по этажам
        apartments = Apartment.objects.filter(building=self.object).order_by('-floor')
        floors = {}
        for apartment in apartments:
            if apartment.floor not in floors:
                floors[apartment.floor] = []
            floors[apartment.floor].append(apartment)
        
        context['floors'] = floors
        return context """
    """ def get(self, request, *args, **kwargs):
        building = get_object_or_404(Building, pk=kwargs.get('building_id'))
        return render(request, 'chessboard/building_detail.html', {'building': building}) """
