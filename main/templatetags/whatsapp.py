from django import template
from django.template import Template, Context

register = template.Library()


@register.simple_tag(name='tpl')
def render_str(tpl, lead, manager):
    return Template(tpl.text).render(Context({'name': manager.__str__(), 'client_name': lead.__str__()}))
