import logging
from datetime import datetime
import json
from json import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError, HttpResponse
from django.utils.timezone import make_aware

from main.models import Dmp
from main.views import BaseView

logger = logging.getLogger(__name__)


class DmpView(BaseView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (JSONDecodeError, TypeError):
            logger.error(f'Пришел запрос из DMP.ONE: {request.body}')
            logger.error(f'POST из DMP.ONE: {request.POST}')
            logger.error(f'GET из DMP.ONE: {request.GET}')
            return HttpResponseServerError('Json decode exit with error', content_type="text/plain")

        phone = list(data['phone'])
        phone[0] = '7'
        phone = ''.join(phone)

        try:
            dmp = Dmp.objects.get(timestamp=make_aware(datetime.fromtimestamp(int(data['timestamp']))),
                                  visit_id=int(data['visit__id']), phone=phone)
        except ObjectDoesNotExist:
            dmp = Dmp()
            dmp.phone = phone
            dmp.visit_id = int(data['visit__id'])
            dmp.timestamp = make_aware(datetime.fromtimestamp(int(data['timestamp'])))
        if 'website' in data:
            dmp.website = data['website']
        if 'page' in data:
            dmp.page = data['page']
        if 'page_with_parameters' in data:
            dmp.page_with_parameters = data['page_with_parameters']
        if 'yid' in data:
            dmp.yid = data['yid']
        if 'email' in data:
            dmp.email = data['email']
        if 'vk' in data:
            dmp.vk = data['vk']
        if 'fb' in data:
            dmp.fb = data['fb']
        if 'insta' in data:
            dmp.insta = data['insta']
        if 'ok' in data:
            dmp.ok = data['ok']
        if 'utm_source' in data:
            dmp.utm_source = data['utm_source']
        if 'utm_medium' in data:
            dmp.utm_medium = data['utm_medium']
        if 'utm_campaign' in data:
            dmp.utm_campaign = data['utm_campaign']
        if 'utm_term' in data:
            dmp.utm_term = data['utm_term']
        if 'utm_content' in data:
            dmp.utm_content = data['utm_content']
        if 'referer' in data:
            dmp.referer = data['referer']
        if 'ip' in data:
            dmp.ip = data['ip']
        if 'stock_key' in data:
            dmp.stock_key = data['stock_key']
        if 'interests' in data:
            dmp.interests = data['interests']
        dmp.save()
        return HttpResponse('Ok', content_type="text/plain")
