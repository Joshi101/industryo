from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(*args, **kwargs):
