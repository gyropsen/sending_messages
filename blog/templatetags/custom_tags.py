from django import template

register = template.Library()


@register.simple_tag
def media_tag(val):
    if val:
        return f"/media/{val}"
    return '#'
