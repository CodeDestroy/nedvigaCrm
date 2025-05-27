from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from main.models import Source, Lead, Comment, LeadSource
from main.views import BaseView


class LandingView(BaseView):
    def post(self, request, *args, **kwargs):
        if request.POST.get('token') == settings.CRM_TOKEN and (phone := request.POST.get('phone')):
            phone = ''.join(filter(lambda i: i.isdigit(), phone))
            try:
                lead = Lead.objects.get(phone=phone)
                if lead.is_deleted:
                    lead.is_deleted = False
                    lead.save()
                    Comment.objects.create(type='lead', item_id=lead.pk,
                                           text='Восстановлен из удаленных при заявке с kvartiri36')
                lead.processed = 'redo'
                lead.save()
            except ObjectDoesNotExist:
                lead = Lead()
                lead.phone = phone
                lead.name = 'Заявка с сайта'
                lead.save()
                Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт создан из заявки с kvartiri36')
            # Прибавляем источник
            if source := request.POST.get('source'):
                source, _ = Source.objects.get_or_create(name=source)
                LeadSource.objects.create(lead=lead, source=source, utm=request.POST.get('utm'))
            if text := request.POST.get('text'):
                Comment.objects.create(type='lead', item_id=lead.pk, text=text)
        return HttpResponse('Ok', content_type="text/plain")
