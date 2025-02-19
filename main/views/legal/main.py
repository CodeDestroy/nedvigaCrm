from django.shortcuts import render

from main.views import BaseView


class LegalListView(BaseView):
    template_name = 'funnel/legal/list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Юридическая воронка'})
