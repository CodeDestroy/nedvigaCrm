from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from main.forms import CommentForm
from main.models import Comment, Lead, Deal, Task, Showing
from main.views import BaseView


class CommentCreateView(CreateView, BaseView):
    model = Comment
    form_class = CommentForm
    template_name = 'base_form.html'
    extra_context = {'title': 'Создание комментария'}

    def form_valid(self, form):
        match self.kwargs.get('type'):
            case 'lead':
                item = get_object_or_404(Lead, pk=self.kwargs.get('item_id'))
            case 'deal':
                item = get_object_or_404(Deal, pk=self.kwargs.get('item_id'))
            case 'task':
                item = get_object_or_404(Task, pk=self.kwargs.get('item_id'))
            case 'showing':
                item = get_object_or_404(Showing, pk=self.kwargs.get('item_id'))
            case _:
                return HttpResponseBadRequest('Невозможно добавить комментарий куда Вы хотите')
        instance = form.save(commit=False)
        instance.type = self.kwargs.get('type')
        instance.item_id = item.pk
        instance.user = self.request.user
        instance.save()
        messages.success(self.request, 'Комментарий успешно создан')
        return HttpResponseRedirect(item.get_absolute_url())


class CommentUpdateView(UpdateView, BaseView):
    model = Comment
    form_class = CommentForm
    template_name = 'base_form.html'
    pk_url_kwarg = 'comment_id'
    extra_context = {'title': 'Обновление комментария'}

    def form_valid(self, form):
        messages.warning(self.request, 'Комментарий успешно обновлен')
        return super().form_valid(form)


class CommentDeleteView(BaseView):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'), user=request.user)
        comment.deleted = True
        comment.save()
        messages.error(request, 'Комментарий успешно удален')
        try:
            match self.kwargs.get('type'):
                case 'lead':
                    item = Lead.objects.get(pk=comment.item_id)
                case 'deal':
                    item = Deal.objects.get(pk=comment.item_id)
                case 'task':
                    item = Task.objects.get(pk=comment.item_id)
                case 'showing':
                    item = Showing.objects.get(pk=comment.item_id)
                case _:
                    return HttpResponseRedirect(reverse('main:index'))
            return HttpResponseRedirect(item.get_absolute_url())
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('main:index'))
