from django.shortcuts import render

from main.views import BaseView


class MortgageListView(BaseView):
    template_name = 'funnel/mortgage/list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Ипотечная воронка'})
