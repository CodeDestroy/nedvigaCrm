from django import template
from django.conf import settings
from django.db.models import Q

from main.models import User, Source, Partner, Funnel

register = template.Library()


@register.inclusion_tag('lead/filter.html', takes_context=True)
def lead_filter(context):
    return {
        'request': context['request'],
        'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True),
        'funnels': Funnel.objects.all(),
        'partners': Partner.objects.all(),
        'sources': Source.objects.all(),
        'warm': settings.LEAD_WARM_CHOICES,
        'processed': settings.PROCESSED_CHOICES,
        'payment': settings.PAYTYPE_CHOICES,
        'from': settings.FROM_CHOICES,
        'decoration': settings.DECORATION_CHOICES,
        'marital': settings.MARITAL_CHOICES,
        'purpose': settings.PURPOSE_BUY
    }
