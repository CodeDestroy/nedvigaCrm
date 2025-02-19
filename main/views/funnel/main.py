from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView, CreateView

from main.forms import FunnelForm, StageForm
from main.models import Funnel, Stage, User
from main.views import BaseDetailView, BaseView


class FunnelCreateView(CreateView, BaseView):
    model = Funnel
    form_class = FunnelForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание воронки продаж'}

    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, 'Воронка продаж успешно создана')
        return redirect(self.request.POST.get(
            'next', reverse('main:funnel-page', kwargs={'user_id': self.request.user.pk, 'funnel_id': obj.id})))


class FunnelUpdateView(UpdateView, BaseView):
    model = Funnel
    form_class = FunnelForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'funnel_id'
    extra_context = {'title': 'Обновление воронки продаж'}

    def form_valid(self, form):
        obj = form.save()
        messages.warning(self.request, 'Воронка продаж успешно обновлена')
        return redirect(self.request.POST.get(
            'next', reverse('main:funnel-page', kwargs={'user_id': self.request.user.pk, 'funnel_id': obj.id})))


class FunnelPageView(BaseDetailView):
    model = Funnel
    pk_url_kwarg = 'funnel_id'
    template_name = 'funnel/page.html'
    context_object_name = 'funnel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        if self.request.user.is_staff:
            context['admin_links'] = [{
                'url': reverse('main:stage-create', kwargs={'funnel_id': self.object.pk}),
                'text': '<i class="ti ti-plus icon"></i> Создать стадию', 'class': 'btn btn-success',
                'get': reverse('main:modal-stage-create', kwargs={'funnel_id': self.object.pk})
            }, {
                'url': reverse('main:funnel-update', kwargs={'funnel_id': self.object.pk}),
                'text': '<i class="ti ti-pencil icon"></i> Изменить', 'class': 'btn btn-warning',
                'get': reverse('main:modal-funnel-update', kwargs={'funnel_id': self.object.pk})
            }, {
                'url': reverse('main:funnel-delete', kwargs={'funnel_id': self.object.pk}),
                'text': '<i class="ti ti-trash icon"></i> Удалить', 'class': 'btn btn-danger',
                'get': reverse('main:modal-funnel-delete', kwargs={'funnel_id': self.object.pk})
            }]
            context['users'] = User.objects.all()
        context['stages'] = self.object.parent_stages()
        context['funnels'] = Funnel.objects.all()
        context['user'] = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return context

    def get_queryset(self):
        return super().get_queryset().prefetch_related('stage_set')


class FunnelDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        get_object_or_404(Funnel, pk=kwargs.get('funnel_id')).delete()
        messages.error(request, 'Воронка продаж успешно удалена')
        return redirect('main:index')


class StageCreateView(CreateView, BaseView):
    model = Stage
    form_class = StageForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание стадии продаж'}

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(funnel_id=self.kwargs.get('funnel_id'), **self.get_form_kwargs())

    def form_valid(self, form):
        obj = form.save()
        messages.success(self.request, 'Стадия продаж успешно создан')
        return redirect(self.request.POST.get(
            'next', reverse('main:funnel-page', kwargs={'user_id': self.request.user.pk, 'funnel_id': obj.funnel.id})))


class StageUpdateView(UpdateView, BaseView):
    model = Stage
    form_class = StageForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'stage_id'
    extra_context = {'title': 'Обновление стадии продаж'}

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(funnel_id=self.kwargs.get('funnel_id'), **self.get_form_kwargs())

    def form_valid(self, form):
        obj = form.save()
        messages.warning(self.request, 'Стадия продаж успешно обновлена')
        return redirect(self.request.POST.get(
            'next', reverse('main:funnel-page', kwargs={'user_id': self.request.user.pk, 'funnel_id': obj.funnel.id})))


class StageDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        stage = get_object_or_404(Stage, pk=kwargs.get('stage_id'))
        if stage.parent:
            if child := stage.child():
                child.parent = stage.parent
                child.save()
        stage.delete()
        messages.error(request, 'Стадия продаж успешно удалена')
        return redirect('main:funnel-page', funnel_id=kwargs.get('funnel_id'), user_id=request.user.pk)
