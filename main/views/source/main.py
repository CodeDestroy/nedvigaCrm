from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from main.forms import SourceForm
from main.models import Source
from main.views import BaseView


class SourceCreateView(CreateView, BaseView):
    model = Source
    form_class = SourceForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание паспорта'}

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, 'Источник контакта успешно заполнен')
        return redirect(self.request.POST.get('next', instance.get_absolute_url()))


class SourceListView(ListView, BaseView):
    model = Source
    context_object_name = 'sources'
    paginate_by = settings.PAGINATION
    template_name = 'source/list.html'
    extra_context = {'title': 'Список источников'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:source-create'), 'text': '<i class="ti ti-plus icon"></i> Создать источник контактов',
            'class': 'btn btn-success',  'get': reverse('main:modal-source-create')}]
        return context


class SourceUpdateView(UpdateView, BaseView):
    model = Source
    form_class = SourceForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'source_id'
    extra_context = {'title': 'Обновление источника контакта'}

    def form_valid(self, form):
        messages.warning(self.request, 'Источник контакта успешно обновлен')
        return super().form_valid(form)


class SourceDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        get_object_or_404(Source, pk=kwargs.get('source_id')).delete()
        messages.error(request, 'Источник контакта успешно удален')
        return redirect('main:source-list')
