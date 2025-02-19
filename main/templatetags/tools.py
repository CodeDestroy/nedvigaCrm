import datetime

from django import template
from django.conf import settings

from main.models import Lead, Call, Notification, User

register = template.Library()


@register.simple_tag(name='percent')
def percent(value, max_value):
    try:
        value = float(value)
        max_value = float(max_value)
        ratio = (value / max_value) * 100
        return str(round(ratio, 2))
    except ZeroDivisionError:
        return "0"
    except (ValueError, TypeError, OverflowError):
        return ""


@register.simple_tag(name='fix_page_request')
def fix_page_request(request):
    request = request.copy()
    if 'page' in request:
        del request['page']
    if request.urlencode():
        return request.urlencode() + '&'
    return ''


@register.simple_tag(name='get_list_request')
def fix_page_request(request, key):
    return request.GET.getlist(key)


@register.simple_tag(name='unassembled_count')
def unassembled_count():
    return Lead.objects.filter(processed__in=['redo', 'not'], is_deleted=False).count()


@register.simple_tag(name='missed_count')
def missed_count():
    return Call.objects.filter(direction='in', status='Missed', processed=False).distinct().count()


@register.simple_tag(name='from_list')
def percent():
    return settings.FROM_CHOICES


@register.simple_tag(name='notifications')
def notifications(user):
    return Notification.objects.filter(user=user, read=False)


@register.simple_tag(name='birthdays')
def birthdays():
    dt_now = datetime.date.today()
    return User.objects.filter(birth__month=dt_now.month)
