from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.forms import UserForm, UserUpdateForm
from main.models import User
from main.views import BaseView


class ModalUserCreate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return render(request, 'modals/create.html', {
            'url': reverse('main:user-create'), 'name': 'пользователя', 'form': UserForm()})


class ModalUserUpdate(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_id'))
        return render(request, 'modals/update.html', {
            'url': reverse('main:user-update', kwargs={'user_id': user.pk}), 'name': 'пользователя',
            'form': UserUpdateForm(instance=user), 'next': reverse('main:user-list')})
