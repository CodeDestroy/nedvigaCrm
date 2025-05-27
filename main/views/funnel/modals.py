from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.forms import FunnelForm, StageForm
from main.models import Funnel, Stage
from main.views import BaseView


class ModalFunnelCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'modals/create.html', {
            'url': reverse('main:funnel-create'), 'name': 'воронки продаж', 'form': FunnelForm()})


class ModalFunnelUpdate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        funnel = get_object_or_404(Funnel, pk=kwargs.get('funnel_id'))
        return render(request, 'modals/update.html', {
            'url': reverse('main:funnel-update', kwargs={'funnel_id': funnel.pk}), 'name': 'воронки продаж',
            'form': FunnelForm(instance=funnel), 'next': reverse('main:funnel-page', kwargs={'funnel_id': funnel.pk, 'user_id': request.user.pk})})


class ModalFunnelDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        funnel = get_object_or_404(Funnel, pk=kwargs.get('funnel_id'))
        return render(request, 'modals/delete.html', {
            'url': reverse('main:funnel-delete', kwargs={'funnel_id': funnel.pk}),
            'name': 'воронку продаж'
        })


class ModalStageCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'modals/create.html', {
            'url': reverse('main:stage-create', kwargs={'funnel_id': self.kwargs.get('funnel_id')}),
            'name': 'стадии продаж', 'form': StageForm(funnel_id=self.kwargs.get('funnel_id'))})


class ModalStageUpdate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        stage = get_object_or_404(Stage, pk=kwargs.get('stage_id'))
        return render(request, 'modals/update.html', {
            'url': reverse('main:stage-update', kwargs={'funnel_id': stage.funnel.pk, 'stage_id': stage.pk}),
            'name': 'стадии продаж', 'form': StageForm(instance=stage, funnel_id=self.kwargs.get('funnel_id')),
            'next': reverse('main:funnel-page', kwargs={'funnel_id': stage.funnel.pk, 'user_id': request.user.pk})})


class ModalStageDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        stage = get_object_or_404(Stage, pk=kwargs.get('stage_id'))
        return render(request, 'modals/delete.html', {
            'url': reverse('main:stage-delete', kwargs={'funnel_id': stage.funnel.pk, 'stage_id': stage.pk}),
            'name': 'стадию продаж'
        })
