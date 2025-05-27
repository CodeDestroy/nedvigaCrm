from datetime import datetime
import json
from json import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError, HttpResponse
from django.utils.timezone import make_aware

from main.models import Lead, Comment, WhatsappMessage, Wantresult
from main.views import BaseView


class WantresultView(BaseView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (JSONDecodeError, TypeError):
            return HttpResponseServerError('Json decode exit with error', content_type="text/plain")
        try:
            wantresult = Wantresult.objects.get(
                vid=int(data['vid']), site=data['site'], time=make_aware(datetime.fromtimestamp(int(data['time']))))
        except ObjectDoesNotExist:
            wantresult = Wantresult()
            wantresult.vid = int(data['vid'])
            wantresult.site = data['site']
            wantresult.time = make_aware(datetime.fromtimestamp(int(data['time'])))
            wantresult.save()
        wantresult.num = kwargs.get('num')
        # Пишем инфу, только если создаем новую часть
        if 'page' in data:
            wantresult.page = data['page']
        if 'ref' in data:
            wantresult.ref = data['ref']
        if 'browser' in data:
            wantresult.browser = data['browser']
        if 'device' in data:
            wantresult.device = data['device']
        if 'platform' in data:
            wantresult.platform = data['platform']
        if 'ip' in data:
            wantresult.ip = data['ip']
        if 'comment' in data:
            wantresult.comment = data['comment']
        if 'roistat_visit' in data:
            wantresult.roistat_visit = data['roistat_visit']
        if 'phones' in data:
            wantresult.phones = data['phones']
        if 'mails' in data:
            wantresult.mails = data['mails']
        if 'utm' in data:
            wantresult.utm = data['utm']
        wantresult.save()
        return HttpResponse('Ok', content_type="text/plain")
