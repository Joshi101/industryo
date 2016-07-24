from django.contrib.sitemaps import Sitemap
from nodes.models import Node

class WpSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        return Node.objects.all()

    def location(self, obj):
        # return reverse(workplace.views_new.workplace_profile, kwargs={'slug':obj.slug})
        return obj.slug
