from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from main.forms import UserForm, UserUpdateForm
from main.models import User
from main.views import BaseView


class UserListView(ListView, BaseView):
    model = User
    context_object_name = 'users'
    paginate_by = settings.PAGINATION
    template_name = 'user/list.html'
    extra_context = {'title': 'Пользователи'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['admin_links'] = [{
                'url': reverse('main:user-create'), 'text': '<i class="ti ti-plus icon"></i> Добавить пользователя',
                'class': 'btn btn-success',  'get': reverse('main:modal-user-create')}]
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if text := self.request.GET.get('text'):
            qs = qs.filter(Q(first_name__icontains=text) | Q(last_name__icontains=text) | Q(phone__icontains=text))
        if self.request.GET.get('fired'):
            qs = qs.filter(fired=True)
        return qs


class UserCreateView(CreateView, BaseView):
    model = User
    template_name = 'base_form.html'
    form_class = UserForm
    extra_context = {'title': 'Создание пользователя'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно создан')
        return super().form_valid(form)


class UserUpdateView(UpdateView, BaseView):
    model = User
    template_name = 'base_form.html'
    pk_url_kwarg = 'user_id'
    form_class = UserUpdateForm
    extra_context = {'title': 'Обновление пользователя'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied()
        return super().dispatch(request, args, kwargs)

    def form_valid(self, form):
        messages.warning(self.request, 'Пользователь успешно обновлен')
        return super().form_valid(form)
