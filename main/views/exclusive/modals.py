from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.models.site import BuyObject
from main.views import BaseView


class ModalExclusiveDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        exclusive = get_object_or_404(BuyObject, pk=kwargs.get('exclusive_id'))
        return render(request, 'modals/delete.html', {
            'url': reverse('main:exclusive-delete', kwargs={'exclusive_id': exclusive.pk}), 'name': 'эксклюзива'
        })
