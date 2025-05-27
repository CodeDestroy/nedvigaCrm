from django.http import JsonResponse

from main.views import BaseView


class LeadReportView(BaseView):
    view_is_async = True

    def post(self, request, *args, **kwargs):
        json = {
            'user': request.POST.get('user'),
            'text': request.POST.get('text'),
            'reserve': request.GET.get('reserve'),
            'spam': request.GET.get('spam'),
            'no_source': request.GET.get('no_source'),
            'source': request.GET.get('source'),
            'warm': request.GET.get('warm'),
            'processed': request.GET.get('processed'),
            'paytype': request.GET.get('paytype'),
            'from': request.GET.get('from'),
            'decoration': request.GET.get('decoration'),
            'marital': request.GET.get('marital'),
            'purpose': request.GET.get('purpose'),
            'birth': request.GET.get('birth'),
            'reserved': request.GET.get('reserved'),
            'user_id': request.user.pk,
            'telegram_id': request.user.telegram_id
        }
        from main.tasks import send_lead_report
        send_lead_report.apply_async(args=[json])
        return JsonResponse({'code': 200, 'message': 'Hello, world'})
