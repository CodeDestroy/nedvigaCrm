import datetime

import requests
from django.conf import settings

from django.core.management import BaseCommand

from main.models.site import BuyObject, ObjectStat


class Command(BaseCommand):
    help = 'Load stats from avito'

    def handle(self, *args, **options):
        response = requests.post('https://api.avito.ru/token/', data={
            'client_id': settings.AVITO_OLD_CLIENT_ID,
            'client_secret': settings.AVITO_OLD_CLIENT_SECRET,
            'grant_type': 'client_credentials',
        })
        # Получаем информацию о пользователе
        user = requests.get('https://api.avito.ru/core/v1/accounts/self',
                            headers={'Authorization': f'Bearer {response.json()["access_token"]}'})

        # Собираем объекты для статистики
        obj_ids = []
        for obj in BuyObject.objects.all():
            if obj.avito_id:
                obj_ids.append(obj.avito_id)

        dt_now = datetime.date.today()
        dt_2 = dt_now - datetime.timedelta(days=2)
        stat_response = requests.post(
            f'https://api.avito.ru/stats/v1/accounts/{user.json()["id"]}/items', json={
                'dateFrom': dt_2.strftime('%Y-%m-%d'),
                'dateTo': dt_now.strftime('%Y-%m-%d'),
                'itemIds': obj_ids
            }, headers={'Authorization': f'Bearer {response.json()["access_token"]}'})
        # Запись статистики в базу
        for item in stat_response.json()['result']['items']:
            try:
                obj = BuyObject.objects.get(avito_id=item['itemId'])
            except BuyObject.DoesNotExist:
                continue
            for stat in item['stats']:
                date = datetime.datetime.strptime(stat['date'], '%Y-%m-%d')
                try:
                    stat_obj = ObjectStat.objects.get(obj=obj, date=date)
                except ObjectStat.DoesNotExist:
                    stat_obj = ObjectStat()
                    stat_obj.obj = obj
                    stat_obj.date = date
                stat_obj.favorites = stat['uniqFavorites']
                stat_obj.contacts = stat['uniqContacts']
                stat_obj.views = stat['uniqViews']
                stat_obj.save()
