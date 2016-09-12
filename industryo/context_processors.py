from django.conf import settings


def res_urls(request):
    return {
        'media_url': settings.MEDIA_URL
    }


def default_images(request):
    return {
        'blank_gif': "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    }
