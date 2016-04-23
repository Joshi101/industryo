from django import template
# from django.template.defaultfilters import stringfilter
# from django.utils.safestring import mark_safe
# from django.utils.html import urlize as urlize_impl


register = template.Library()


def index(List, i):
    return List[int(i)]
index = register.filter(index)

# def
