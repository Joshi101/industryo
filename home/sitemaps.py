# from django.contrib.sitemaps import GenericSitemap
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from nodes.models import Node
from workplace.models import Workplace
from tags.models import Tags
from products.models import Products
from forum.models import Question
from userprofile.models import UserProfile


class uObj:
    """Object to hold the data for one url in the sitemap"""
    location = 'http://www.corelogs.com'
    lastmod = None
    changefreq = None
    priority = None

    def __init__(self, location):
        super(uObj, self).__init__()
        self.location = self.location + location


def sitemap(request):
    urlset = []
    wp_no, article_no, tag_no, prod_no, q_no, up_no = 0, 0, 0, 0, 0, 0
    workplaces = Workplace.objects.all()
    tags = Tags.objects.all()
    nodes = Node.objects.all()
    userprofiles = UserProfile.objects.all()
    questions = Question.objects.all()
    products = Products.objects.all()
    for wp in workplaces:
        wp_about = uObj(location=reverse('workplace:workplace_profile', kwargs={'slug': wp.slug}))
        urlset.append(wp_about)
        wp_products = uObj(location=reverse('workplace:products', kwargs={'slug': wp.slug}))
        urlset.append(wp_products)
        wp_members = uObj(location=reverse('workplace:members', kwargs={'slug': wp.slug}))
        urlset.append(wp_members)
        wp_activity = uObj(location=reverse('workplace:activity', kwargs={'slug': wp.slug}))
        urlset.append(wp_activity)
        wp_no += 1
    for tag in tags:
        tag_about = uObj(location=reverse('tags:get_tag', kwargs={'slug': tag.slug}))
        urlset.append(tag_about)
        tag_products = uObj(location=reverse('tags:products', kwargs={'slug': tag.slug}))
        urlset.append(tag_products)
        tag_companies = uObj(location=reverse('tags:companies', kwargs={'slug': tag.slug}))
        urlset.append(tag_companies)
        tag_leads = uObj(location=reverse('tags:leads', kwargs={'slug': tag.slug}))
        urlset.append(tag_leads)
        tag_no += 1
    for prod in products:
        prod_link = uObj(location=reverse('products:product', kwargs={'slug': prod.slug}))
        urlset.append(prod_link)
        prod_no += 1
    for node in nodes:
        if node.category == 'A':
            node_link = uObj(location=reverse('nodes:node', kwargs={'slug': node.slug}))
            urlset.append(node_link)
            article_no += 1
    for q in questions:
        q_link = uObj(location=reverse('forum:question', kwargs={'slug': q.slug}))
        urlset.append(q_link)
        q_no += 1
    for up in userprofiles:
        up_link = uObj(location=reverse('userprofile:profile', kwargs={'slug': up.slug}))
        urlset.append(up_link)
        up_no += 1
    print('Workplace Links: ', wp_no*4)
    print('Tag Links: ', tag_no*4)
    print('Product Links: ', prod_no)
    print('Article Links: ', article_no)
    print('Question Links: ', q_no)
    print('UserProfile Links: ', up_no)
    return render_to_response('sitemap.xml', {'urlset': urlset}, content_type='text/xml')
