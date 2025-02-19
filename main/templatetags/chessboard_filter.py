from django import template

register = template.Library()

@register.filter(name='type_of')
def type_of(value):
    return type(value).__name__

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, None)
