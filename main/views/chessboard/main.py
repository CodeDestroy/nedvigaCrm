from decimal import Decimal, DivisionByZero, InvalidOperation
from main.models import Complex, Building, Apartment, ApartmentPhoto, ApartmentTypes, VisionTypes, Coefficients
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
from main.forms import ApartmentForm, ApartmentCreateForm, BuildingCreateForm, ComplexCreateForm, ApartmentPhotoForm, ApartmentDetailForm, ComplexUpdateForm, BuildingUpdateForm,\
                        VisionTypeForm, ApartmentTypeForm, CoefficentForm
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

class ResidentialComplexUpdateView (SuccessMessageMixin, UpdateView):
    model = Complex
    form_class = ComplexUpdateForm
    pk_url_kwarg = 'complex_id'
    template_name = 'chessboard/residential_complex_update.html'
    success_message = "Жилой комплекс успешно обновлён"
    def dispatch(self, request, *args, **kwargs):
        complex_id = kwargs.get('complex_id')
        complex_obj = Complex.objects.filter(id=complex_id).first()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('main:residential_complex_update', kwargs={'complex_id': self.object.pk})  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
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
    model = Building
    form_class = BuildingUpdateForm
    pk_url_kwarg = 'building_id'
    template_name = 'chessboard/building_update.html'
    success_message = "Дом успешно обновлён"

    def get_success_url(self):
        return reverse_lazy('main:building_list', kwargs={'complex_id': self.object.complex.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
            return JsonResponse({'message': self.success_message, 'building_id': self.object.pk})
        
        return redirect(self.get_success_url())  # Перенаправляем после успешного обновления
class ApartmentListView(ListView, BaseView):
    def get(self, request, building_id):
        building_instance = get_object_or_404(Building, pk=building_id)
        apartments = Apartment.objects.filter(building_id=building_id).order_by('-floor', 'col', '-section')
        complex_instance = building_instance.complex

        # Получаем типы квартир, виды и коэффициенты для этого комплекса
        apartment_types = ApartmentTypes.objects.filter(complex=complex_instance)
        vision_types = VisionTypes.objects.filter(complex=complex_instance)
        coefficients = Coefficients.objects.filter(complex=complex_instance)

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
            'column_range': column_range,
            'apartment_types': apartment_types,
            'vision_types': vision_types,
            'coefficients': coefficients,
        }
        return render(request, 'chessboard/apartment_list.html', context)

class ApartmentCreateView(CreateView):
    model = Apartment
    form_class = ApartmentCreateForm
    template_name = 'chessboard/apartment_list.html'
    success_message = "Квартира успешно создана"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        building_id = self.kwargs.get("building_id")
        context["building_id"] = building_id
        context["building"] = get_object_or_404(Building, id=building_id)
        return context

    def form_valid(self, form):
        form.instance.building = get_object_or_404(Building, id=self.kwargs.get("building_id"))
        self.object = form.save()
        return JsonResponse({"message": "Квартира успешно создана"})

    def form_invalid(self, form):
        return JsonResponse({
            "error": "Ошибка валидации",
            "errors": form.errors,
        }, status=400)

    def get_success_url(self):
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
    

class ApartmentTypeCreateView(View):
    def get(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        form = ApartmentTypeForm()
        return render(request, 'chessboard/apartment_type_form.html', {'form': form, 'complex': complex_obj})
    
    def post(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        form = ApartmentTypeForm(request.POST)
        if form.is_valid():
            apartment_type = form.save(commit=False)
            apartment_type.complex = complex_obj
            apartment_type.save()
            return redirect(reverse('main:complex_settings', kwargs={'complex_id': complex_id}))
        return render(request, 'chessboard/apartment_type_form.html', {'form': form, 'complex': complex_obj})

class ApartmentTypeUpdateView(View):
    def get(self, request, complex_id, pk):
        apartment_type = get_object_or_404(ApartmentTypes, id=pk, complex_id=complex_id)
        form = ApartmentTypeForm(instance=apartment_type)
        return render(request, 'chessboard/apartment_type_form.html', {'form': form, 'complex': apartment_type.complex})
    
    def post(self, request, complex_id, pk):
        apartment_type = get_object_or_404(ApartmentTypes, id=pk, complex_id=complex_id)
        form = ApartmentTypeForm(request.POST, instance=apartment_type)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:complex_settings', kwargs={'complex_id': complex_id}))
        return render(request, 'apartment_type_form.html', {'form': form, 'complex': apartment_type.complex})

class ComplexSettingsView(View):
    def get(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        apartment_types = ApartmentTypes.objects.filter(complex=complex_obj)
        vision_types = VisionTypes.objects.filter(complex=complex_obj)
        coefficients = Coefficients.objects.filter(complex=complex_obj)
        
        return render(request, 'chessboard/complex_settings.html', {
            'complex': complex_obj,
            'apartment_types': apartment_types,
            'vision_types': vision_types,
            'coefficients': coefficients,
        })
    
class VisionTypeCreateView(View):
    def get(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        form = VisionTypeForm()
        return render(request, 'chessboard/vision_type_form.html', {'form': form, 'complex': complex_obj})

    def post(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        form = VisionTypeForm(request.POST)
        if form.is_valid():
            vision_type = form.save(commit=False)
            vision_type.complex = complex_obj
            vision_type.save()
            return redirect(reverse('main:complex_settings', kwargs={'complex_id': complex_id}))
        return render(request, 'chessboard/vision_type_form.html', {'form': form, 'complex': complex_obj})


class VisionTypeUpdateView(View):
    def get(self, request, complex_id, pk):
        vision_type = get_object_or_404(VisionTypes, id=pk, complex_id=complex_id)
        form = VisionTypeForm(instance=vision_type)
        return render(request, 'chessboard/vision_type_form.html', {'form': form, 'complex': vision_type.complex})

    def post(self, request, complex_id, pk):
        vision_type = get_object_or_404(VisionTypes, id=pk, complex_id=complex_id)
        form = VisionTypeForm(request.POST, instance=vision_type)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:complex_settings', kwargs={'complex_id': complex_id}))
        return render(request, 'chessboard/vision_type_form.html', {'form': form, 'complex': vision_type.complex})


class CoefficientCreateView(View):
    def get(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        form = CoefficentForm()
        return render(request, 'chessboard/coefficient_form.html', {'form': form, 'complex': complex_obj})

    def post(self, request, complex_id):
        complex_obj = get_object_or_404(Complex, id=complex_id)
        form = CoefficentForm(request.POST)
        if form.is_valid():
            coefficient = form.save(commit=False)
            coefficient.complex = complex_obj
            coefficient.save()
            return redirect(reverse('main:complex_settings', kwargs={'complex_id': complex_id}))
        return render(request, 'chessboard/coefficient_form.html', {'form': form, 'complex': complex_obj})


class CoefficientUpdateView(View):
    def get(self, request, complex_id, pk):
        coefficient = get_object_or_404(Coefficients, id=pk, complex_id=complex_id)
        form = CoefficentForm(instance=coefficient)
        return render(request, 'chessboard/coefficient_form.html', {'form': form, 'complex': coefficient.complex})

    def post(self, request, complex_id, pk):
        coefficient = get_object_or_404(Coefficients, id=pk, complex_id=complex_id)
        form = CoefficentForm(request.POST, instance=coefficient)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:complex_settings', kwargs={'complex_id': complex_id}))
        return render(request, 'chessboard/coefficient_form.html', {'form': form, 'complex': coefficient.complex})



import xlwt
from collections import defaultdict
from datetime import date
from urllib.parse import quote
STATUS_COLORS = {
    'sold': '#FF0000',
    'closedToSell': '#800080',
    'shortReserved': '#700707',
    'reserved': '#0000FF',
    'available': '#00FF00'
}

""" class ChessboardExportView(View):
    def get(self, request, building_id):
        wb = xlwt.Workbook()
        building = Building.objects.get(id=building_id)
        apartments = Apartment.objects.filter(building=building).select_related('building')

        # Группировка: section > floor > col > [apartments]
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for apt in apartments:
            data[apt.section][apt.floor][apt.col].append(apt)

        for section, floors in data.items():
            sheet = wb.add_sheet(f'Секция {section}')

            # Заголовок
            sheet.write(0, 0, 'Этаж \\ Колонка')
            col_range = set()
            for floor_cols in floors.values():
                col_range.update(floor_cols.keys())
            col_range = sorted(col_range)

            for col_index, col in enumerate(col_range):
                sheet.write(0, col_index + 1, f'Колонка {col}')

            # Этажи по строкам
            for row_index, (floor, columns) in enumerate(sorted(floors.items(), reverse=True), start=1):
                sheet.write(row_index * 2 - 1, 0, f'{floor} этаж')

                for col_index, col in enumerate(col_range):
                    apartments = columns.get(col, [])
                    if not apartments:
                        continue

                    # Только первый апартамент определяет цвет
                    style = xlwt.XFStyle()
                    if apartments:
                        color_hex = STATUS_COLORS.get(apartments[0].status, '#FFFFFF')
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = xlwt.Style.colour_map.get(
                            self.get_excel_color_name(color_hex), 1
                        )
                        style.pattern = pattern

                    text_lines = []
                    row_base = row_index * 2 - 1  # Два ряда на этаж
                    col_base = col_index * 3 + 1  # Три колонки на квартиру

                    for apt in apartments:
                        try:
                            price_per_m2 = round(apt.price / Decimal(str(apt.area)), 2)
                        except (DivisionByZero, InvalidOperation):
                            price_per_m2 = 0

                        # Цвет фона
                        bg_color = STATUS_COLORS.get(apt.status, '#FFFFFF')
                        pattern = xlwt.Pattern()
                        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                        pattern.pattern_fore_colour = xlwt.Style.colour_map.get(
                            self.get_excel_color_name(bg_color), 1
                        )
                        style = xlwt.XFStyle()
                        style.pattern = pattern

                        # Верхний ряд: номер, вид, площадь
                        sheet.write(row_base, col_base, f'№{apt.number}', style)
                        sheet.write(row_base, col_base + 1, apt.window_orientation, style)
                        sheet.write(row_base, col_base + 2, f'{apt.area} м²', style)

                        # Нижний ряд: комнаты, тип, цена
                        sheet.write(row_base + 1, col_base, f'{apt.rooms}к', style)
                        sheet.write(row_base + 1, col_base + 1, apt.apartment_type, style)
                        sheet.write(row_base + 1, col_base + 2, f'{apt.price} руб.', style)

                    #sheet.write(row_index, col_index + 1, '\n\n'.join(text_lines), style)

        # Возврат файла
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="шахматка_{building.name}.xls"'
        wb.save(response)
        return response """

"""  @staticmethod
    def get_excel_color_name(hex_color):
        
        Преобразует HEX в ближайшее имя цвета из xlwt
       
        color_map = {
            '#FF0000': 'red',
            '#00FF00': 'bright_green',
            '#0000FF': 'blue',
            '#800080': 'purple_ega',
            '#700707': 'brown'
        }
        return color_map.get(hex_color.upper(), 'white') """
class ChessboardExportView(View):
    def get(self, request, building_id):
        wb = xlwt.Workbook()
        sheet = wb.add_sheet('Шахматка')

        building = Building.objects.get(id=building_id)
        apartments = Apartment.objects.filter(building=building).select_related('building').order_by('section', '-floor', 'col', 'number')

        data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for apt in apartments:
            data[apt.section][apt.floor][apt.col].append(apt)

        section_offset = 0
        spacing = 3
        max_col_widths = defaultdict(int)

        # 1. Найдём макс. кол-во этажей в одной из секций
        max_floors_count = max(len(floors) for floors in data.values())

        for section_index, (section, floors) in enumerate(data.items()):
            start_col = section_offset

            sheet.write(0, start_col, f'Секция {section}')
            sheet.write(1, start_col, 'Этаж \\ Колонка')
            max_col_widths[start_col] = max(max_col_widths[start_col], len('Этаж \\ Колонка'))

            col_range = set()
            for floor_cols in floors.values():
                col_range.update(floor_cols.keys())
            col_range = sorted(col_range)

            for col_index, col in enumerate(col_range):
                col_pos = start_col + 1 + col_index * 3
                sheet.write(1, col_pos, f'Колонка {col}')
                max_col_widths[col_pos] = max(max_col_widths[col_pos], len(f'Колонка {col}'))

            section_floors = sorted(floors.items(), reverse=True)
            floor_offset = max_floors_count - len(section_floors)

            for row_index, (floor, columns) in enumerate(section_floors):
                base_row = (row_index + floor_offset) * 2 + 2  # +2 для заголовков

                sheet.write(base_row, start_col, f'{floor} этаж')
                max_col_widths[start_col] = max(max_col_widths[start_col], len(f'{floor} этаж'))

                for col_index, col in enumerate(col_range):
                    apartments = columns.get(col, [])
                    if not apartments:
                        continue

                    for apt in apartments:
                        try:
                            price_per_m2 = round(apt.price / Decimal(str(apt.area)), 2)
                        except (DivisionByZero, InvalidOperation):
                            price_per_m2 = 0

                        bg_color = STATUS_COLORS.get(apt.status, '#FFFFFF')
                        excel_color = self.get_excel_color_name(bg_color)
                        col_base = start_col + 1 + col_index * 3

                        def get_border_style(row_offset, col_offset):
                            font = xlwt.Font()
                            if bg_color.upper() != '#00FF00':
                                font.colour_index = xlwt.Style.colour_map['white']

                            borders = xlwt.Borders()
                            if row_offset == 0:
                                borders.top = xlwt.Borders.THIN
                            if row_offset == 1:
                                borders.bottom = xlwt.Borders.THIN
                            if col_offset == 0:
                                borders.left = xlwt.Borders.THIN
                            if col_offset == 2:
                                borders.right = xlwt.Borders.THIN

                            pattern = xlwt.Pattern()
                            pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                            pattern.pattern_fore_colour = xlwt.Style.colour_map.get(excel_color, 1)

                            style = xlwt.XFStyle()
                            style.font = font
                            style.pattern = pattern
                            style.borders = borders
                            return style

                        value_grid = [
                            [f'№{apt.number}', apt.window_orientation, f'{apt.area} м²'],
                            [f'{apt.rooms}к', apt.apartment_type, f'{apt.price} руб.']
                        ]

                        for row_offset in range(2):
                            for col_offset in range(3):
                                r = base_row + row_offset
                                c = col_base + col_offset
                                val = value_grid[row_offset][col_offset]
                                style = get_border_style(row_offset, col_offset)
                                sheet.write(r, c, val, style)
                                max_col_widths[c] = max(max_col_widths[c], len(str(val)))

            section_width = len(col_range) * 3 + 1
            section_offset += section_width + spacing

        # Ширина колонок
        for col_index, width_chars in max_col_widths.items():
            sheet.col(col_index).width = (width_chars + 2) * 256

        # Высота строк
        for row_idx in range(sheet.last_used_row + 10):
            sheet.row(row_idx).height_mismatch = True
            sheet.row(row_idx).height = 1000  # ≈ 20 pt

        today_str = date.today().strftime('%Y-%m-%d')
        raw_filename = f'шахматка_{building.name}_{today_str}.xls'
        encoded_filename = quote(raw_filename)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f"attachment; filename={encoded_filename}; filename*=UTF-8''{encoded_filename}"
        wb.save(response)
        return response

    @staticmethod
    def get_excel_color_name(hex_color):
        color_map = {
            '#FF0000': 'red',
            '#00FF00': 'bright_green',
            '#0000FF': 'blue',
            '#800080': 'purple_ega',
            '#700707': 'brown'
        }
        return color_map.get(hex_color.upper(), 'white')
