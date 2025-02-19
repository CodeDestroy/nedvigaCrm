from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from main.models import Source, Lead, Comment, LeadSource, Notification, User
from main.views import BaseView

class SiteView(BaseView):
    def post(self, request, *args, **kwargs):
        referrer = request.POST.get('referrer')
        if request.POST.get('token') == settings.CRM_TOKEN and (phone := request.POST.get('phone')):
            phone = ''.join(filter(lambda i: i.isdigit(), phone))
            try:
                lead = Lead.objects.get(phone=phone)
                if lead.is_deleted:
                    lead.is_deleted = False
                    lead.save()
                    Comment.objects.create(type='lead', item_id=lead.pk,
                                           text=('Восстановлен из удаленных при заявке с сайта ' + referrer))
                lead.processed = 'redo'
                lead.save()
            except ObjectDoesNotExist:
                lead = Lead()
                lead.phone = phone
                lead.name = request.POST.get('name', 'Заявка с сайта')
                lead.save()
                Comment.objects.create(type='lead', item_id=lead.pk, text=('Контакт создан из заявки с сайта ' + referrer))
            # Прибавляем источник
            if 'client_name' not in request.POST:
                LeadSource.objects.create(lead=lead, source=Source.objects.get(pk=6), utm=request.POST.get('utm'))
            else:
                client_phone = ''.join(filter(lambda i: i.isdigit(), request.POST.get('client_phone')))
                try:
                    client = Lead.objects.get(phone=client_phone)
                    if client.is_deleted:
                        client.is_deleted = False
                        client.save()
                        Comment.objects.create(type='lead', item_id=client.pk,
                                               text=(f'Восстановлен из удаленных при заявке с сайта {referrer}'))
                        #text = f'Сообщение со страницы: {referrer}'
                        #Comment.objects.create(type='lead', item_id=client.pk, text=text)
                    client.processed = 'redo'
                except ObjectDoesNotExist:
                    client = Lead()
                    client.phone = client_phone
                    client.name = request.POST.get('client_name', 'Клиент с сайта')
                    client.save()
                    Comment.objects.create(type='lead', item_id=client.pk, text=('Контакт создан из заявки с сайта ' + referrer))
                    user = User.objects.get(pk=59)
                    #Если от втб 
                    if (request.POST.get('phone') == "79688617915"):
                        Notification.objects.create(name=f"эксперт инвест втб", text="Не забудьте посмотреть", priority='danger', user=user, type='lead', item_id=client.pk)
                # TODO: если придет заявка на клиента с номером, то игнорируем
                if not client.client:
                    client.client = lead
                client.save()
                LeadSource.objects.create(lead=client, source=Source.objects.get(pk=22720), utm=request.POST.get('utm'))
                #if (lead.phone == "79688617915"):
                
                
            text = f'Сообщение со страницы: {request.POST.get("previously")}'
            if msg := request.POST.get('message'):
                text += f'<br>Сообщение {msg}'
            if msg := request.POST.get('text'):
                text += f'<br>{msg}'
            if msg := request.POST.getlist('type'):
                text += '<br>Интересующее жилье: '
                text += '; '.join(msg)
            if msg := request.POST.getlist('year'):
                text += '<br>Срок сдачи: '
                text += '; '.join(msg)
            if msg := request.POST.getlist('budget'):
                text += '<br>Бюджет на покупку: '
                text += '; '.join(msg)
            if msg := request.POST.getlist('opinion'):
                text += '<br>Важные особенности: '
                text += '; '.join(msg)
            # Какую квартиру хотите продать?
            if sell_type := request.POST.getlist('sell_type'):
                text += '<br>Какую квартиру продают: '
                text += '; '.join(sell_type)
            # Как быстро хотите продать квартиру?
            if speed := request.POST.getlist('speed'):
                text += '<br>Как быстро хотят продать квартиру: '
                text += '; '.join(speed)
            # Нужны ли Вам дополнительные услуги?
            if help_values := request.POST.getlist('help'):
                text += '<br>Нужны ли дополнительные услуги: '
                text += '; '.join(help_values)
            # Тип дома
            if home_type := request.POST.getlist('home_type'):
                text += '<br>Рассматриваемый объект для покупки: '
                text += '; '.join(home_type)
            # Способ связи
            if home_type := request.POST.getlist('home_type'):
                text += '<br>Рассматриваемый объект для покупки: '
                text += '; '.join(home_type)
            Comment.objects.create(type='lead', item_id=lead.pk, text=text)
        return HttpResponse('Ok', content_type="text/plain")
