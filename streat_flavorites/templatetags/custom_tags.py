from django import template
from random import sample

register = template.Library()

@register.filter
def random_items(items, count):
    return sample(items, min(len(items), count))
