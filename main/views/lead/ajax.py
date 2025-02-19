from django.db.models import Q
from django.views.generic import ListView

from main.models import Lead
from main.views import BaseView


class AjaxLeadListView(ListView, BaseView):
    model = Lead
    context_object_name = 'items'
    template_name = 'ajax/client_and_partner_list.html'

    # При изменении фильтров, поменяй и отчет
    def get_queryset(self):
        qs = super().get_queryset()
        if chars := self.request.GET.get('chars'):
            qs = qs.filter(Q(surname__icontains=chars) | Q(name__icontains=chars) | Q(patronymic__icontains=chars)
                           | Q(phone__icontains=chars))
        return qs
