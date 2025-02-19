from django.conf import settings

from main.models import Deal
from main.views import BaseListView


class LegalStatusListAjax(BaseListView):
    model = Deal
    context_object_name = 'deals'
    paginate_by = settings.AJAX_PAGINATION
    template_name = 'funnel/legal/status.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        return context

    def get_queryset(self):
        return super().get_queryset().distinct('pk').filter(legal_status=self.kwargs.get('status'))
