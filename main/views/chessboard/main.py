from main.models import Complex, Building, Apartment, ApartmentPhoto
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
from main.forms import ApartmentForm, ApartmentCreateForm, BuildingCreateForm, ComplexCreateForm, ApartmentPhotoForm, ApartmentDetailForm
from django.urls import reverse

class ResidentialComplexListView(ListView, BaseView):
    def get(self, request):
        complexes = Complex.objects.all()
        return render(request, 'chessboard/residential_complex_list.html', {'complexes': complexes})
class ResidentialComplexCreateView(CreateView):
    model = Complex
    form_class = ComplexCreateForm
    template_name = "chessboard/residential_complex_list.html"
    success_url = reverse_lazy('main:residential_complex_list')
    success_message = "Жилой комплекс успешно создан"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        complex_instance = form.save(commit=False)
        complex_instance.created_by = self.request.user
        complex_instance.updated_by = self.request.user
        complex_instance.save()
        return super().form_valid(form)


class BuildingListView(ListView, BaseView):
    def get(self, request, complex_id):
        complex_instance = get_object_or_404(Complex, pk=complex_id)
        buildings = Building.objects.filter(complex_id=complex_id)

        context = {
            'complex': complex_instance,
            'buildings': buildings
        }
        return render(request, 'chessboard/building_list.html', context)
class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingCreateForm
    template_name = "chessboard/building_list.html"
    success_message = "Дом успешно создан"

    def form_valid(self, form):
        """Добавляем complex_id и сохраняем дом"""
        complex_id = self.request.POST.get("complex_id")
        form.instance.complex = get_object_or_404(Complex, id=complex_id)
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправляем на страницу комплекса после создания дома"""
        return reverse("main:building_list", kwargs={"complex_id": self.object.complex.id})



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
class ApartmentListView(ListView, BaseView):
    def get(self, request, building_id):
        building_instance = get_object_or_404(Building, pk=building_id)
        apartments = Apartment.objects.filter(building_id=building_id).order_by('-floor', 'col', '-section')

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
        return render(request, 'chessboard/apartment_list.html', context)

class ApartmentCreateView(CreateView):
    model = Apartment
    form_class = ApartmentCreateForm

    """ pk_url_kwarg = 'building_id' """
    template_name = 'chessboard/apartment_list.html'
    #success_url = reverse_lazy('main:apartment_list')  # Измени на нужную страницу
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
    def get_success_url(self):
        """После успешного создания перенаправляем на apartment_list с нужным ID"""
        return reverse("main:apartment_list", kwargs={"building_id": self.kwargs.get("building_id")})

class ApartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Apartment
    form_class = ApartmentForm
    pk_url_kwarg = 'apartment_id'
    template_name = 'chessboard/apartment_list.html'
    success_url = reverse_lazy('main:apartment_list')  # Измени на нужную страницу
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
class ApartmentDetailUpdateView(SuccessMessageMixin, UpdateView):
    model = Apartment
    form_class = ApartmentDetailForm
    pk_url_kwarg = 'apartment_id'
    template_name = 'chessboard/apartment_detail.html'
    success_message = "Квартира успешно обновлена"

    def get_success_url(self):
        return reverse('main:apartment_detail', kwargs={
            'building_id': self.object.building.id,  # Добавляем building_id
            'apartment_id': self.object.pk
        })
    def post(self, request, apartment_id, *args, **kwargs):
        apartment = get_object_or_404(Apartment, id=apartment_id)
        form = ApartmentDetailForm(request.POST, instance=apartment)

        if form.is_valid():
            apartment = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX-запрос
                return JsonResponse({"message": self.success_message, "apartment_id": apartment.pk})
            return super().form_valid(form)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX
            return JsonResponse({"error": form.errors}, status=400)
        return super().form_invalid(form)
    
class ApartmentDetailView(BaseDetailView):
    model = Apartment
    pk_url_kwarg = 'apartment_id'
    template_name = 'chessboard/apartment_detail.html'
    context_object_name = 'apartment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        context['form'] = ApartmentDetailForm(instance=self.object)
        context['photos'] = self.object.apartmentphoto_set.all().order_by('sort')  # Получаем все фото
        context['photo_upload_form'] = ApartmentPhotoForm()  # Форма для загрузки фото
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('building', 'created_by', 'updated_by')

class ApartmentPhotoUploadView(View):
    def dispatch(self, request, *args, **kwargs):
        """Позволяет передавать building_id в методы"""
        self.building_id = kwargs.get('building_id')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, building_id, apartment_id, *args, **kwargs):
        apartment = get_object_or_404(Apartment, id=apartment_id)

        if 'photo' not in request.FILES:
            return JsonResponse({'error': 'Файл не найден'}, status=400)

        photo = request.FILES['photo']
        ApartmentPhoto.objects.create(apartment=apartment, photo=photo)

        return JsonResponse({'message': 'Фото успешно загружено'})