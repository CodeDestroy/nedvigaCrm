from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.models import Task
from main.views import BaseView


class ModalTaskClose(BaseView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('task_id'))
        return render(request, 'task/modals/close.html', {
            'url': reverse('main:task-close', kwargs={'task_id': task.pk}), 'next': task.get_absolute_url()})
