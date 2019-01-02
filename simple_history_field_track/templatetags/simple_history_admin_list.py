import datetime

import jdatetime
from django import template

register = template.Library()


@register.inclusion_tag("simple_history_field_track/_object_history_list.html",
                        takes_context=True)
def display_list(context):
    return context


def fa_datetime_filter(value, date_format='%Y/%m/%d ساعت %H:%M:%S'):

    if isinstance(value, datetime.datetime):
        value = jdatetime.datetime.fromgregorian(datetime=value)

    if not isinstance(value, jdatetime.datetime):
        raise Exception("Value type is not valid.")

    return value.strftime(date_format)
