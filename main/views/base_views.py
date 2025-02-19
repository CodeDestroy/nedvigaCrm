from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator, classonlymethod
from django.http import Http404
from django.views import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin, MultipleObjectMixin
from django.utils.translation import gettext as _


class BaseView(View):
    http_method_names = ['get', 'post']
    view_is_async = True

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = True
        return view

    @method_decorator(login_required)
    def __call__(self, request, *args, **kwargs):
        self.setup(request, *args, **kwargs)
        if request.user.fired:
            return redirect('main:fired')
        return self.dispatch(request, *args, **kwargs)


class BaseListView(MultipleObjectTemplateResponseMixin, MultipleObjectMixin, BaseView):
    http_method_names = ['get']
    object_list = None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset, it's better to do a cheap query than to load the
            # unpaginated queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.')
                              % {'class_name': self.__class__.__name__,})
        context = self.get_context_data()
        return self.render_to_response(context)


class BaseDetailView(SingleObjectTemplateResponseMixin, SingleObjectMixin, BaseView):
    http_method_names = ['get']
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
