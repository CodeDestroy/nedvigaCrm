from django import template
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

from main.models import Deal

register = template.Library()


@register.simple_tag(name='stage_deals')
def stage_deals(stage=None, funnel=None, user=None):
    if stage is None:
        return Paginator(Deal.objects.filter(stage=None), settings.AJAX_PAGINATION).page(1)
    return Paginator(Deal.objects.filter(stage=stage, stage__funnel=funnel).filter(
        Q(responsible=user) | Q(responsible__isnull=True, lead__first_manager=user) |
        Q(responsible__isnull=True, lead__responsible=user)), settings.AJAX_PAGINATION).page(1)
