import json
import logging
from json import JSONDecodeError

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError, HttpResponse

from main.models import Lead, Comment, WhatsappMessage
from main.views import BaseView

logger = logging.getLogger(__name__)


class WhatsappApiView(BaseView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (JSONDecodeError, TypeError):
            return HttpResponseServerError('Json decode exit with error', content_type="text/plain")
        empty_messages = False
        if 'messages' in data:
            for msg in data['messages']:
                if not msg['isEcho'] or ('authorName' in msg and msg['authorName'] != 'Admin'):
                    try:
                        lead = Lead.objects.get(phone=msg['chatId'])
                        lead.processed = 'redo'
                        lead.save()
                    except ObjectDoesNotExist:
                        lead = Lead()
                        lead.phone = msg['chatId']
                        lead.save()
                        Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт создан из Whatsapp')
                    Comment.objects.create(type='lead', item_id=lead.pk,
                                           text=f'Входящее сообщение в whatsapp:<br><b>"{msg["text"] or msg["contentUri"]}"</b>')

                    whatsapp_msg = WhatsappMessage()
                    whatsapp_msg.message_id = msg['messageId']
                    whatsapp_msg.body = msg['text'] or msg['contentUri']
                    whatsapp_msg.type = 'chat'
                    whatsapp_msg.direction = 'in'
                    whatsapp_msg.lead = lead
                    whatsapp_msg.status = 'delivered'
                    whatsapp_msg.save()
            else:
                empty_messages = True

        empty_statuses = False
        if 'statuses' in data:
            for status in data['statuses']:
                try:
                    whatsapp_msg = WhatsappMessage.objects.get(message_id=status['messageId'])
                    whatsapp_msg.status = status['status']
                    whatsapp_msg.save()
                except ObjectDoesNotExist:
                    logger.warning(f'Whatsapp сообщение с ID: {status["messageId"]}, не найдено в базе')
            else:
                empty_statuses = True

        if empty_messages and empty_statuses:
            logger.error(f'Неизвестное событие на Whatsapp webhook: {request.body}')

        return HttpResponse('Ok', content_type="text/plain")
