from django import template
# from django.template.defaultfilters import stringfilter
# from django.utils.safestring import mark_safe
# from django.utils.html import urlize as urlize_impl


register = template.Library()


def new_tab(text):
    return text.replace('<a ', '<a target="_blank" ')
new_tab = register.filter(new_tab)

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