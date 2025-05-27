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
    template_name = 'feeds/domclick/main.xml'
    extra_context = {'type': 'domclick'}
class NewAvitoFeed(BaseFeedView):
    template_name = 'feeds/avito-new.xml'
class NewAvitoFeedByComplex(BaseFeedView):
    
    template_name = 'feeds/avito-new.xml'
    def get_queryset(self):
        complex_id = self.kwargs.get("complex_id")  # получаем complex_id из URL
        return super().get_queryset().filter(
            status="available",
            building__complex_id=complex_id
        )
class CianFeedNew(BaseFeedView):
    template_name = 'feeds/cian.xml'

    """ def get_queryset(self):
        return super().get_queryset().filter(Q(obj__cian_id__isnull=False) | Q(obj__parent__cian_id__isnull=False)) """
