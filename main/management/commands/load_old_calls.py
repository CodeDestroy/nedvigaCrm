import requests
from django.conf import settings
from django.db import connection
from django.core.management import BaseCommand

from main.models import Call


class Command(BaseCommand):
    help = 'Load calls from avito'

    def handle(self, *args, **options):
        response = requests.get(f'{settings.DOM_RU_ADDRESS}/crmapi/v1/history/json',
                                params={'start': '20240702T000000Z', 'user': 'yuliya_vyrodova'},
                                headers={'X-API-KEY': settings.DOM_RU_KEY})
        with connection.cursor() as cursor:
            for call in response.json():
                try:
                    cursor.execute(
                        'INSERT INTO calls (direction, uuid, status, event, record, phone, ext, user_id, created_at, updated_at, processed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                        [call['type'], call['uid'], status(call['status']), event(call['status'], call['type']), call['record'] if 'record' in call else None, call['client'], '308', 86, call['start'], call['start'], True])
                except:
                    try:
                        c = Call.objects.get(uuid=call['uid'])
                        c.direction = call['type']
                        c.status = status(call['status'])
                        c.event = event(call['status'], call['type'])
                        c.record = call['record'] if 'record' in call else None
                        c.phone = call['client']
                        c.ext = '308'
                        c.user_id = 86
                        c.save()
                    except Call.DoesNotExist:
                        pass


def status(string):
    match string:
        case 'success':
            return 'Success'
        case 'missed':
            return 'Missed'
        case 'noanswer':
            return 'Cancel'


def event(string, direction):
    match string:
        case 'success':
            return 'COMPLETED'
        case 'missed':
            return 'INCOMING' if direction == 'in' else 'OUTGOING'
        case 'noanswer':
            return 'CANCELLED'
