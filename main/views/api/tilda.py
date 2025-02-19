import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseServerError

from main.models import Source, Lead, Comment, LeadSource
from main.views import BaseView


logger = logging.getLogger(__name__)


class TildaView(BaseView):
    def post(self, request, *args, **kwargs):
        if request.POST.get('tilda') == 'GYwygOtNH6' and (phone := request.POST.get('Phone')):
            phone = ''.join(filter(lambda i: i.isdigit(), phone))
            landing_name = 'Tilda'
            match request.POST.get('formid'):
                case 'form655649318':
                    landing_name += ' Недорого'
                case 'form661167056':
                    landing_name += ' Комфорт'
                case 'form661167305':
                    landing_name += ' Новостройки'
                case 'form661167118':
                    landing_name = ' Семья'
            source = Source.objects.get_or_create(name=landing_name)[0]

            comment_text = 'В лендинге была указана следующая информация:<br>'
            if value := request.POST.get('Какое_жилье_Вы_ищете'):
                comment_text += f'<b>Тип квартиры</b><br>{value.replace("; ", "<br>")}<br>'
            if value := request.POST.get('City_area'):
                comment_text += f'<b>Район</b><br>{value.replace("; ", "<br>")}<br>'
            if value := request.POST.get('City_area_2'):
                comment_text += f'<b>Сдача объекта</b><br>{value.replace("; ", "<br>")}<br>'
            if value := request.POST.get('City_area_3'):
                comment_text += f'<b>Цена</b><br>{value.replace("; ", "<br>")}<br>'
            if value := request.POST.get('City_area_4'):
                comment_text += f'<b>Дополнительные особенности</b><br>{value.replace("; ", "<br>")}<br>'

            try:
                lead = Lead.objects.get(phone=phone)
                lead.processed = 'redo'
                lead.save()
                if lead.is_deleted:
                    lead.is_deleted = False
                    lead.save()
                    Comment.objects.create(type='lead', item_id=lead.pk,
                                           text='Восстановлен из удаленных при заявке с лендинга')
            except ObjectDoesNotExist:
                lead = Lead()
                lead.phone = phone
                if name := request.POST.get('Name'):
                    lead.name = name
                lead.save()
                Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт создан из заявки с лендинга')
            # Прибавляем источник
            LeadSource.objects.create(lead=lead, source=source)

            comment = Comment()
            comment.type = 'lead'
            comment.item_id = lead.pk
            if name := request.POST.get('Name'):
                comment.text = f'Заявка с лендинга на обратный звонок. Указанно имя: {name}<br>{comment_text}<br>Источник: <b>{landing_name}</b>'
            else:
                comment.text = f'Заявка с лендинга на обратный звонок.<br>{comment_text}<br>Источник: <b>{landing_name}</b>'
            comment.save()
            return HttpResponse('Ok', content_type="text/plain")
        logger.error(f'Пришел запрос из tilda: {request.body}')
        logger.error(f'POST из tilda: {request.POST}')
        logger.error(f'GET из tilda: {request.GET}')
        return HttpResponseServerError('Bad Request', content_type="text/plain")
