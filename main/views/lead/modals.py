from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.forms import TaskForm, SourceForm, ShowingForm
from main.forms.deal import DealUserForm, DealAdminForm
from main.models import User, Lead
from main.views import BaseView


class ModalLeadDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs.get('lead_id'))
        return render(request, 'modals/delete.html', {
            'url': reverse('main:lead-delete', kwargs={'lead_id': lead.pk}),
            'name': 'контакт'
        })


class ModalTaskLeadCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'lead/modals/task.html', {
            'url': reverse('main:task-create'), 'name': 'Задачи', 'form': TaskForm(),
            'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True) if request.user.is_staff else None, 'lead_id': self.kwargs.get('lead_id'),
            'next': reverse('main:lead-page', kwargs={'lead_id': self.kwargs.get('lead_id')})})


class ModalShowingLeadCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'lead/modals/showing.html', {
            'url': reverse('main:showing-create'), 'name': 'показа', 'form': ShowingForm(),
            'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True) if request.user.is_staff else None,
            'lead_id': self.kwargs.get('lead_id'),
            'next': reverse('main:lead-page', kwargs={'lead_id': self.kwargs.get('lead_id')})})


class ModalSourceLeadCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'modals/create.html', {
            'url': reverse('main:source-create'), 'name': 'источника контакта', 'form': SourceForm(),
            'next': reverse('main:lead-page', kwargs={'lead_id': self.kwargs.get('lead_id')})})


class ModalDealLeadCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'lead/modals/deal.html', {
            'url': reverse('main:deal-create'), 'name': 'сделку', 'lead_id': self.kwargs.get('lead_id'),
            'form': DealUserForm() if not request.user.is_staff else DealAdminForm(),
            'next': reverse('main:lead-page', kwargs={'lead_id': self.kwargs.get('lead_id')})})
