from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, FormView

from main.forms.site import *
from main.models import User
from main.models.site import BuyObject, ObjectPhoto, ObjectField
from main.views import BaseView, BaseDetailView

# Булевые поля
bool_fields = ['WeekendWork', 'Working24Hours', 'PriceWithVAT', 'SmokingAllowed', 'ChildrenAllowed', 'PetsAllowed',
               'PartiesAllowed', 'Documents', 'Secured']
# Мультивыборные поля
multi_fields = [
    'RoomType', 'BalconyOrLoggiaMulti', 'LeaseAppliances', 'Parking', 'BathroomMulti', 'NDAdditionally',
    'Furniture', 'LeaseMultimedia', 'LeaseComfort', 'LeaseAdditionally', 'ParkingType', 'ParkingAdditionally',
    'LeaseComfortMulti', 'Layout', 'AdditionalObjectTypes', 'EntranceAdditionally', 'FloorAdditionally',
    'SquareAdditionally', 'KeyConveniences', 'ConvenienceIncluded', 'AvailableHardware', 'FoodAndDrinks',
    'AvailableService', 'AdditionalFacilities', 'RentalHolidays', 'LeasePriceOptions', 'PowerGridAdditionally',
    'CurrentTenants', 'SaleOptions', 'ViewFromWindows', 'Courtyard', 'RepairAdditionally', 'RenovationProgram',
    'InHouse', 'SSAdditionally', 'LandAdditionally', 'HouseAdditionally', 'HouseServices', 'TransportAccessibility',
    'Infrastructure', 'HeatingType'
]


class ExclusiveListView(ListView, BaseView):
    model = BuyObject
    context_object_name = 'exclusives'
    paginate_by = settings.PAGINATION
    template_name = 'exclusive/list.html'
    extra_context = {
        'title': 'Список эксклюзивов',
        'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
    }

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('objectfield_set')
        if user := self.request.GET.get('user'):
            qs = qs.filter(user_id=user)
        if category := self.request.GET.get('category'):
            qs = qs.filter(objectfield__name='Category', objectfield__value=category)
        if operation := self.request.GET.get('operation'):
            qs = qs.filter(objectfield__name='OperationType', objectfield__value=operation)
        return qs


class ExclusiveFormView(BaseView, FormView):
    template_name = 'exclusive/form.html'
    instance = None
    extra_context = {'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)}

    def get_form_class(self):
        if exclusive_id := self.kwargs.get('exclusive_id'):
            self.instance = BuyObject.objects.get(pk=exclusive_id)
            fields = self.instance.fields_for_list()
            match fields['category']:
                case 'Квартиры':
                    if fields['operation'] == 'Продам':
                        if market_type := self.instance.objectfield_set.filter(name='MarketType'):
                            market_type = market_type.first().value
                            if market_type == 'Новостройка':
                                return FlatSaleNew
                            elif market_type == 'Вторичка':
                                return FlatSaleOld
                    else:
                        return FlatLease
                case 'Дома, дачи, коттеджи':
                    if fields['operation'] == 'Сдам':
                        if lease_type := self.instance.objectfield_set.filter(name='LeaseType'):
                            lease_type = lease_type.first().value
                            if lease_type == 'Посуточно':
                                return HouseLeaseDay
                            elif lease_type == 'На длительный срок':
                                return HouseLease
                    else:
                        return HouseSale
                case 'Земельные участки':
                    return LandSale if fields['operation'] == 'Продам' else LandLease
                case 'Комнаты':
                    return RoomSale if fields['operation'] == 'Продам' else RoomLease
                case 'Коммерческая недвижимость':
                    return CommerceSale if fields['operation'] == 'Продам' else CommerceLease
                case 'Гаражи и машиноместа':
                    return GarageSale if fields['operation'] == 'Продам' else GarageLease
            messages.error(self.request, 'Нет формы для данной категории объявлений')
            return redirect('main:exclusive-list')
        return self.form_class

    def get_initial(self):
        initial = super().get_initial()
        if self.instance:
            for field in self.instance.objectfield_set.all():
                initial[field.name] = field.value
        return initial

    def form_valid(self, form):
        try:
            create = False
            if not self.instance:
                self.instance = BuyObject()
                self.instance.user = self.request.user
                self.instance.save()
                create = True
            if self.request.POST['user']:
                try:
                    self.instance.user = User.objects.get(pk=self.request.POST['user'])
                except User.DoesNotExist:
                    messages.warning(self.request, 'Выбранный пользователь не найден')
            existed_fields = []
            for key in form.cleaned_data:
                if form.cleaned_data[key]:
                    try:
                        field = ObjectField.objects.get(obj=self.instance, name=key)
                    except ObjectField.DoesNotExist:
                        field = ObjectField()
                        field.obj = self.instance
                        field.name = key
                    if key in bool_fields:
                        field.value = 'Да' if form.cleaned_data[key] else 'Нет'
                    elif key in multi_fields:
                        field.value = '|'.join(form.cleaned_data[key])
                    else:
                        field.value = form.cleaned_data[key]
                    field.save()
                    existed_fields.append(field.pk)
            # Удаляем поля, которые удалены из формы
            ObjectField.objects.filter(obj=self.instance).exclude(pk__in=existed_fields).delete()
            # Удаляем лишние фотки
            photos = ObjectPhoto.objects.filter(obj=self.instance)
            if existed_photos := self.request.POST.getlist('photo'):
                photos = photos.exclude(pk__in=existed_photos)
            photos.delete()
            # Сохраняем фотки
            for file in self.request.FILES.getlist('photos'):
                ph = ObjectPhoto()
                ph.obj = self.instance
                ph.photo.save(file.name, file)
                ph.save()
            if create:
                messages.success(self.request, 'Эксклюзив успешно создан')
            else:
                messages.warning(self.request, 'Эксклюзив успешно обновлен')
            return redirect('main:exclusive-page', exclusive_id=self.instance.pk)
        except BaseException:
            return BaseException


class ExclusivePageView(BaseDetailView):
    model = BuyObject
    pk_url_kwarg = 'exclusive_id'
    template_name = 'exclusive/page.html'
    context_object_name = 'exclusive'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Эксклюзив #{self.object.pk}'
        context['admin_links'] = [{
            'url': reverse('main:exclusive-publish', kwargs={'exclusive_id': self.object.pk}),
            'text': '<i class="ti ti-eye-off icon"></i> Снять с публикации' if self.object.published else '<i class="ti ti-eye icon"></i> Опубликовать',
            'class': 'btn btn-warning' if self.object.published else 'btn btn-success',
        }, {
            'url': reverse('main:exclusive-delete', kwargs={'exclusive_id': self.object.pk}),
            'text': '<i class="ti ti-trash icon"></i>', 'class': 'btn btn-danger btn-icon',
            'get': reverse('main:modal-exclusive-delete', kwargs={'exclusive_id': self.object.pk})
        }]
        initial_values = self.object.objectfield_set.all()
        d = {}
        for v in initial_values:
            if v.name in multi_fields:
                d[v.name] = v.value.split('|')
            elif v.name in bool_fields and v.value == 'Да':
                d[v.name] = True
            elif v.name in bool_fields and v.value == 'Нет':
                d[v.name] = False
            else:
                d[v.name] = v.value
        fields = self.object.fields_for_list()
        match fields['category']:
            case 'Квартиры':
                if fields['operation'] == 'Продам':
                    if market_type := self.object.objectfield_set.filter(name='MarketType'):
                        market_type = market_type.first().value
                        if market_type == 'Новостройка':
                            context['form'] = FlatSaleNew(initial=d)
                        elif market_type == 'Вторичка':
                            context['form'] = FlatSaleOld(initial=d)
                else:
                    context['form'] = FlatLease(initial=d)
            case 'Дома, дачи, коттеджи':
                if fields['operation'] == 'Сдам':
                    if lease_type := self.object.objectfield_set.filter(name='LeaseType'):
                        lease_type = lease_type.first().value
                        if lease_type == 'Посуточно':
                            context['form'] = HouseLeaseDay(initial=d)
                        elif lease_type == 'На длительный срок':
                            context['form'] = HouseLease(initial=d)
                else:
                    context['form'] = HouseSale(initial=d)
            case 'Земельные участки':
                context['form'] = LandSale(initial=d) if fields['operation'] == 'Продам' else LandLease(initial=d)
            case 'Комнаты':
                context['form'] = RoomSale(initial=d) if fields['operation'] == 'Продам' else RoomLease(initial=d)
            case 'Коммерческая недвижимость':
                context['form'] = CommerceSale(initial=d) if fields['operation'] == 'Продам' else CommerceLease(initial=d)
            case 'Гаражи и машиноместа':
                context['form'] = GarageSale(initial=d) if fields['operation'] == 'Продам' else GarageLease(initial=d)
        context['photos'] = ObjectPhoto.objects.filter(obj=self.object)
        context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def get_queryset(self):
        return super().get_queryset().prefetch_related('objectfield_set', 'objectphoto_set', 'objectstat_set')


class ExclusiveDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        get_object_or_404(BuyObject, pk=kwargs.get('exclusive_id')).delete()
        messages.error(request, 'Эксклюзив успешно удален')
        return redirect('main:exclusive-list')


class ExclusivePublish(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(BuyObject, pk=kwargs.get('exclusive_id'))
        obj.published = not obj.published
        obj.save()
        messages.success(self.request, 'Объект опубликован' if obj.published else 'Объект не опубликован')
        return redirect('main:exclusive-page', exclusive_id=obj.pk)
