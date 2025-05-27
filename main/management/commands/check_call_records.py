import json

import requests
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from telegram import Bot
from telegram.constants import ParseMode

from main.models import Call


class Command(BaseCommand):
    help = 'get history from dom.ru ats'

    def handle(self, *args, **options):
        count = 0
        response = requests.get(f'{settings.DOM_RU_ADDRESS}/crmapi/v1/history/json', headers={
            'X-API-KEY': settings.DOM_RU_KEY}, params={'period': 'this_month', 'type': 'all'})
        if response.status_code != 200:
            async_to_sync(send_to_group)(f'*Ошибка запроса к серверу ОАТС при проверке звонков*\nКод ошибки: `{response.status_code}`\nТекст ошибки: `{response.text}`')
            exit()
        elems = json.loads(response.text)
        if elems:
            for elem in elems:
                print(elem)
                if 'record' in elem and 'uid' in elem:
                    try:
                        call = Call.objects.get(uuid=elem['uid'])
                        if call.record is None:
                            count += 1
                        call.record = elem['record']
                        if 'user' in elem:
                            match elem['user']:
                                case 'director':
                                    call.ext = 300
                                case 'inna_kositsina':
                                    call.ext = 301
                                case 'olga_menyakina':
                                    call.ext = 302
                                case 'mariya_sveshnikova':
                                    call.ext = 303
                                case 'svetlana_pisarevskaya':
                                    call.ext = 305
                                case 'veronika_asfindiyarova':
                                    call.ext = 306
                                case 'oksana_anpilova':
                                    call.ext = 307
                                case 'yuliya_vyrodova':
                                    call.ext = 308
                                case 'avdeev_roman':
                                    call.ext = 309
                                case 'office2-1':
                                    call.ext = 401
                                case 'office2-2':
                                    call.ext = 402
                        call.save()
                    except ObjectDoesNotExist:
                        # async_to_sync(send_to_group)('') Подумать выгружать ли ошибку записи звонков
                        continue
        async_to_sync(send_to_group)(f'*Запрос к серверу ОАТС при проверке звонков*\nБыло загружено `{count}` записей')


async def send_to_group(text):
    async with Bot(settings.TELEGRAM_BOT_KEY) as bot:
        # admin user id = 286896743
        await bot.send_message(settings.TELEGRAM_CHAT_ID, text, parse_mode=ParseMode.MARKDOWN_V2)
