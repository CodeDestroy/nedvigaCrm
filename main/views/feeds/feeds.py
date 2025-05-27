from django.db.models import Q, F
from django.views.generic import ListView

from main.models import Complex, Building, Apartment, ApartmentPhoto


class BaseFeedView(ListView):
    content_type = 'application/xml'
    model = Apartment
    context_object_name = 'apartments'

    def get_queryset(self):
        return Apartment.objects.filter(
            Q(Q(obj__parent__isnull=False, obj__parent__hide=False, obj__parent__is_deleted=False) | Q(obj__parent__isnull=True)) &
            Q(Q(is_deleted=False, hide=False, obj__hide=False, obj__is_deleted=False) | Q(obj__parent__isnull=False, obj__parent__show=True) | Q(obj__show=True)))


class AvitoFeed(BaseFeedView):
    template_name = 'feeds/avito.xml'


class NewAvitoFeed(BaseFeedView):
    template_name = 'feeds/avito-new.xml'


class CianFeedNew(BaseFeedView):
    template_name = 'feeds/cian.xml'

    def get_queryset(self):
        return super().get_queryset().filter(Q(obj__cian_id__isnull=False) | Q(obj__parent__cian_id__isnull=False))


class DomClickFeed(BaseFeedView):
    template_name = 'feeds/domclick/main.xml'
    extra_context = {'type': 'domclick'}

    """ def get_queryset(self):
        return super(DomClickFeed, self).get_queryset().filter(
            Q(obj__parent__isnull=False, obj__parent__domclick_hide=False) |
            Q(obj__parent__isnull=True, obj__domclick_hide=False), domclick_hide=False) """


"""class YandexFeed(BaseFeedView):
    template_name = 'feeds/yandex.xml' """
