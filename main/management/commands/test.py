from django.core.management import BaseCommand
from django.db.models import Q

from main.models import Lead, Comment


class Command(BaseCommand):
    help = 'set tasks to ROP'

    def handle(self, *args, **options):
        with open('/var/www/crm/main/management/commands/data.txt', 'w') as f:
            for l in Lead.objects.distinct('pk').filter(pk__in=Comment.objects.values_list('item_id', flat=True).filter(Q(text__icontains='Z-') | Q(text__icontains=' таун') | Q(text__icontains='Z ') | Q(text__icontains='-таун') | Q(text__icontains='town') | Q(text__icontains=' town') | Q(text__icontains='-town'), type='lead')):
                f.write(f'https://crm.квартиры36.рф/lead/{l.id}/\n')
            f.close()
