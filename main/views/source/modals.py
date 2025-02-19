from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.forms import SourceForm
from main.models import Source
from main.views import BaseView


class ModalSourceCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'modals/create.html', {
            'url': reverse('main:source-create'), 'name': 'источника контактов', 'form': SourceForm(),
            'next': reverse('main:source-list')})


class ModalSourceUpdate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        source = get_object_or_404(Source, pk=kwargs.get('source_id'))
        return render(request, 'modals/update.html', {
            'url': reverse('main:source-update', kwargs={'source_id': source.pk}),
            'name': 'источник контактов', 'form': SourceForm(instance=source),
            'next': reverse('main:source-list')})


class ModalSourceDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        source = get_object_or_404(Source, pk=kwargs.get('source_id'))
        return render(request,'modals/delete.html', {
            'url': reverse('main:source-delete', kwargs={'source_id': source.pk}),
            'name': 'источник контактов'
        })
