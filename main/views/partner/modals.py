from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.forms import PartnerForm
from main.models import Partner
from main.views import BaseView


class ModalPartnerCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'modals/create.html', {
            'url': reverse('main:partner-create'), 'name': 'партнера', 'form': PartnerForm()})


class ModalPartnerUpdate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=kwargs.get('partner_id'))
        return render(request, 'modals/update.html', {
            'url': reverse('main:partner-update', kwargs={'partner_id': partner.pk}),
            'name': 'партнера', 'form': PartnerForm(instance=partner)})


class ModalPartnerDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=kwargs.get('partner_id'))
        return render(request, 'modals/delete.html', {
            'url': reverse('main:partner-delete', kwargs={'partner_id': partner.pk}), 'name': 'партнера'})
