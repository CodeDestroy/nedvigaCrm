from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from main.forms import MessageTemplateForm
from main.models import Task, User, Showing, MessageTemplate, Notification
from main.views import BaseView


class BaseManagementTaskShowingView(ListView, BaseView):
    paginate_by = settings.PAGINATION

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if user_id := self.request.GET.get('user'):
            qs = qs.filter(user__pk=user_id)
        if user_id := self.request.GET.get('creator'):
            qs = qs.filter(created_by__pk=user_id)
        if user_id := self.request.GET.get('updater'):
            qs = qs.filter(updated_by__pk=user_id)
        if date := self.request.GET.get('date'):
            date = datetime.strptime(date, '%Y-%m-%d').date()
            qs = qs.distinct().filter(Q(date_to__date=date) | Q(created_at__date=date))
        if self.request.GET.get('hide_closed'):
            qs = qs.filter(is_done=False)
        return qs


class ManagementTaskView(BaseManagementTaskShowingView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'management/task.html'
    extra_context = {'title': 'Пользовательские задачи'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:task-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
            'class': 'btn btn-success',  # 'get': reverse('cabinet:project-modals-create')
        }]
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if text := self.request.GET.get('text'):
            qs = qs.filter(Q(name__icontains=text) | Q(text__icontains=text))
        return qs


class ManagementShowingView(BaseManagementTaskShowingView):
    model = Showing
    context_object_name = 'showings'
    template_name = 'management/showing.html'
    extra_context = {'title': 'Пользовательские показы'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:showing-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
            'class': 'btn btn-success',  # 'get': reverse('cabinet:project-modals-create')
        }]
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if text := self.request.GET.get('text'):
            qs = qs.filter(description__icontains=text)
        return qs


class ManagementChangeUserTask(BaseView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        if (responsible := request.POST.get('responsible')) and (tasks := request.POST.getlist('task')):
            for t_id in tasks:
                try:
                    task = Task.objects.get(pk=t_id)
                    task.user = User.objects.get(pk=responsible)
                    task.updated_by = request.user
                    task.save()
                except ObjectDoesNotExist:
                    continue
            messages.success(request, 'Ответственный у задач установлен')
        else:
            messages.error(request, 'А Вы точно всё выбрали?')
        return redirect(self.request.POST.get('next'))


class ManagementChangeUserShowing(BaseView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        if (responsible := request.POST.get('responsible')) and (tasks := request.POST.getlist('showing')):
            for t_id in tasks:
                try:
                    show = Showing.objects.get(pk=t_id)
                    show.user = User.objects.get(pk=responsible)
                    show.updated_by = request.user
                    show.save()
                except ObjectDoesNotExist:
                    continue
            messages.success(request, 'Ответственный у показов установлен')
        else:
            messages.error(request, 'А Вы точно всё выбрали?')
        return redirect(self.request.POST.get('next'))


class MessageTemplateList(ListView, BaseView):
    model = MessageTemplate
    paginate_by = settings.PAGINATION
    context_object_name = 'templates'
    template_name = 'management/messages/list.html'
    extra_context = {'title': 'Шаблоны сообщений'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_links'] = [{
            'url': reverse('main:management-message-create'), 'text': '<i class="ti ti-plus icon"></i> Создать',
            'class': 'btn btn-success',  # 'get': reverse('cabinet:project-modals-create')
        }]
        return context


class MessageTemplateCreate(SuccessMessageMixin, CreateView, BaseView):
    model = MessageTemplate
    form_class = MessageTemplateForm
    template_name = 'management/messages/form.html'
    extra_context = {'title': 'Создание шаблона'}
    success_url = reverse_lazy('main:management-message-list')
    success_message = 'Шаблон сообщения успешно создан'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)


class MessageTemplateUpdate(SuccessMessageMixin, UpdateView, BaseView):
    model = MessageTemplate
    pk_url_kwarg = 'message_id'
    form_class = MessageTemplateForm
    template_name = 'management/messages/form.html'
    extra_context = {'title': 'Создание шаблона'}
    success_url = reverse_lazy('main:management-message-list')
    success_message = 'Шаблон сообщения успешно обновлен'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)


class MessageTemplateDelete(BaseView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        get_object_or_404(MessageTemplate, pk=kwargs.get('message_id')).delete()
        messages.error(request, 'Шаблон сообщения успешно удален')
        return redirect('main:management-message-list')


class ManagementNotificationView(ListView, BaseView):
    model = Notification
    context_object_name = 'objects'
    paginate_by = settings.PAGINATION
    template_name = 'management/notification.html'
    extra_context = {'title': 'Уведомления'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if creator := self.request.GET.get('creator'):  # Кто
            qs = qs.filter(created_by__pk=creator)
        if whom := self.request.GET.get('whom'):  # Кому
            qs = qs.filter(user__pk=whom)
        if t := self.request.GET.get('type'):  # Тип
            qs = qs.filter(type=t)
        if date := self.request.GET.get('date'):
            qs = qs.filter(created_at__date=datetime.strptime(date, '%Y-%m-%d').date())
        return qs
