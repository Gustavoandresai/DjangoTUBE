from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def intcomma(value):
    return '{:,}'.format(value)

@register.filter
def durationformat(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return '{:02d}:{:02d}'.format(minutes, seconds)
    else:
        hours, minutes = divmod(minutes, 60)
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


@register.filter
def wordcount(value):
    return len(value.split())

@register.filter
def truncatewords_html(value, arg):
    from django.template.defaultfilters import truncatewords_html
    return truncatewords_html(value, arg)

@register.filter
def timesince_short(value):
    return timesince(value).split(", ")[0]