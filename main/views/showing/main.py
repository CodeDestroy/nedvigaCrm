import datetime

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import ShowingForm, CommentForm
from main.models import Showing, User, Comment, Lead, Deal
from main.views import BaseDetailView, BaseView


class ShowingCreateView(CreateView, BaseView):
    model = Showing
    form_class = ShowingForm
    template_name = 'showing/form.html'
    extra_context = {'title': 'Создание показа'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        if user := self.request.POST.get('user'):
            try:
                instance.user = User.objects.get(pk=user)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Не получилось прикрепить показ пользователю, поэтому он '
                                             'назначен на вас')
                instance.user = self.request.user
        else:
            instance.user = self.request.user
        if lead_id := self.request.POST.get('lead_id'):
            instance.lead = get_object_or_404(Lead, pk=lead_id)
        if deal_id := self.request.POST.get('deal_id'):
            instance.deal = get_object_or_404(Deal, pk=deal_id)
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Показ успешно создан')
        return redirect(self.request.POST.get('next', instance.get_absolute_url()))


class ShowingUpdateView(UpdateView, BaseView):
    model = Showing
    form_class = ShowingForm
    template_name = 'showing/form.html'
    pk_url_kwarg = 'showing_id'
    extra_context = {'title': 'Обновление показа'}

    def form_valid(self, form):
        instance = form.save(commit=False)
        if user := self.request.POST.get('user'):
            try:
                instance.user = User.objects.get(pk=user)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Не получилось прикрепить показ пользователю, поэтому он '
                                             'назначен на вас')
                instance.user = self.request.user
        else:
            instance.user = self.request.user
        if lead_id := self.request.POST.get('lead_id'):
            instance.lead = get_object_or_404(Lead, pk=lead_id)
        if deal_id := self.request.POST.get('deal_id'):
            instance.deal = get_object_or_404(Deal, pk=deal_id)
        instance.updated_by = self.request.user
        instance.save()
        messages.warning(self.request, 'Показ успешно обновлен')
        return redirect(instance.get_absolute_url())


class ShowingPageView(BaseDetailView):
    model = Showing
    pk_url_kwarg = 'showing_id'
    template_name = 'showing/page.html'
    context_object_name = 'showing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'&laquo;{self.object}&raquo;'
        context['form'] = ShowingForm(instance=self.object)
        context['comment_form'] = CommentForm()
        context['admin_links'] = [{
            'url': reverse('main:showing-update', kwargs={'showing_id': self.object.pk}),
            'text': '<i class="ti ti-pencil icon"></i> Изменить', 'class': 'btn btn-warning',
        }]
        if self.request.user.is_staff or self.request.user == self.object.user:
            context['admin_links'].append({
                'url': reverse('main:showing-close', kwargs={'showing_id': self.object.pk}),
                'text': '<i class="ti ti-alert-triangle icon"></i> Закрыть', 'class': 'btn btn-danger',
                'get': reverse('main:modal-showing-close', kwargs={'showing_id': self.object.pk})
            })
        return context


class ShowingCloseView(BaseView):
    def get(self, request, *args, **kwargs):
        showing = get_object_or_404(Showing, pk=self.kwargs.get('showing_id'))
        if request.user.is_staff or request.user == showing.user:
            showing.is_done = True
            showing.save()
            messages.success(self.request, 'Вы успешно закрыли этот показ')
            Comment.objects.create(type='showing', item_id=showing.pk, text=f'Показ закрыт пользователем: <b>{self.request.user}</b>')
        else:
            messages.error(self.request, 'Вы не можете закрыть этот показ')
        return redirect(showing.get_absolute_url())

    def post(self, request, *args, **kwargs):
        showing = get_object_or_404(Showing, pk=self.kwargs.get('showing_id'))
        if request.user.is_staff or request.user == showing.user:
            showing.is_done = True
            showing.save()
            messages.success(self.request, 'Вы успешно закрыли этот показ')
            Comment.objects.create(type='showing', item_id=showing.pk, text=f'Показ закрыт пользователем: <b>{self.request.user}</b>')
        else:
            messages.error(self.request, 'Вы не можете закрыть этот показ')
        return redirect(self.request.POST.get('next', showing.get_absolute_url()))


class BaseShowingListView(BaseView, ListView):
    model = Showing
    context_object_name = 'showings'
    paginate_by = settings.PAGINATION
    template_name = 'showing/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.dt_now = datetime.datetime.strptime(kwargs.get('date_str'), '%Y-%m-%d')
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:showing-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
            'class': 'btn btn-success'}]
        return context


class ClosedShowingListView(BaseShowingListView):
    extra_context = {'title': 'Закрытые показы'}

    def get_queryset(self):
        return self.request.user.showing.filter(is_done=True)


class OutdatedShowingListView(BaseShowingListView):
    extra_context = {'title': 'Просроченные показы'}

    def get_queryset(self):
        return self.request.user.showing.filter(is_done=False, date_to__date__lt=self.dt_now)


class TodayShowingListView(BaseShowingListView):
    extra_context = {'title': 'Показы на сегодня'}

    def get_queryset(self):
        return self.request.user.showing.filter(is_done=False, date_to__date=self.dt_now)


class TomorrowShowingListView(BaseShowingListView):
    extra_context = {'title': 'Показы на завтра'}

    def get_queryset(self):
        return self.request.user.showing.filter(is_done=False, date_to__date=self.dt_now + datetime.timedelta(days=1))


class OtherShowingListView(BaseShowingListView):
    extra_context = {'title': 'Прочие показы'}

    def get_queryset(self):
        return self.request.user.showing.filter(is_done=False).exclude(
            date_to__date__lte=self.dt_now + datetime.timedelta(days=1))
