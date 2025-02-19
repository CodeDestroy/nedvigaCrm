import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import classonlymethod
from django.views import View

from main.models import Notification
from main.views import BaseView


class FiredView(View):
    view_is_async = True

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = True
        return view

    def get(self, request, *args, **kwargs):
        return render(request, 'pages/fired.html', {'title': 'Ууппсссс… А Вам сюда нельзя'})


class MakeCallView(View):
    view_is_async = True
    url = 'https://vpbx000052233b.domru.biz/crmapi/v1/makecall'

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = True
        return view

    def get(self, request, *args, **kwargs):
        response = requests.post(self.url, headers={'X-API-KEY': settings.DOM_RU_KEY}, data={
            'phone': kwargs.get('phone'), 'user': self.request.user.sip.sip
        })
        if response.status_code < 400:
            return HttpResponse(response.text, content_type='text/plain')
        return HttpResponseServerError(response.text, content_type='text/plain')


class NotifyDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        notify = get_object_or_404(Notification, pk=kwargs.get('notify_id'), user=request.user)
        notify.read = True
        notify.save()
        messages.success(request, 'Уведомление удалено')
        return redirect(self.request.POST.get('next'))
