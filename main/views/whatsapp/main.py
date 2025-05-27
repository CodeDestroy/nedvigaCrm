import json
import datetime
import logging
from datetime import timedelta

import requests

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template, Context
from django.urls import reverse

from main.models import Lead, WhatsappMessage, Comment, MessageTemplate
from main.views import BaseView


logger = logging.getLogger(__name__)


class WhatsappView(BaseView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            leads = Lead.objects.distinct().filter(
                responsible=request.user, whatsappmessage__created_at__gte=datetime.date.today() - timedelta(days=10))
        else:
            leads = Lead.objects.distinct().filter(
                whatsappmessage__created_at__gte=datetime.date.today() - timedelta(days=10))
        return render(request, 'whatsup/page.html', {'title': 'Whatsup', 'leads': leads})


class WhatsappSendMessage(BaseView):
    url = f'{settings.WHATSAPP_URL}/message'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {settings.WHATSAPP_TOKEN}'}
    data = {'channelId': settings.WHATSAPP_CHANNEL_ID, 'chatType': 'whatsapp'}

    def post(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs.get('lead_id'))
        self.data['chatId'] = lead.phone
        if (message := request.POST.get('message')) and (file := request.FILES.get('file')):
            if request.POST.get('image_first'):
                self.send_file(lead, file)
                del self.data['contentUri']
                self.send_message(lead, message)
                del self.data['text']
            else:
                self.send_message(lead, message)
                del self.data['text']
                self.send_file(lead, file)
                del self.data['contentUri']
            messages.success(self.request, 'Сообщение успешно отправлено')
        elif message := request.POST.get('message'):
            if self.send_message(lead, message):
                del self.data['text']
                messages.success(self.request, 'Сообщение успешно отправлено')
        elif file := request.FILES.get('file'):
            if self.send_file(lead, file):
                del self.data['contentUri']
                messages.success(self.request, 'Сообщение успешно отправлено')
        else:
            messages.error(self.request, 'Вы не заполнили форму отправки')
        return redirect(request.POST.get('next') or reverse('main:lead-page', kwargs={'lead_id': lead.pk}))

    def send_file(self, lead, file):
        # Сохранение файла
        file = default_storage.save(f'whatsapp/{lead.pk}/{file.name}', file)
        self.data['contentUri'] = f'https://crm.xn--36-6kch5aj8bbq6g.xn--p1ai/media/{file}'
        response = requests.post(self.url, headers=self.headers, json=self.data, verify=False)
        if response.status_code != 200 and response.status_code != 201:
            messages.error(self.request, f'Сообщение не было отправлено из-за ошибки {response.status_code}')
            logger.error(f'Whatsapp: Текст ошибки {response.text}')
            logger.error(f'Whatsapp: Заголовки {self.headers}')
            logger.error(f'Whatsapp: Отправленный запрос {self.data}')
            logger.error(f'Whatsapp: ссылка {self.data["contentUri"]}')
            return False
        response = json.loads(response.text)
        if 'messageId' in response:
            whatsapp_msg = WhatsappMessage()
            whatsapp_msg.message_id = response['messageId']
            whatsapp_msg.body = self.data['contentUri']
            whatsapp_msg.direction = 'out'
            whatsapp_msg.lead = lead
            whatsapp_msg.user = self.request.user
            whatsapp_msg.status = 'sending'
            whatsapp_msg.save()

            if not lead.first_manager:
                lead.first_manager = self.request.user
                lead.save()
            if not lead.responsible:
                lead.responsible = self.request.user
                Comment.objects.create(type='lead', item_id=lead.pk, text=f'Добавлен ответственный <b>{self.request.user}</b> из-за исходящего сообщения в whatsapp')
            Comment.objects.create(type='lead', item_id=lead.pk, text=f'Отправлено сообщение в whatsapp:<br><b>"{self.data["contentUri"]}"</b><br>пользователем: <b>{self.request.user}</b>')
        return True

    def send_message(self, lead, message):
        self.data['text'] = message.replace('xn--36-6kch5aj8bbq6g.xn--p1ai', 'квартиры36.рф').replace('<br>', '\n')
        response = requests.post(self.url, headers=self.headers, json=self.data)
        if response.status_code != 200 and response.status_code != 201:
            messages.error(self.request, f'Сообщение не было отправлено из-за ошибки {response.status_code}')
            logger.error(f'Whatsapp: Текст ошибки {response.text}')
            logger.error(f'Whatsapp: Заголовки {self.headers}')
            logger.error(f'Whatsapp: Отправленный запрос {self.data}')
            return False
        response = json.loads(response.text)
        if 'messageId' in response:
            WhatsappMessage.objects.create(message_id=response['messageId'], body=self.data['text'].replace('\n', '<br>'), direction='out',
                                           lead=lead, user=self.request.user, status='sending')
            if not lead.first_manager:
                lead.first_manager = self.request.user
                lead.save()
            if not lead.responsible:
                lead.responsible = self.request.user
                Comment.objects.create(type='lead', item_id=lead.pk, text=f'Добавлен ответственный <b>{self.request.user}</b> из-за исходящего сообщения в whatsapp')
            Comment.objects.create(type='lead', item_id=lead.pk, text=f'Отправлено сообщение в whatsapp:<br><b>"{self.data["text"]}"</b><br>пользователем: <b>{self.request.user}</b>')
        return True


class WhatsappLeadView(BaseView):
    def get(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs.get('lead_id'))
        return render(request, 'whatsup/user.html', {
            'messages': WhatsappMessage.objects.filter(lead=lead), 'lead': lead,
            'templates': MessageTemplate.objects.all()})


class WhatsappSendTemplate(BaseView):
    url = f'{settings.WHATSAPP_URL}/message'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {settings.WHATSAPP_TOKEN}'}
    data = {'channelId': settings.WHATSAPP_CHANNEL_ID, 'chatType': 'whatsapp'}

    def get(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=kwargs.get('lead_id'))
        tpl = get_object_or_404(MessageTemplate, pk=kwargs.get('template_id'))
        return HttpResponse(Template(tpl.text).render(Context({'name': request.user.__str__(), 'client_name': lead.__str__()})).replace('<br>', '\n'))
