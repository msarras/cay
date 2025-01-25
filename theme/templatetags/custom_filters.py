from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def duration_in_hours(duration):
    if duration:
        return duration.total_seconds() / 3600
    return 0


@register.filter
def format_duration(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days > 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

        return ', '.join(parts) if parts else '0 minutes'
    return value  # Return the original value if it's not a timedelta
