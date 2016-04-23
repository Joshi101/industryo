from django import template
# from django.template.defaultfilters import stringfilter
# from django.utils.safestring import mark_safe
# from django.utils.html import urlize as urlize_impl


register = template.Library()


def callMethod(obj, methodName):
    method = getattr(obj, methodName)

    if "__callArg" in obj.__dict__:
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()


def args(obj, arg):
    if "__callArg" not in obj.__dict__:
        obj.__callArg = []

    obj.__callArg += [arg]
    return obj

register.filter("call", callMethod)
register.filter("args", args)
