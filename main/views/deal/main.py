from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import TaskForm, CommentForm, ShowingForm, MoneyForm, MortgageForm
from main.forms.deal import DealAdminForm, DealUserForm
from main.models import Deal, User, Lead, Funnel, Money, Mortgage, Notification
from main.views import BaseView, BaseDetailView


class DealListView(ListView, BaseView):
    model = Deal
    context_object_name = 'deals'
    paginate_by = settings.PAGINATION
    template_name = 'deal/list.html'
    extra_context = {'title': 'Список сделок', 'funnels': Funnel.objects.all(),
                     'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)}

    def get_queryset(self):
        qs = super().get_queryset().distinct('pk')
        if text := self.request.GET.get('text'):
            qs = qs.filter(name__icontains=text)
        if user := self.request.GET.get('user'):
            qs = qs.filter(responsible__pk=user)
        if responsible := self.request.GET.get('responsible'):
            qs = qs.filter(responsible__pk=responsible)
        if stage := self.request.GET.get('stage'):
            qs = qs.filter(stage__pk=stage)
        if self.request.GET.get('no_lead'):
            qs = qs.filter(lead=None)
        return qs


class DealCreateView(CreateView, BaseView):
    model = Deal
    form_class = DealAdminForm
    template_name = 'deal/form.html'
    extra_context = {'title': 'Создание сделки'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lead_id'] = self.request.POST.get('lead_id')
        return context

    def get_form(self, form_class=None):
        if not self.request.user.is_staff:
            return DealUserForm(**self.get_form_kwargs())
        return DealAdminForm(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)
        if lead_id := self.request.POST.get('lead_id'):
            instance.lead = get_object_or_404(Lead, pk=lead_id)
        instance.responsible = self.request.user
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Сделка успешно создана')
        return redirect(instance.get_absolute_url())


class DealUpdateView(UpdateView, BaseView):
    model = Deal
    form_class = DealAdminForm
    template_name = 'deal/form.html'
    pk_url_kwarg = 'deal_id'
    extra_context = {'title': 'Обновление сделки'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lead_id'] = self.request.POST.get('lead_id')
        return context

    def get_form(self, form_class=None):
        if not self.request.user.is_staff:
            return DealUserForm(**self.get_form_kwargs())
        return DealAdminForm(**self.get_form_kwargs())

    def form_valid(self, form):
        instance = form.save(commit=False)
        # Получаем исходное значение ответственного из базы данных
        original_instance = Deal.objects.get(pk=instance.pk)
        previous_responsible = original_instance.responsible

        if not instance.responsible:
            instance.responsible = self.request.user
        if lead_id := self.request.POST.get('lead_id'):
            instance.lead = get_object_or_404(Lead, pk=lead_id)
        instance.updated_by = self.request.user
        instance.save()

        # Проверка: изменился ли ответственный
        if previous_responsible != instance.responsible:
            # Создаем уведомление для нового ответственного
            Notification.objects.create(
                name="Вам передана сделка",
                text="Не забудьте посмотреть",
                priority='danger',
                user=instance.responsible,  # Назначаем уведомление новому ответственному
                type='deal',
                item_id=instance.pk,
                created_by=self.request.user
            )

        messages.warning(self.request, 'Сделка успешно обновлена')
        return redirect(instance.get_absolute_url())


class DealMortgageCreateView(CreateView, BaseView):
    model = Mortgage
    form_class = MortgageForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание ипотеки'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.deal = get_object_or_404(Deal, pk=self.kwargs.get('deal_id'))
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Ипотека успешно заполнена')
        return HttpResponseRedirect(instance.deal.get_absolute_url())


class DealMortgageUpdateView(UpdateView, BaseView):
    model = Mortgage
    form_class = MortgageForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'mortgage_id'
    extra_context = {'title': 'Обновление ипотеки'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        instance.save()
        messages.warning(self.request, 'Ипотека успешно обновлена')
        return HttpResponseRedirect(instance.deal.get_absolute_url())


class DealMoneyCreateView(CreateView, BaseView):
    model = Money
    form_class = MoneyForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание денежек'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.deal = get_object_or_404(Deal, pk=self.kwargs.get('deal_id'))
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Денежки успешно заполнены')
        return HttpResponseRedirect(instance.deal.get_absolute_url())


class DealMoneyUpdateView(UpdateView, BaseView):
    model = Money
    form_class = MoneyForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'money_id'
    extra_context = {'title': 'Обновление денежек'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        instance.save()
        messages.warning(self.request, 'Денежки успешно обновлены')
        return HttpResponseRedirect(instance.deal.get_absolute_url())


class DealPageView(BaseDetailView):
    model = Deal
    pk_url_kwarg = 'deal_id'
    template_name = 'deal/page.html'
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        context['admin_links'] = [{
            'url': reverse('main:deal-task-create', kwargs={'deal_id': self.object.pk}),
            'text': '<i class="ti ti-plus icon"></i> Создать задачу', 'class': 'btn btn-success',
            'get': reverse('main:modal-deal-task-create', kwargs={'deal_id': self.object.pk})
        }, {
            'url': reverse('main:deal-showing-create', kwargs={'deal_id': self.object.pk}),
            'text': '<i class="ti ti-plus icon"></i> Создать показ', 'class': 'btn btn-teal',
            'get': reverse('main:modal-deal-showing-create', kwargs={'deal_id': self.object.pk})
        }, {
            'url': reverse('main:deal-delete', kwargs={'deal_id': self.object.pk}),
            'text': '<i class="ti ti-trash icon"></i> Удалить', 'class': 'btn btn-danger',
            'get': reverse('main:modal-deal-delete', kwargs={'deal_id': self.object.pk})
        }]
        if self.request.user.is_staff:
            context['form'] = DealAdminForm(instance=self.object)
            context['money_form'] = MoneyForm(instance=self.object.money if hasattr(self.object, 'money') else None)
        else:
            context['form'] = DealUserForm(instance=self.object)
        if self.request.user.is_staff or self.request.user.broker:
            context['mortgage_form'] = MortgageForm(instance=self.object.mortgage if hasattr(self.object, 'mortgage') else None)
        context['comment_form'] = CommentForm()
        return context


class DealDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        deal = get_object_or_404(Deal, pk=kwargs.get('deal_id'))
        url = reverse('main:index')
        if deal.stage:
            url = reverse('main:funnel-page', kwargs={'funnel_id': deal.stage.funnel.pk, 'user_id': request.user.pk})
        deal.delete()
        messages.error(request, 'Сделка успешно удалена')
        return redirect(url)


class DealTaskCreateView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'task/form.html', {
            'title': 'Создание задачи',
            'deal_id': self.kwargs.get('deal_id'),
            'form': TaskForm()
        })


class DealShowingCreateView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, 'showing/form.html', {
            'title': 'Создание показа',
            'deal_id': self.kwargs.get('deal_id'),
            'form': ShowingForm()
        })
