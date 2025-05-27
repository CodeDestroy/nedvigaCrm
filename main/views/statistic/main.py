import datetime

from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import classonlymethod
from django.views.generic import ListView

from main.models import User, Source, Deal, Funnel
from main.views import BaseView


class ResponsibleStatsView(BaseView):
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
        funnel = get_object_or_404(Funnel, pk=kwargs.get('funnel_id'))
        return render(request, 'statistic/responsible.html', {
            'title': 'Контакты и Сделки по ответственному',
            'users': User.objects.filter(
                Q(fired=False, in_stat=True) | Q(fired=False, updated_at__gt=frm, updated_at__lte=to, in_stat=True)),
            'funnel_id': funnel.pk,
            'funnels': Funnel.objects.all(),
            'stages': funnel.stage_set.filter(statistic=True),
            'from': frm,
            'to': to
        })


class DealStatsView(BaseView):
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
        return render(request, 'statistic/deals.html', {
            'title': 'Сделки по продавцу',
            'users': User.objects.filter(
                Q(fired=False, in_stat=True) | Q(fired=False, updated_at__gt=frm, updated_at__lte=to, in_stat=True)),
            'from': frm,
            'to': to,
        })


class SourceStatsView(BaseView):
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
        return render(request, 'statistic/sources/page.html', {
            'title': 'Источники контактов',
            'funnel': get_object_or_404(Funnel, pk=kwargs.get('funnel_id')),
            'funnels': Funnel.objects.all(),
            'from': frm,
            'to': to,
        })


class SourceStatsEmptyView(BaseView):
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
        return render(request, 'statistic/sources/no_stage.html', {
            'title': 'Источники контактов',
            'sources': Source.objects.distinct().filter(
                leadsource__created_at__gte=frm, leadsource__created_at__lte=to + datetime.timedelta(days=1)),
            'funnels': Funnel.objects.all(),
            'from': frm,
            'to': to,
        })

class DebtorStatsView(ListView, BaseView):
    model = Deal
    context_object_name = 'deals'
    # paginate_by = 25
    template_name = 'statistic/debtor.html'
    extra_context = {'title': 'Дебиторская задолженность'}

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.debetor or request.user.is_superuser):
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frm'] = self.kwargs.get('frm')
        context['to'] = self.request.GET.get('to')
        context['from'] = self.request.GET.get('from')
        
        #context['from_list'] = (('raz', 'Развитие'), ('nmarket', 'Нмаркет'), ('perv', 'Домклик'), ('vdk', 'ВДК'), ('contract', 'Прямой договор'), ('city', 'Сити-центр'), ('sec', 'Вторичка'))
        context['all'] = self.request.GET.get('all')
        context['developers'] = Deal.objects.values('developer').distinct().annotate(
            tcount=Count('developer')).order_by()
        context['developer'] = self.request.GET.get('developer')
       
        return context

    def get_queryset(self):
        if self.request.GET.get('all'):
            deals = super().get_queryset().select_related('money').filter(
                stage__good=True, stage__pk__gte=2, frm=self.kwargs.get('frm'),
                reserved__gte=datetime.date(year=2023, month=11, day=1))
        else:
            deals = super().get_queryset().filter(
                stage__good=True, stage__pk__gte=2, frm=self.kwargs.get('frm'), money__status__in=['wait', 'think'],
                reserved__gte=datetime.date(year=2023, month=11, day=1))
        if frm_date := self.request.GET.get('from'):
            frm_date = datetime.datetime.strptime(frm_date, '%Y-%m-%d').date()
            deals = deals.filter(Q(money__get_date__gte=frm_date) | Q(reserved__gte=frm_date))
        if to_date := self.request.GET.get('to'):
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
            deals = deals.filter(Q(money__get_date__lte=to_date) | Q(reserved__lte=to_date))
        if developer := self.request.GET.get('developer'):
            deals = deals.filter(developer=developer)
        deals = deals.order_by('reserved')
        res = {'sum': 0, 'debt': 0}
        for d in deals:
            if d.money:
                if d.money.paid > 0:
                    res['debt'] += d.money.com_diff()
                    res['sum'] += d.money.paid
                elif d.money.status == 'receive':
                    res['sum'] += d.money.agent
                else:
                    res['debt'] += d.money.agent
        return deals, res
