from django import template
from num2words import num2words

register = template.Library()

@register.filter
def int_to_words(value):
    try:
        return num2words(value)
    except (TypeError, ValueError):
        return value
