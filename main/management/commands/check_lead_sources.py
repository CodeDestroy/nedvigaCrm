import datetime

from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.management import BaseCommand
from django.urls import reverse
from telegram import Bot
from telegram.constants import ParseMode

from main.models import Lead


class Command(BaseCommand):
    help = 'get leads without source'

    def handle(self, *args, **options):
        dt_now = datetime.date.today()
        dt_now = datetime.date(year=dt_now.year, month=dt_now.month, day=1)
        leads = Lead.objects.filter(leadsource__isnull=True, created_at__gte=dt_now,
                                    created_at__lte=datetime.date.today() + datetime.timedelta(days=1))
        lead_links = 'Фамилия;Имя;Отчество;Телефон;Дата создания;Ссылка\n'
        for lead in leads:
            lead_links += f'{lead.surname if lead.surname else ""};{lead.name if lead.name else ""};{lead.patronymic if lead.patronymic else ""};{lead.phone};{lead.created_at};https://crm.квартиры36.рф{reverse("main:lead-page", kwargs={"lead_id": lead.pk})}\n'
        async_to_sync(send_to_group)('*Проверка контактов на отсутствие источников*', lead_links)


async def send_to_group(text, file):
    async with Bot(settings.TELEGRAM_BOT_KEY) as bot:
        # admin user id = 286896743
        await bot.send_document(settings.TELEGRAM_CHAT_ID, caption=text, parse_mode=ParseMode.MARKDOWN_V2,
                                document=bytes(''.join(file), 'cp1251'), filename='leads_without_source.csv')
