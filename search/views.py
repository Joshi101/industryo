from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from workplace.models import Workplace
from products.models import Products
from tags.models import Tags
from forum.models import Question
from nodes.models import Node


def search(request):
    print('GGGGGGGGGGGGGGGGGGGHHHHHHHHHHH')
    querystring = request.GET.get('pre_q').strip()
    terms = None
    if len(querystring) >= 3:
        terms = querystring.split(' ')
    if not terms:
        return HttpResponse('Keep Typing..')
    query = None
    what = request.GET.get('type')
    if not terms:
        return redirect('/search/')
    query = None
    if what == 'questions':
        for term in terms:
            q = Question.objects.filter(Q(title__icontains=term) | Q(question__icontains=term))
    elif what == 'articles':
        for term in terms:
            q = Node.article.filter(Q(title__icontains=term) | Q(post__icontains=term))
    elif what == 'tags':
        for term in terms:
            q = Tags.objects.filter(Q(tag__icontains=term) | Q(description__icontains=term))
    elif what == 'users':
        for term in terms:
            q = User.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term))
    elif what == 'workplaces':
        for term in terms:
            q = Workplace.objects.filter(name__icontains=term)
    elif what == 'products':
        for term in terms:
            q = Products.objects.filter(Q(product__icontains=term) | Q(description__icontains=term))
    else:
        for term in terms:
            q = Question.objects.filter(Q(title__icontains=term) | Q(question__icontains=term))

    if query is None:
        query = q
    else:
        query = query & q
    # query = q
    return render(request, 'search/results.html', locals())


def searchq(request):   # active
    querystring = request.GET.get('the_query').strip()
    terms = None
    if len(querystring) >= 3:
        terms = querystring.split(' ')
    if not terms:
        return render(request, 'search/list.html')

    query = None
    what = request.GET.get('the_type')
    if what == 'questions':
        for term in terms:
            q = Question.objects.filter(Q(title__icontains=term) | Q(question__icontains=term))
            if query is None:
                query = q
            else:
                query = query & q
    elif what == 'articles':
        for term in terms:
            q = Node.article.filter(Q(title__icontains=term) | Q(post__icontains=term))
            if query is None:
                query = q
            else:
                query = query & q
    elif what == 'tags':
        for term in terms:
            q = Tags.objects.filter(Q(tag__icontains=term) | Q(description__icontains=term))
            if query is None:
                query = q
            else:
                query = query & q
    elif what == 'users':
        for term in terms:
            q = User.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term) | Q(username__icontains=term))
            if query is None:
                query = q
            else:
                query = query & q
    elif what == 'workplaces':
        for term in terms:
            q = Workplace.objects.filter(name__icontains=term)
            if query is None:
                query = q
            else:
                query = query & q
    elif what == 'products':            
        for term in terms:
            q = Products.objects.filter(Q(product__icontains=term) | Q(description__icontains=term))
            if query is None:
                query = q
            else:
                query = query & q
    # if query is None:
    #     query = q
    # else:
    #     query = query & q
    return render(request, 'search/list.html', {'query': query, 'what': what})


def forum_search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = 'qusetions'
        if not terms:
            return redirect('/search/')
        query = None
        for term in terms:
            q = Question.objects.filter(Q(title__icontains=term) | Q(detail__icontains=term))

            if query is None:
                query = q
            else:
                query = query & q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')


def article_search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = "articles"
        if not terms:
            return redirect('/search/')
        query = None
        for term in terms:
            q = Node.article.filter(Q(title__icontains=term) | Q(detail__icontains=term))

            if query is None:
                query = q
            else:
                query = query & q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')


def product_search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = "products"
        if not terms:
            return redirect('/search/')
        query = None
        for term in terms:
            q = Products.objects.filter(Q(title__icontains=term) | Q(detail__icontains=term))

            if query is None:
                query = q
            else:
                query = query & q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')


def tag_search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = "tags"
        if not terms:
            return redirect('/search/')
        query = None
        for term in terms:
            q = Tags.objects.filter(Q(tag__icontains=term) | Q(description__icontains=term))

            if query is None:
                query = q
            else:
                query = query & q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')


def user_search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = "user"
        if not terms:
            return redirect('/search/')
        query = None
        for term in terms:
            q = User.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term)) | Q(username__icontains=term)

            if query is None:
                query = q
            else:
                query = query & q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')


def workplace_search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = "workplace"
        if not terms:
            return redirect('/search/')
        query = None
        for term in terms:
            q = Workplace.objects.filter(name__icontains=term)

            if query is None:
                query = q
            else:
                query = query & q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')
