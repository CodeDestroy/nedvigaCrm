from django.views.generic import ListView

from main.models.site import BuyObject


class BaseFeedView(ListView):
    content_type = 'application/xml'
    model = BuyObject
    context_object_name = 'flats'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class AvitoFeed(BaseFeedView):
    template_name = 'feeds/avito.xml'

class DomClickFeed(BaseFeedView):
    template_name = 'feeds/avito.xml'
    extra_context = {'type': 'domclick'}
