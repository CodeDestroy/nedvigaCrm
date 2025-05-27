from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from main.models import Call, Lead, Comment, User
from main.views import BaseView


class CallListView(ListView, BaseView):
    model = Call
    context_object_name = 'calls'
    paginate_by = settings.PAGINATION
    template_name = 'call/list.html'
    extra_context = {'title': 'Список всех звонков'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['users'] = User.objects.filter(Q(fired=False) | Q(return_to_list=True), can_be_responsible=True)
        return context

    def get_queryset(self):
        # Если пользователь не админ, даем ему смотреть только свои звонки
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        if user := self.request.GET.get('user'):
            qs = qs.filter(user__pk=user)
        if date := self.request.GET.get('date'):
            qs = qs.filter(created_at__date=datetime.strptime(date, '%Y-%m-%d').date())
        if t := self.request.GET.get('type'):
            qs = qs.filter(direction=t)
        return qs


class CallMissedListView(ListView, BaseView):
    model = Call
    context_object_name = 'calls'
    paginate_by = settings.PAGINATION
    template_name = 'call/list.html'
    extra_context = {'title': 'Пропущенные звонки'}

    def get_queryset(self):
        return super().get_queryset().filter(Q(direction='in', status='Missed') | Q(direction__isnull=True, status__isnull=True), processed=False).distinct()


class CallProcessedView(BaseView):
    def get(self, request, *args, **kwargs):
        call = get_object_or_404(Call, pk=kwargs.get('call_id'))
        call.processed = True
        call.save()
        for lead in Lead.objects.filter(phone=call.phone):
            if not lead.first_manager:
                lead.first_manager = self.request.user
            if not lead.responsible:
                lead.responsible = self.request.user
                Comment.objects.create(type='lead', item_id=lead.pk, text=f'Добавлен ответственный <b>{self.request.user}</b>')
            lead.save()
        messages.error(request, 'Звонок изменил статус на предобработано')
        return redirect('main:call-missed')

