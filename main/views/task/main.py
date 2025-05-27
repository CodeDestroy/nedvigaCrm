import datetime

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView

from main.forms import TaskForm, CommentForm
from main.models import Task, User, Lead, Deal, Comment
from main.views import BaseDetailView, BaseView


class TaskCreateView(CreateView, BaseView):
    model = Task
    form_class = TaskForm
    template_name = 'task/form.html'
    extra_context = {'title': 'Создание задачи'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        if user := self.request.POST.get('user'):
            try:
                instance.user = User.objects.get(pk=user)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Не получилось прикрепить задачу пользователю, поэтому она '
                                             'назначена на вас')
                instance.user = self.request.user
        else:
            instance.user = self.request.user
        if lead_id := self.request.POST.get('lead_id'):
            instance.lead = get_object_or_404(Lead, pk=lead_id)
        if deal_id := self.request.POST.get('deal_id'):
            instance.deal = get_object_or_404(Deal, pk=deal_id)
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, 'Задача успешно создана')
        return redirect(self.request.POST.get('next', instance.get_absolute_url()))


class TaskUpdateView(UpdateView, BaseView):
    model = Task
    form_class = TaskForm
    template_name = 'task/form.html'
    pk_url_kwarg = 'task_id'
    extra_context = {'title': 'Обновление задачи'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.updated_by = self.request.user
        if user := self.request.POST.get('user'):
            try:
                instance.user = User.objects.get(pk=user)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Не получилось прикрепить задачу пользователю, поэтому она '
                                             'назначена на вас')
                instance.user = self.request.user
        else:
            instance.user = self.request.user
        instance.save()
        messages.warning(self.request, 'Задача успешно обновлена')
        return redirect(self.request.POST.get('next', instance.get_absolute_url()))


class TaskPageView(BaseDetailView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'task/page.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Задача &laquo;{self.object.name}&raquo;'
        context['comment_form'] = CommentForm()
        context['admin_links'] = [{
            'url': reverse('main:task-update', kwargs={'task_id': self.object.pk}),
            'text': '<i class="ti ti-pencil icon"></i> Изменить',
            'class': 'btn btn-warning',  # 'get': reverse('cabinet:project-modals-create')
        }]
        if self.request.user.is_staff or self.request.user == self.object.user:
            context['admin_links'].append({
                'url': reverse('main:task-close', kwargs={'task_id': self.object.pk}),
                'text': '<i class="ti ti-alert-triangle icon"></i> Закрыть', 'class': 'btn btn-danger',
                'get': reverse('main:modal-task-close', kwargs={'task_id': self.object.pk})
            })
        return context


class TaskCloseView(BaseView):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        if request.user.is_staff or request.user == task.user:
            task.is_done = True
            task.save()
            Comment.objects.create(type='task', item_id=task.pk,
                                   text=f'Задача закрыта пользователем: <b>{self.request.user}</b>')
            messages.success(self.request, 'Вы успешно закрыли эту задачу')
        else:
            messages.error(self.request, 'Вы не можете закрыть эту задачу')
        return redirect(task.get_absolute_url())

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        if request.user.is_staff or request.user == task.user:
            task.is_done = True
            task.save()
            Comment.objects.create(type='task', item_id=task.pk, text=f'Задача закрыта пользователем: <b>{self.request.user}</b>')
            messages.success(self.request, 'Вы успешно закрыли эту задачу')
        else:
            messages.error(self.request, 'Вы не можете закрыть эту задачу')
        return redirect(self.request.POST.get('next', task.get_absolute_url()))


class BaseTaskListView(ListView, BaseView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = settings.PAGINATION
    template_name = 'task/list.html'

    def dispatch(self, request, *args, **kwargs):
        self.dt_now = datetime.datetime.strptime(kwargs.get('date_str'), '%Y-%m-%d')
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:task-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
            'class': 'btn btn-success'}]
        return context


class TodayTaskListView(BaseTaskListView):
    extra_context = {'title': 'Задачи на сегодня'}

    def get_queryset(self):
        return self.request.user.task.filter(is_done=False, date_to__date=self.dt_now)


class TomorrowTaskListView(BaseTaskListView):
    extra_context = {'title': 'Задачи на завтра'}

    def get_queryset(self):
        return self.request.user.task.filter(is_done=False, date_to__date=self.dt_now + datetime.timedelta(days=1))


class ClosedTaskListView(BaseTaskListView):
    extra_context = {'title': 'Закрытые задачи'}

    def get_queryset(self):
        return self.request.user.task.filter(is_done=True)


class OutdatedTaskListView(BaseTaskListView):
    extra_context = {'title': 'Просроченные задачи'}

    def get_queryset(self):
        return self.request.user.task.filter(is_done=False, date_to__date__lt=self.dt_now)


class OtherTaskListView(BaseTaskListView):
    extra_context = {'title': 'Остальные задачи'}

    def get_queryset(self):
        return self.request.user.task.filter(is_done=False).exclude(
            date_to__date__lte=self.dt_now + datetime.timedelta(days=1))
