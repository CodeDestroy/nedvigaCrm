from django import template

from main.models import Deal

register = template.Library()


@register.simple_tag(name='lead_money')
def lead_money(lead, stage):
    money = 0
    deals = Deal.objects.filter(stage=stage, lead__client=lead)
    for deal in deals:
        if deal.price < 4000000:
            money += 2000
        elif 4000000 <= deal.price < 7000000:
            money += 3000
        else:
            money += 5000
    return {'money': money, 'deals': deals.count()}
