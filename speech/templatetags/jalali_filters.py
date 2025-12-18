from django import template
import jdatetime

register = template.Library()

@register.filter
def jalali_verbose(value):
    if not value:
        return ""
    if isinstance(value, jdatetime.date):
        return value.strftime("%d %B %Y")
    return value