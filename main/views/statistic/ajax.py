import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import classonlymethod

from main.models import Source, Stage
from main.views import BaseView


class AjaxSourceStageView(BaseView):
    view_is_async = True
    dt_now = datetime.date.today()

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = True
        return view

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        if frm := request.GET.get('from'):
            frm = datetime.datetime.strptime(frm, '%Y-%m-%d').date()
        else:
            frm = self.dt_now
        if to := request.GET.get('to'):
            to = datetime.datetime.strptime(to, '%Y-%m-%d').date()
        else:
            to = self.dt_now
        return render(request, 'statistic/sources/ajax.html', {
            'sources': Source.objects.distinct().filter(
                leadsource__lead__deal__stage__pk=kwargs.get('stage_id'),
                leadsource__created_at__gte=frm, leadsource__created_at__lte=to + datetime.timedelta(days=1)),
            'stage': get_object_or_404(Stage, pk=kwargs.get('stage_id')),
            'from': frm,
            'to': to,
        })
