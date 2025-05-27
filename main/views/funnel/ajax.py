from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from main.models import Deal, Stage, User
from main.views import BaseListView, BaseView


class LeadNoStageListAjax(BaseListView):
    model = Deal
    context_object_name = 'deals'
    paginate_by = settings.AJAX_PAGINATION
    template_name = 'funnel/ajax/no_stage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funnel_id'] = self.kwargs.get('funnel_id')
        context['stage_id'] = self.kwargs.get('stage_id')
        return context

    def get_queryset(self):
        return super().get_queryset().distinct('pk').filter(stage=None)


class LeadStageListAjax(BaseListView):
    model = Deal
    context_object_name = 'deals'
    paginate_by = settings.AJAX_PAGINATION
    template_name = 'funnel/ajax/stage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funnel_id'] = self.kwargs.get('funnel_id')
        context['stage_id'] = self.kwargs.get('stage_id')
        context['user'] = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return context

    def get_queryset(self):
        return super().get_queryset().distinct('pk').filter(
            stage__pk=self.kwargs.get('stage_id'), stage__funnel__pk=self.kwargs.get('funnel_id')
        ).filter(
            Q(responsible__pk=self.kwargs.get('user_id')) | Q(responsible__isnull=True, lead__first_manager__pk=self.kwargs.get('user_id'))
        )


class ChangeStageAjax(BaseView):
    def post(self, request, *args, **kwargs):
        if deal_ids := request.POST.getlist('deal_id'):
            stage_id = kwargs.get('stage_id')
            deals = Deal.objects.filter(pk__in=deal_ids).exclude(stage__pk=stage_id if stage_id > 0 else None)
            if deals and stage_id:
                try:
                    deals.update(stage=Stage.objects.get(pk=stage_id))
                except ObjectDoesNotExist:
                    return HttpResponseNotFound('Стадия не найдена')
            elif deals:
                deals.update(stage=None)
        return HttpResponse('Ok')
