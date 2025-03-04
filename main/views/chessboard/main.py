from main.models import Complex, Building, Apartment
from main.views import BaseView, BaseDetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from main.forms import ApartmentForm, ApartmentCreateForm
from django.urls import reverse
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

class BuildingCreateView(ListView, BaseView):
    def dispatch(self, request, *args, **kwargs):
        """ if not request.user.is_staff:
            raise PermissionDenied() """
        return super().dispatch(request, args, kwargs)

class BuildingUpdateView(SuccessMessageMixin, UpdateView, BaseView):
    """ model = MessageTemplate
    pk_url_kwarg = 'message_id'
    form_class = MessageTemplateForm
    template_name = 'management/messages/form.html'
    extra_context = {'title': 'Создание шаблона'}
    success_url = reverse_lazy('main:management-message-list')
    success_message = 'Шаблон сообщения успешно обновлен' """

    def dispatch(self, request, *args, **kwargs):
        """ if not request.user.is_staff:
            raise PermissionDenied() """
        return super().dispatch(request, args, kwargs)
class BuildingDetailView(ListView, BaseView):
    def get(self, request, building_id):
        building_instance = get_object_or_404(Building, pk=building_id)
        apartments = Apartment.objects.filter(building_id=building_id).order_by('-floor', 'col')

        floors = {}
        sections = {}
        column_range = set()

        for apartment in apartments:
            floor = apartment.floor
            col = apartment.col
            section = apartment.section
            if section not in sections:
                sections[section] = {}
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
            'sections': reversed(sections),
            'column_range': column_range
        }
        return render(request, 'chessboard/building_detail.html', context)

class ApartmentCreateView(CreateView):
    model = Apartment
    form_class = ApartmentCreateForm

    """ pk_url_kwarg = 'building_id' """
    template_name = 'chessboard/building_detail.html'
    #success_url = reverse_lazy('main:building_detail')  # Измени на нужную страницу
    success_message = "Квартира успешно создана"

   

    def form_valid(self, form):
        """Добавляем building_id и сохраняем квартиру"""
        form.instance.building = get_object_or_404(Building, id=self.kwargs.get("building_id"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Передаём building_id в контекст"""
        context = super().get_context_data(**kwargs)
        context["building_id"] = self.kwargs.get("building_id")
        return context
        context = super().get_context_data(**kwargs)
        context["building_id"] = self.kwargs.get("building_id")
        context["floor"] = self.kwargs.get("floor")
        context["col"] = self.kwargs.get("col")
        context["str"] = self.kwargs.get("str")
        return context
    def get_success_url(self):
        """После успешного создания перенаправляем на building_detail с нужным ID"""
        return reverse("main:building_detail", kwargs={"building_id": self.kwargs.get("building_id")})

class ApartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Apartment
    form_class = ApartmentForm
    pk_url_kwarg = 'apartment_id'
    template_name = 'chessboard/building_detail.html'
    success_url = reverse_lazy('main:building_detail')  # Измени на нужную страницу
    success_message = "Квартира успешно обновлена"


    def post(self, request, apartment_id, *args, **kwargs):  # Добавляем apartment_id
        apartment = get_object_or_404(Apartment, id=apartment_id)
        
        form = ApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Квартира успешно обновлена"})
        else:
            return JsonResponse({"error": form.errors}, status=400)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Если это AJAX-запрос
            return JsonResponse({'message': self.success_message, 'apartment_id': self.object.pk})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Если AJAX
            return JsonResponse({'error': 'Ошибка валидации', 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    