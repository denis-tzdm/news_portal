from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag(takes_context=True)
def pagination_dots_left(context):
    prev_page = context['page_obj'].previous_page_number()
    if prev_page > 2:
        return '…'
    else:
        return ''


@register.simple_tag(takes_context=True)
def pagination_dots_right(context):
    next_page = context['page_obj'].next_page_number()
    last_page = context['page_obj'].paginator.num_pages
    if last_page - next_page > 1:
        return '…'
    else:
        return ''
