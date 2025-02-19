from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from main.forms import TaskForm, ShowingForm
from main.models import Deal, User
from main.views import BaseView


class ModalTaskDealCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'deal/modals/task.html', {
            'url': reverse('main:task-create'), 'name': 'задачи', 'form': TaskForm(),
            'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True) if request.user.is_staff else None,
            'deal_id': self.kwargs.get('deal_id'),
            'next': reverse('main:deal-page', kwargs={'deal_id': self.kwargs.get('deal_id')})})


class ModalShowingDealCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'deal/modals/showing.html', {
            'url': reverse('main:showing-create'), 'name': 'показа', 'form': ShowingForm(),
            'users': User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True) if request.user.is_staff else None,
            'deal_id': self.kwargs.get('deal_id'),
            'next': reverse('main:deal-page', kwargs={'deal_id': self.kwargs.get('deal_id')})})


class ModalDealDelete(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        deal = get_object_or_404(Deal, pk=kwargs.get('deal_id'))
        return render(request, 'modals/delete.html', {
            'url': reverse('main:deal-delete', kwargs={'deal_id': deal.pk}),
            'name': 'сделку'
        })
