from datetime import timedelta

from django import template
from django.db.models import Sum, Avg, Count, Q

from main.models import Call, Lead, Deal, LeadSource

register = template.Library()


@register.simple_tag(name='calls')
def calls(direction, frm, to, user=None):  # Количество входящих вызовов
    if user:
        return Call.objects.filter(user=user, direction=direction, created_at__gte=frm, created_at__lte=to + timedelta(days=1)).count()
    return Call.objects.filter(direction=direction, created_at__gte=frm, created_at__lte=to + timedelta(days=1)).count()


@register.simple_tag(name='contacts')
def contacts(frm, to, user=None):  # Количество контактов
    lead_source = LeadSource.objects.distinct('lead').filter(
        created_at__gte=frm, created_at__lte=to + timedelta(days=1)).values_list('lead')
    if user:
        #  return Lead.objects.filter(Q(responsible=user) | Q(first_manager=user), created_at__gte=frm, created_at__lte=to + timedelta(days=1)).count()
        return Lead.objects.exclude(Q(warm__in=['not_client', 'not_call']) | Q(warm__isnull=True)).filter(responsible=user, pk__in=lead_source).aggregate(
            new=Count('pk', filter=Q(created_at__gte=frm)), old=Count('pk', filter=Q(created_at__lt=frm))
        )
    return Lead.objects.exclude(Q(warm__in=['not_client', 'not_call']) | Q(warm__isnull=True)).filter(pk__in=lead_source).aggregate(
        new=Count('pk', filter=Q(created_at__gte=frm)), old=Count('pk', filter=Q(created_at__lt=frm))
    )


@register.simple_tag(name='stages')
def stages(stage, frm, to, user=None):  # Количество контактов
    if user:
        return Deal.objects.aggregate(
            count=Count('pk', filter=Q(lead__warm__in=['hot', 'warm', 'cold'], responsible=user, stage=stage, created_at__gte=frm, created_at__lte=to + timedelta(days=1))),
            all=Count('pk', filter=Q(lead__warm__in=['hot', 'warm', 'cold'], responsible=user, stage__statistic=True, created_at__gte=frm, created_at__lte=to + timedelta(days=1)))
        )
    return Deal.objects.aggregate(
        count=Count('pk', filter=Q(lead__warm__in=['hot', 'warm', 'cold'], stage=stage, created_at__gte=frm, created_at__lte=to + timedelta(days=1))),
        all=Count('pk', filter=Q(lead__warm__in=['hot', 'warm', 'cold'], stage__statistic=True, created_at__gte=frm, created_at__lte=to + timedelta(days=1)))
    )


@register.simple_tag(name='bad')
def bad_count(frm, to, user=None):  # Количество контактов
    all_count = Deal.objects.filter(stage__bad=True, created_at__gte=frm, created_at__lte=to + timedelta(days=1)).count()
    if user:
        count = Deal.objects.filter(responsible=user, stage__bad=True, created_at__gte=frm, created_at__lte=to + timedelta(days=1)).exclude(lead__warm='not_client').count()
    else:
        count = Deal.objects.filter(stage__bad=True, created_at__gte=frm, created_at__lte=to + timedelta(days=1)).exclude(lead__warm='not_client').count()
    return {'count': count, 'all': all_count}


@register.simple_tag(name='deals')
def deals(frm, to, user=None):
    d = Deal.objects.filter(reserved__gte=frm, reserved__lte=to, stage__good=True)
    if user:
        return d.aggregate(
            reserve_all=Count('pk'),
            reserve_count=Count('pk', filter=Q(responsible=user)),
            reserve_sum=Sum('price', filter=Q(responsible=user)),
            reserve_avg=Avg('price', filter=Q(responsible=user)),
            sale_all=Count('pk', filter=Q(stage__name='Продано')),
            sale_count=Count('pk', filter=Q(responsible=user, stage__name='Продано')),
            sale_sum=Sum('price', filter=Q(responsible=user, stage__name='Продано')),
            sale_avg=Avg('price', filter=Q(responsible=user, stage__name='Продано')),
            com_avg=Sum('money__agent', filter=Q(responsible=user)) / Count('pk', Q(responsible=user)),
            com_sum=Sum('money__agent', filter=Q(responsible=user)),
            com_manager=Sum('money__manager', filter=Q(responsible=user))
        )
    return d.aggregate(
        reserve_all=Count('pk'), reserve_count=Count('pk'), reserve_sum=Sum('price'), reserve_avg=Avg('price'),
        sale_all=Count('pk', filter=Q(stage__name='Продано')),
        sale_count=Count('pk', filter=Q(stage__name='Продано')),
        sale_sum=Sum('price', filter=Q(stage__name='Продано')),
        sale_avg=Avg('price', filter=Q(stage__name='Продано')),
        com_avg=Sum('money__agent') / Count('pk'), com_sum=Sum('money__agent'), com_manager=Sum('money__manager')
    )


@register.simple_tag(name='source')
def source(frm, to, stage=None, src=None):
    if src:
        return Lead.objects.filter(
            deal__stage=stage, leadsource__source=src, leadsource__created_at__gte=frm,
            leadsource__created_at__lt=to + timedelta(days=1)
        ).aggregate(
            count=Count('pk'),
            # Горячий
            count_hot_new=Count('pk', filter=Q(warm='hot', created_at__gte=frm)),
            count_hot_old=Count('pk', filter=Q(warm='hot', created_at__lt=frm)),
            # Теплый
            count_warm_new=Count('pk', filter=Q(warm='warm', created_at__gte=frm)),
            count_warm_old=Count('pk', filter=Q(warm='warm', created_at__lt=frm)),
            # Холодный
            count_cold_new=Count('pk', filter=Q(warm='cold', created_at__gte=frm)),
            count_cold_old=Count('pk', filter=Q(warm='cold', created_at__lt=frm)),
            # Не клиент
            count_not_client_new=Count('pk', filter=Q(warm='not_client', created_at__gte=frm)),
            count_not_client_old=Count('pk', filter=Q(warm='not_client', created_at__lt=frm)),
            # Не дозвонились
            count_not_call_new=Count('pk', filter=Q(warm='not_call', created_at__gte=frm)),
            count_not_call_old=Count('pk', filter=Q(warm='not_call', created_at__lt=frm)),
            # Не актуально
            count_not_actual_new=Count('pk', filter=Q(warm='not_actual', created_at__gte=frm)),
            count_not_actual_old=Count('pk', filter=Q(warm='not_actual', created_at__lt=frm)),
            # Без теплоты
            count_none_new=Count('pk', filter=Q(warm__isnull=True, created_at__gte=frm)),
            count_none_old=Count('pk', filter=Q(warm__isnull=True, created_at__lt=frm))
        )
    return Lead.objects.filter(
        deal__stage=stage, leadsource__source__isnull=False, leadsource__created_at__gte=frm,
        leadsource__created_at__lt=to + timedelta(days=1)
    ).aggregate(
        count=Count('pk'),
        # Горячий
        count_hot_new=Count('pk', filter=Q(warm='hot', created_at__gte=frm)),
        count_hot_old=Count('pk', filter=Q(warm='hot', created_at__lt=frm)),
        # Теплый
        count_warm_new=Count('pk', filter=Q(warm='warm', created_at__gte=frm)),
        count_warm_old=Count('pk', filter=Q(warm='warm', created_at__lt=frm)),
        # Холодный
        count_cold_new=Count('pk', filter=Q(warm='cold', created_at__gte=frm)),
        count_cold_old=Count('pk', filter=Q(warm='cold', created_at__lt=frm)),
        # Не клиент
        count_not_client_new=Count('pk', filter=Q(warm='not_client', created_at__gte=frm)),
        count_not_client_old=Count('pk', filter=Q(warm='not_client', created_at__lt=frm)),
        # Не дозвонились
        count_not_call_new=Count('pk', filter=Q(warm='not_call', created_at__gte=frm)),
        count_not_call_old=Count('pk', filter=Q(warm='not_call', created_at__lt=frm)),
        # Не актуально
        count_not_actual_new=Count('pk', filter=Q(warm='not_actual', created_at__gte=frm)),
        count_not_actual_old=Count('pk', filter=Q(warm='not_actual', created_at__lt=frm)),
        # Без теплоты
        count_none_new=Count('pk', filter=Q(warm__isnull=True, created_at__gte=frm)),
        count_none_old=Count('pk', filter=Q(warm__isnull=True, created_at__lt=frm))
    )
