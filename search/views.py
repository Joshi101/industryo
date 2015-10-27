from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from workplace.models import Workplace
from products.models import Products
from tags.models import Tags
from forum.models import Question
from nodes.models import Node


def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        terms = querystring.split(' ')
        what = request.GET.get('what')
        if not terms:
            return redirect('/search/')
        if not terms:
            return redirect('/search/')
        query = None
        if what == 'questions':
            for term in terms:
                q = Question.objects.filter(Q(title__icontains=term) | Q(question__icontains=term))
        elif what == 'articles':
            for term in terms:
                q = Node.article.filter(Q(title__icontains=term) | Q(detail__icontains=term))
        elif what == 'tags':
            for term in terms:
                q = Tags.objects.filter(Q(tag__icontains=term) | Q(description__icontains=term))
        elif what == 'users':
            for term in terms:
                q = User.objects.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term)) | Q(username__icontains=term)
        elif what == 'workplaces':
            for term in terms:
                q = Workplace.objects.filter(name__icontains=term)
        elif what == 'products':            
            for term in terms:
                q = Products.objects.filter(Q(title__icontains=term) | Q(detail__icontains=term))
        # if query is None:
        #     query = q
        # else:
        #     query = query & q
        query = q
        return render(request, 'search/results.html', locals())
    else:
        return render(request, 'search/search.html')


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



#