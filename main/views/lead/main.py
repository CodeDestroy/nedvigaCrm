import xlrd
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import QuestionsForm, TaskForm, PassportForm, LeadSourceForm, ShowingForm
from main.forms.lead import LeadAdminForm, LeadUserForm
from main.models import Lead, Questions, Passport, LeadSource, Stage, Comment, Source, User, Notification
from main.views import BaseView, BaseDetailView


class BaseLeadListView(ListView, BaseView):
    model = Lead
    context_object_name = 'leads'
    paginate_by = settings.PAGINATION

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:lead-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
            'class': 'btn btn-success',  # 'get': reverse('cabinet:project-modals-create')
        }]
        return context

    # При изменении фильтров, поменяй и отчет
    def get_queryset(self):
        qs = super().get_queryset().distinct('pk')
        if user := self.request.GET.getlist('user'):
            qs = qs.filter(responsible__pk__in=user)
        if partner := self.request.GET.get('partner'):
            qs = qs.filter(partner__pk=partner)
        if text := self.request.GET.get('text'):
            qs = qs.filter(Q(surname__icontains=text) | Q(name__icontains=text) | Q(phone__icontains=text) |
                           Q(partner__surname__icontains=text) | Q(partner__name__icontains=text) |
                           Q(partner__phone__icontains=text) | Q(client__surname__icontains=text) |
                           Q(client__name__icontains=text) | Q(client__phone__icontains=text) |
                           Q(pk__in=Comment.objects.filter(text__icontains=text, type='lead').values_list('item_id',
                                                                                                          flat=True)))
        if self.request.GET.get('reserve'):
            qs = qs.filter(deal__reserved__isnull=False)
        if self.request.GET.get('spam'):
            qs = qs.exclude(warm__in=['not_client', 'not_call'])
        if self.request.GET.get('no_source'):
            qs = qs.filter(leadsource__isnull=True)
        if self.request.GET.get('no_warm'):
            qs = qs.filter(warm=None)
        if source := self.request.GET.getlist('source'):
            qs = qs.filter(leadsource__source__pk__in=source)
        if warm := self.request.GET.getlist('warm'):
            qs = qs.filter(warm__in=warm)
        if processed := self.request.GET.getlist('processed'):
            qs = qs.filter(processed__in=processed)
        if paytype := self.request.GET.get('paytype'):
            qs = qs.filter(Q(deal__paytype=paytype) | Q(questions__payment=paytype))
        if frm := self.request.GET.get('from'):
            qs = qs.filter(deal__frm=frm)
        if stage := self.request.GET.get('stage'):
            qs = qs.filter(deal__stage__pk=stage)
        if decoration := self.request.GET.get('decoration'):
            qs = qs.filter(questions__decoration=decoration)
        if developer := self.request.GET.get('developer'):
            qs = qs.filter(questions__developer=developer)
        if marital := self.request.GET.get('marital'):
            qs = qs.filter(questions__marital_status=marital)
        if purpose := self.request.GET.get('purpose'):
            qs = qs.filter(questions__purpose=purpose)
        if birth := self.request.GET.get('birth'):
            qs = qs.filter(questions__birth_date=datetime.strptime(birth, '%Y-%m-%d').date())
        if reserved := self.request.GET.get('reserved'):
            qs = qs.filter(deal__reserved=datetime.strptime(reserved, '%Y-%m-%d').date())
        from_in = self.request.GET.get('from_in')
        to_in = self.request.GET.get('to_in')
        if from_in and to_in:
            qs = qs.filter(leadsource__created_at__date__gte=datetime.strptime(from_in, '%Y-%m-%d').date(),
                           leadsource__created_at__date__lte=datetime.strptime(to_in, '%Y-%m-%d').date())
        elif from_in:
            qs = qs.filter(leadsource__created_at__date=datetime.strptime(from_in, '%Y-%m-%d').date())
        elif to_in:
            qs = qs.filter(leadsource__created_at__date=datetime.strptime(to_in, '%Y-%m-%d').date())
        if created_at := self.request.GET.get('created_at'):
            qs = qs.filter(created_at__date=datetime.strptime(created_at, '%Y-%m-%d').date())
        if self.request.GET.get('deferred'):
            qs = qs.filter(deferred=True)
        return qs


class LeadListView(BaseLeadListView):
    template_name = 'lead/list.html'
    extra_context = {'title': 'Активные контакты', 'users': User.objects.filter(
        Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)}

    # При изменении фильтров, поменяй и отчет
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False) #processed__in=['redo', 'not']


class LeadMoneyView(ListView, BaseView):
    model = Lead
    context_object_name = 'leads'
    template_name = 'lead/money.html'
    extra_context = {'title': 'Клиентская сеть'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stages'] = Stage.objects.all()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(pk__in=Lead.objects.values_list('client', flat=True))


class LeadListDeletedView(BaseLeadListView):
    template_name = 'lead/deleted.html'
    extra_context = {'title': 'Удаленные контакты'}

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class LeadCreateView(CreateView, BaseView):
    model = Lead
    form_class = LeadAdminForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание контакта'}

    def get_form(self, form_class=None):
        if not self.request.user.is_staff:
            return LeadUserForm(**self.get_form_kwargs())
        return LeadAdminForm(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)
        try:
            lead = Lead.objects.get(phone=instance.phone)
            messages.error(self.request, 'Контакт с указанным номером телефона уже существует')
            return redirect(lead.get_absolute_url())
        except Lead.DoesNotExist:
            instance.first_manager = self.request.user
            instance.responsible = self.request.user
            instance.created_by = self.request.user
            instance.save()
            messages.success(self.request, 'Контакт успешно создан')
            return redirect(self.request.POST.get('next', instance.get_absolute_url()))


class LeadUpdateView(UpdateView, BaseView):
    model = Lead
    form_class = LeadAdminForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'lead_id'
    extra_context = {'title': 'Обновление контакта'}

    def get_form(self, form_class=None):
        if not self.request.user.is_staff:
            return LeadUserForm(**self.get_form_kwargs())
        return LeadAdminForm(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Получаем исходное значение ответственного из базы данных
        original_instance = Lead.objects.get(pk=instance.pk)
        previous_responsible = original_instance.responsible

        # Если у контакта нет ответственного, значит тот, кто его редактирует сейчас и есть ответственный
        if not instance.responsible:
            instance.responsible = self.request.user
            if deals := instance.deal_set.all():
                deal = deals.last()
                if not deal.responsible:
                    deal.responsible = self.request.user
                deal.save()
        instance.updated_by = self.request.user
        if instance.deferred:
            instance.warm = 'cold'
        instance.save()
        
        # Если изменился ответственный, создаем уведомление
        if previous_responsible != instance.responsible:
            Notification.objects.create(
                name="Вам передан контакт",
                text="Не забудьте посмотреть",
                priority='danger',
                user=instance.responsible,  # Уведомление направляем новому ответственному
                type='lead',
                item_id=instance.pk,
                created_by=self.request.user
            )


        if instance.warm in ['not_client', 'not_call'] or instance.spam:
            if deals := instance.deal_set.all():
                deal = deals.last()
                deal.spam = True
                deal.save()
        messages.warning(self.request, 'Контакт успешно обновлен')
        return redirect(self.request.POST.get('next', instance.get_absolute_url()))


class LeadPageView(BaseDetailView):
    model = Lead
    pk_url_kwarg = 'lead_id'
    template_name = 'lead/page.html'
    context_object_name = 'lead'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        context['admin_links'] = [{
            'url': reverse('main:lead-task-create', kwargs={'lead_id': self.object.pk}),
            'text': '<i class="ti ti-plus icon"></i> Добавить задачу', 'class': 'btn btn-success',
            'get': reverse('main:modal-lead-task-create', kwargs={'lead_id': self.object.pk})
        }, {
            'url': reverse('main:lead-showing-create', kwargs={'lead_id': self.object.pk}),
            'text': '<i class="ti ti-plus icon"></i> Добавить показ', 'class': 'btn btn-teal',
            'get': reverse('main:modal-lead-showing-create', kwargs={'lead_id': self.object.pk})
        }]
        if self.request.user.is_staff:
            context['form'] = LeadAdminForm(instance=self.object)
        else:
            context['form'] = LeadUserForm(instance=self.object)
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('first_manager', 'questions', 'passport')


class LeadSourceCreateView(CreateView, BaseView):
    model = LeadSource
    form_class = LeadSourceForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание источника'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.lead = get_object_or_404(Lead, pk=self.kwargs.get('lead_id'))
        instance.save()
        messages.success(self.request, 'Источник успешно добавлен к контакту')
        return HttpResponseRedirect(instance.lead.get_absolute_url())


class LeadSourceDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        lead_source = get_object_or_404(LeadSource, pk=kwargs.get('ls_id'))
        url = lead_source.lead.get_absolute_url()
        lead_source.delete()
        messages.error(request, 'Источник успешно удален из контакта')
        return HttpResponseRedirect(url)


class LeadQuestionsCreateView(CreateView, BaseView):
    model = Questions
    form_class = QuestionsForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание вопросов'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.lead = get_object_or_404(Lead, pk=self.kwargs.get('lead_id'))
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Вопросы успешно заполнены')
        return redirect(instance.lead.get_absolute_url())


class LeadQuestionsUpdateView(UpdateView, BaseView):
    model = Questions
    form_class = QuestionsForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'questions_id'
    extra_context = {'title': 'Обновление вопросов'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        instance.save()
        messages.warning(self.request, 'Вопросы успешно обновлены')
        return redirect(instance.lead.get_absolute_url())


class LeadPassportCreateView(CreateView, BaseView):
    model = Passport
    form_class = PassportForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание паспорта'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.lead = get_object_or_404(Lead, pk=self.kwargs.get('lead_id'))
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Паспорт успешно заполнен')
        return HttpResponseRedirect(instance.lead.get_absolute_url())


class LeadPassportUpdateView(UpdateView, BaseView):
    model = Passport
    form_class = PassportForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'passport_id'
    extra_context = {'title': 'Обновление паспорта'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        instance.save()
        messages.warning(self.request, 'Вопросы успешно обновлены')
        return HttpResponseRedirect(instance.lead.get_absolute_url())


class LeadTaskCreateView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'task/form.html', {
            'title': 'Создание задачи', 'lead_id': self.kwargs.get('lead_id'), 'form': TaskForm()})


class LeadShowingCreateView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'showing/form.html', {
            'title': 'Создание показа', 'lead_id': self.kwargs.get('lead_id'), 'form': ShowingForm()})


class LeadDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs.get('lead_id'))
        lead.is_deleted = True
        lead.save()
        messages.error(self.request, 'Контакт успешно удален')
        return redirect('main:lead-list-deleted')


class LeadUnassembledView(ListView, BaseView):
    model = Lead
    context_object_name = 'leads'
    paginate_by = settings.PAGINATION
    template_name = 'lead/unassembled.html'
    extra_context = {'title': 'Неразобранные контакты',
                     'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)}

    def get_queryset(self):
        return super().get_queryset().filter(processed__in=['redo', 'not'], is_deleted=False) #is_deleted=False


class LeadUploadView(BaseView):
    def post(self, request, *args, **kwargs):
        
        if 'excel' in request.FILES:
            leads_count = 0
            # if os.path.splitext(request.FILES['excel'].name)[1] == '.xls':
            wb = xlrd.open_workbook(file_contents=request.FILES['excel'].read())
            sh = wb.sheet_by_index(0)
            for rx in range(1, sh.nrows):
                if sh.cell_type(rx, 16) != xlrd.XL_CELL_EMPTY:
                    try:
                        phone_value = sh.cell_value(rx, 16)
                        phone_number = int(phone_value)
                        # Если это число (float/int) — просто преобразуем
                        if isinstance(phone_value, (int, float)):
                            phone_number = int(phone_value)
                            Lead.objects.get(phone=phone_number)
                        # Если это строка, проверяем, состоит ли она только из цифр
                        elif isinstance(phone_value, str) and phone_value.isdigit():
                            phone_number = int(phone_value)
                            Lead.objects.get(phone=phone_number)
                        # Если не число и не строка с цифрами — ошибка
                        else:
                            messages.error(request, f"Ошибка: в ячейке {rx},16 неверный формат ({phone_value})")
                    except Lead.DoesNotExist:
                        leads_count += 1
                        lead = Lead()
                        lead.phone = f'{int(sh.cell_value(rx, 16))}'
                        lead.surname = f"{sh.cell_value(rx, 14)}"
                        lead.save()
                        LeadSource.objects.create(lead=lead,
                                                  source=Source.objects.get_or_create(name='База для обзвона')[0])
                        
                        comment_text = (
                            f"sourse: {sh.cell_value(rx, 1)}\n"  # Колонка B
                            f"city: {sh.cell_value(rx, 2)}\n"  # Колонка C
                            f"district {sh.cell_value(rx, 3)}\n"  # Колонка D
                            f"building: {sh.cell_value(rx, 6)}\n"  # Колонка G
                            f"location: {sh.cell_value(rx, 7)}\n"  # Колонка H
                            f"purpose: {sh.cell_value(rx, 8)}\n"  # Колонка I
                            f"beds: {sh.cell_value(rx, 10)}\n"  # Колонка K
                            f"baths: {sh.cell_value(rx, 11)}\n"  # Колонка L
                            f"area_sqft: {sh.cell_value(rx, 12)}\n"  # Колонка M
                            f"price: {sh.cell_value(rx, 13)}\n"  # Колонка N
                            f"buy: {sh.cell_value(rx, 15)}\n"  # Колонка P
                        )

                        # Создаем комментарий
                        Comment.objects.create(
                            type="lead",
                            item_id=lead.id,
                            text=comment_text
                        )
                    except ValueError:
                        messages.error(request, "Нечисловое значение в номере телефона!")
                    except Lead.MultipleObjectsReturned:
                        messages.error(request, "Ошибка: найдено несколько лидов с таким номером!")
                    except Exception as e:
                        messages.error(request, f"Другая ошибка: {e}")
            messages.success(request, f'Было выгружено <b>{leads_count}</b> новых контактов')
        else:
            messages.error(request, 'А файл точно был прикреплен?')
        return redirect('main:lead-list')


class ChangeLeadResponsibleView(BaseView):
    def post(self, request, *args, **kwargs):
        if (responsible := request.POST.get('responsible')) and (leads := request.POST.getlist('lead')):
            for l_id in leads:
                try:
                    user = User.objects.get(pk=responsible)
                    lead = Lead.objects.get(pk=l_id)
                    lead.responsible = user
                    lead.updated_by = request.user
                    lead.save()
                except ObjectDoesNotExist:
                    continue
            messages.success(request, 'Ответственный у контактов установлен')
        else:
            messages.error(request, 'А Вы точно всё выбрали?')
        return redirect(self.request.POST.get('next'))
