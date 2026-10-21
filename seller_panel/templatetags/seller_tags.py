from django import template
from decimal import Decimal

register = template.Library()

def format_inr_value(number):
    
    if number is None or number == '':
        return '0'
    try:
        val = int(round(float(number)))
    except (ValueError, TypeError):
        return str(number)

    s = str(abs(val))
    if len(s) <= 3:
        res = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        res = ','.join(groups) + ',' + last3

    return ('-' if val < 0 else '') + res


@register.filter(name='inr')
def inr_filter(value):
    return format_inr_value(value)


@register.filter(name='currency_inr')
def currency_inr_filter(value):
    return f"₹{format_inr_value(value)}"
