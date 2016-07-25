from django.contrib.sitemaps import Sitemap
from nodes.models import Node
from workplace.models import Workplace


class WpSitemap(Sitemap):
    changefreq = "daily"
    priority = 1
    # location = '/'

    def items(self):
        return Workplace.objects.all()

    def location(self, obj):
        # return reverse(workplace.views_new.workplace_profile, kwargs={'slug':obj.slug})
        return obj.slug
