from django.views.generic import ListView
from django.shortcuts import render
""" from main.models.site import BuyObject """

from main.models import Complex, Building, Apartment, ApartmentPhoto

class BaseFeedView(ListView):
    content_type = 'application/xml'
    model = Apartment
    context_object_name = 'apartments'

    def get_queryset(self):
        return super().get_queryset().filter(status="available")

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/xml'
        return super().render_to_response(context, **response_kwargs)

class AvitoFeed(BaseFeedView):
    template_name = 'feeds/avito.xml'

class DomClickFeed(BaseFeedView):
    template_name = 'feeds/avito.xml'
    extra_context = {'type': 'domclick'}
class NewAvitoFeed(BaseFeedView):
    template_name = 'feeds/avito-new.xml'