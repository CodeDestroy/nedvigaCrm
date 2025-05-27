from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.models import Showing
from main.views import BaseView


class ModalShowingClose(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        showing = get_object_or_404(Showing, pk=kwargs.get('showing_id'))
        return render(request, 'showing/modals/close.html', {
            'url': reverse('main:showing-close', kwargs={'showing_id': showing.pk}),
            'next': showing.get_absolute_url()})
