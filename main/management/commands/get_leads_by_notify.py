from asgiref.sync import async_to_sync
from django.urls import reverse
from openpyxl.workbook import Workbook

from django.core.management import BaseCommand

from main.models import Notification, Lead


class Command(BaseCommand):
    help = 'fix sources dates for statistic (use only ONCE)'

    def handle(self, *args, **options):
        print('Вторичка')
        lead_ids = Notification.objects.filter(
            user__funnel_id=2, type='lead', created_at__year=2024, created_at__month=7).values_list('item_id', flat=True)
        lead_ids = set(lead_ids)
        for l in lead_ids:
            try:
                lead = Lead.objects.get(pk=l)
                print(lead, lead.get_absolute_url())
            except Lead.DoesNotExist:
                continue
        print('Ижс')
        lead_ids = Notification.objects.filter(
            user__funnel_id=4, type='lead', created_at__year=2024, created_at__month=7).values_list('item_id', flat=True)
        lead_ids = set(lead_ids)
        for l in lead_ids:
            try:
                lead = Lead.objects.get(pk=l)
                print(lead, lead.get_absolute_url())
            except Lead.DoesNotExist:
                continue
