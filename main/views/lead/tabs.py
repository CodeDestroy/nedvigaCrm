from itertools import chain

from django.shortcuts import get_object_or_404, render

from main.forms import CommentForm, LeadSourceForm, QuestionsForm, PassportForm
from main.models import Lead, MessageTemplate
from main.views import BaseView


class BaseTabLeadView(BaseView):
    lead = None

    def dispatch(self, request, *args, **kwargs):
        self.lead = get_object_or_404(Lead, pk=self.kwargs.get('lead_id'))
        return super().dispatch(request, args, kwargs)


class ActivityTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/activity.html'

    def get(self, request, *args, **kwargs):
        activity = list(chain(self.lead.comments(), self.lead.calls()))
        activity.sort(key=lambda x: x.created_at, reverse=True)
        return render(request, self.template_name, {
            'activity': activity, 'comment_form': CommentForm(), 'lead': self.lead})


class SourceTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/source.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'source_form': LeadSourceForm(initial={'lead': self.lead}), 'lead': self.lead})


class QuestionsTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/questions.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'questions_form': QuestionsForm(instance=self.lead.questions if hasattr(self.lead, 'questions') and self.lead.questions is not None else None), 'lead': self.lead})


class PassportTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/passport.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'passport_form': PassportForm(instance=self.lead.passport if hasattr(self.lead, 'passport') and self.lead.passport is not None else None), 'lead': self.lead})


class TasksTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/tasks.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'lead': self.lead})


class ShowsTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/shows.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'lead': self.lead})


class WhatsappTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/whatsapp.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'lead': self.lead, 'templates': MessageTemplate.objects.all()})


class CallsTabLeadView(BaseTabLeadView):
    template_name = 'lead/tabs/calls.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'lead': self.lead})
