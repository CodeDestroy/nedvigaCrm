import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseServerError
from django.views import View

from main.models import Call, User


logger = logging.getLogger(__name__)


# Данный файл полностью совместим с Дом РУ АТС 4.0
class CallView(View):
    def post(self, request, *args, **kwargs):
        logger.error(f'Пришел запрос из атс: {request.body}')
        if request.POST.get('crm_token') != settings.CRM_TOKEN:  # АТС прислала неверный токен, мб кто-то пытается стучаться
            logger.error(f'Пришел запрос из атс: {request.body}')
            return HttpResponseServerError('Bad Token', content_type="text/plain")
        if request.POST.get('cmd') in ['history', 'event']:
            try:
                call = Call.objects.get(uuid=request.POST.get('callid'))
            except ObjectDoesNotExist:
                call = Call()
                call.uuid = request.POST.get('callid')
            if type_ := request.POST.get('type'):
                call.event = type_
            if direction := request.POST.get('direction'):
                call.direction = direction
            phone = request.POST.get('phone')
            phone = list(phone)
            phone[0] = '7'
            call.phone = ''.join(phone)
            if ext := request.POST.get('ext'):
                call.ext = ext
                try:
                    call.user = User.objects.get(sip__sip=call.ext)
                except ObjectDoesNotExist:
                    pass
            if status := request.POST.get('status'):
                call.status = status
            if link := request.POST.get('link'):
                call.record = link
            call.save()
        return HttpResponse('Ok', content_type="text/plain")
