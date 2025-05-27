from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import PartnerForm
from main.models import Partner, Stage
from main.views import BaseView


class PartnerListView(ListView, BaseView):
    model = Partner
    context_object_name = 'partners'
    paginate_by = settings.PAGINATION
    template_name = 'partner/list.html'
    extra_context = {'title': 'Список агентов'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stages'] = Stage.objects.all()
        if self.request.user.is_staff:
            context['admin_links'] = [{
                'url': reverse('main:partner-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
                'class': 'btn btn-success',  'get': reverse('main:modal-partner-create')
            }]
        return context


class PartnerCreateView(CreateView, BaseView):
    model = Partner
    form_class = PartnerForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание партнера'}

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Партнер успешно создан')
        return redirect('main:partner-list')


class PartnerUpdateView(UpdateView, BaseView):
    model = Partner
    form_class = PartnerForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'partner_id'
    extra_context = {'title': 'Обновление партнера'}

    def form_valid(self, form):
        form.save()
        messages.warning(self.request, 'Партнер успешно обновлен')
        return redirect('main:partner-list')


class PartnerDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        partner = get_object_or_404(Partner, pk=kwargs.get('partner_id'))
        partner.deleted = True
        partner.delete()
        messages.error(request, 'Партнер успешно удален')
        return redirect('main:partner-list')
