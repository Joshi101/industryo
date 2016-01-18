from django import template
# from django.template.defaultfilters import stringfilter
# from django.utils.safestring import mark_safe
# from django.utils.html import urlize as urlize_impl


register = template.Library()


def index(List, i):
    return List[int(i)]
index = register.filter(index)

# from django import template
# from django.template.defaultfilters import stringfilter
# from django.utils.safestring import mark_safe
# from django.utils.html import urlize as urlize_impl
#
# register = template.Library()
#
# @register.filter(is_safe=True, needs_autoescape=True)
# @stringfilter
# def new_tab(value, limit, autoescape=None):
#     return mark_safe(urlize_impl(value, trim_url_limit=int(limit), nofollow=True, autoescape=autoescape).replace('<a', '<a target="_blank"'))