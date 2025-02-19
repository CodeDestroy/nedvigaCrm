from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from main.models import Source, Lead, Comment, LeadSource
from main.views import BaseView


class ForumsView(BaseView):
    def post(self, request, *args, **kwargs):
        if request.POST.get('token') == settings.CRM_TOKEN and (phone := request.POST.get('phone')):
            phone = ''.join(filter(lambda i: i.isdigit(), phone))
            try:
                lead = Lead.objects.get(phone=phone)
                if lead.is_deleted:
                    lead.is_deleted = False
                    lead.save()
                    Comment.objects.create(type='lead', item_id=lead.pk,
                                           text='Восстановлен из удаленных при заявке с сайта')
                lead.processed = 'redo'
                lead.save()
            except ObjectDoesNotExist:
                lead = Lead()
                lead.phone = phone
                lead.name = request.POST.get('name')
                #lead.email = request.POST.get('email')
                
                
                lead.save()
                activity = request.POST.get('activity')
                Comment.objects.create(type='lead', item_id=lead.pk,
                                           text=f'Сфера деятельности {activity}')
                Comment.objects.create(type='lead', item_id=lead.pk, text='Контакт создан из регистрации на форуме')
            # Прибавляем источник
            LeadSource.objects.create(lead=lead, source=Source.objects.get(pk=50), utm={
                'forum-name': request.POST.get('forum-name'),
                'name': request.POST.get('name'),
                'phone': request.POST.get('phone'),
                #'email': request.POST.get('email'),
                'utm': request.POST.get('utm')
            })
            text = f'Сообщение со страницы: {request.POST.get("previously")}'

            Comment.objects.create(type='lead', item_id=lead.pk, text=text)
        return HttpResponse('Ok', content_type="text/plain")
