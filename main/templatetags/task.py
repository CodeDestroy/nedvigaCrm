import datetime

from django import template
from django.db.models import Count, Q, F

from main.models import Task, Showing

register = template.Library()

dt_now = datetime.date.today()


@register.simple_tag(name='tasks')
def tasks(user=None):  # Количество задач
    return count(Task, user)


@register.simple_tag(name='showings')
def showings(user=None):  # Количество задач
    return count(Showing, user)


def count(model, user):
    if user:
        return model.objects.aggregate(
            closed_count=Count('pk', filter=Q(user=user, is_done=True)),
            outdated_count=Count('pk', filter=Q(user=user, is_done=False, date_to__date__lt=dt_now)),
            today_count=Count('pk', filter=Q(user=user, is_done=False, date_to__date=dt_now)),
            tomorrow_count=Count('pk', filter=Q(user=user, is_done=False,
                                                date_to__date=dt_now + datetime.timedelta(days=1))),
            other_count=Count('pk', filter=Q(user=user)) - F('closed_count') - F('outdated_count') - F(
                'today_count') - F('tomorrow_count')
        )
    return model.objects.aggregate(
        closed_count=Count('pk', filter=Q(is_done=True)),
        outdated_count=Count('pk', filter=Q(is_done=False, date_to__date__lt=dt_now)),
        today_count=Count('pk', filter=Q(is_done=False, date_to__date=dt_now)),
        tomorrow_count=Count('pk', filter=Q(is_done=False, date_to__date=dt_now + datetime.timedelta(days=1))),
        other_count=Count('pk') - F('closed_count') - F('outdated_count') - F('today_count') - F('tomorrow_count')
    )
