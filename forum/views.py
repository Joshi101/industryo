from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, RequestContext
from django.template.loader import render_to_string
from forum.models import *
from tags.models import Tags
from workplace.models import Workplace
from forum.forms import AskForm
from activities.models import *
import json
from nodes.models import Comments
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def ask(request):
    form = AskForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'forum/ask.html', {'form': form})
        else:
            question = request.POST.get('question')
            title = form.cleaned_data.get('title')
            user = request.user
            anonymous = request.POST.get('anonymous')
            category = request.POST.get('category')
            if anonymous:
                question = Question(question=question, title=title, user=user, anonymous=True, category=category)
            else:
                question = Question(question=question, title=title, user=user, category=category)
            question.save()
            image0 = request.FILES.get('image0', None)
            image1 = request.FILES.get('image1', None)
            image2 = request.FILES.get('image2', None)
            if image0:
                i = Images()
                a = i.upload_image(image=image0, user=user)
                question.images.add(a)
            if image1:
                i = Images()
                a = i.upload_image(image=image1, user=user)
                question.images.add(a)
            if image2:
                i = Images()
                a = i.upload_image(image=image2, user=user)
                question.images.add(a)
            tags = request.POST.get('tag')
            print(tags)
            question.set_tags(tags)
            slug = question.slug
            return HttpResponseRedirect('/forum/'+slug)
    else:
        return render(request, 'forum/ask.html', {'form': form})


def edit_ques(request, id):
    q = Question.objects.get(id=id)
    if request.method == 'POST':
        user = request.user
        q.question = request.POST['question']
        q.title = request.POST['title']
        q.save()
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if image0:
            i = Images()
            a = i.upload_image(image=image0, user=user)
            q.images.add(a)
        if image1:
            i = Images()
            a = i.upload_image(image=image1, user=user)
            q.images.add(a)
        if image2:
            i = Images()
            a = i.upload_image(image=image2, user=user)
            q.images.add(a)
        tags = request.POST.get('tag')
        q.set_tags(tags)
        slug = q.slug
        return HttpResponseRedirect('/forum/'+slug)
    return render(request, 'forum/edit_q.html', locals())


def get_question(request, slug):
    q = Question.objects.get(slug=slug)
    comments = Comments.objects.filter(question=q.id)
    answers = Answer.objects.filter(question=q.id)
    show_ans = request.GET.get('answers', None)
    write_ans = request.GET.get('write', None)
    tags = q.tags.all()
    # user = q.user
    return render(request, 'forum/quest.html', locals())

@login_required
def ques_comment(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        comment = request.POST['comment']
        id = request.POST['id']
        question = Question.objects.get(id=id)
        comment = Comments(question=question, user=user, comment=comment)
        comment.save()
        user.userprofile.notify_q_commented(question=question)
        user.userprofile.notify_also_q_commented(question=question)
        r_elements = ['comments']
        r_html['comments'] = render_to_string('snippets/comment.html', {'comment':comment})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def ans_comment(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        comment = request.POST['comment']
        id = request.POST['id']
        answer = Answer.objects.get(id=id)
        user = request.user
        c = Comments(answer=answer, comment=comment, user=user)
        c.save()
        user.userprofile.notify_a_commented(answer)
        user.userprofile.notify_also_a_commented(answer=answer)
        r_elements = ['comments']
        r_html['comments'] = render_to_string('snippets/comment.html', {'comment':c})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        print('problem hai')


@login_required
def voteup(request):
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        print("question found")
        user = request.user
        try:
            vote = Activity.objects.get(user=user, question=question, activity='U')
            vote.delete()
            user.userprofile.unotify_q_upvoted(question)
            print('notification deleted')
            question.votes -=1
            question.save()
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='U')
            vote.save()
            user.userprofile.notify_q_upvoted(question)
            print('notification created')
            question.votes +=1
            question.save()
        return HttpResponse()
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='U')
            vote.delete()
            user.userprofile.unotify_a_upvoted(answer)
            answer.votes -= 1
            answer.save()
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='U')
            vote.save()
            user.userprofile.notify_a_upvoted(answer)
            answer.votes += 1
            answer.save()
        return HttpResponse()

@login_required
def votedown(request):
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, question=question, activity='D')
            vote.delete()
            user.userprofile.unotify_q_downvoted(question)
            question.votes += 1
            question.save()
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='D')
            vote.save()
            user.userprofile.notify_q_downvoted(question)
            question.votes -= 1
            question.save()
        return HttpResponse()
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='D')
            vote.delete()
            print('123456')
            user.userprofile.unotify_a_downvoted(answer)
            print('123457')
            answer.votes += 1
            answer.save()
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='D')
            vote.save()
            print('123458')
            user.userprofile.notify_a_downvoted(answer)
            print('123459')
            answer.votes -= 1
            answer.save()
        return HttpResponse()

@login_required
def reply(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        ans = request.POST['answer']
        user = request.user
        id = request.POST['id']
        question = Question.objects.get(id=id)
        question.answered = True
        slug = question.slug
        anonymous = request.POST.get('anonymous')
        edit = request.POST.get('edit')
        if edit == 'true':
            aid = request.POST.get('aid')
            answer = Answer.objects.get(id=aid)
            answer.answer = ans
            if anonymous:
                answer.anonymous=True
            else:
                answer.anonymous=False
            answer.save()
            image0 = request.FILES.get('image0', None)
            image1 = request.FILES.get('image1', None)
            image2 = request.FILES.get('image2', None)
            if image0:
                i = Images()
                a = i.upload_image(image=image0, user=user)
                answer.images.add(a)
            if image1:
                i = Images()
                a = i.upload_image(image=image1, user=user)
                answer.images.add(a)
            if image2:
                i = Images()
                a = i.upload_image(image=image2, user=user)
                answer.images.add(a)
        else:
            if anonymous:
                answer = Answer.objects.create(answer=ans, user=user, question=question, anonymous=True)
            else:
                answer = Answer.objects.create(answer=ans, user=user, question=question)
            user.userprofile.notify_answered(question)
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if image0:
            i = Images()
            a = i.upload_image(image=image0, user=user)
            answer.images.add(a)
        if image1:
            i = Images()
            a = i.upload_image(image=image1, user=user)
            answer.images.add(a)
        if image2:
            i = Images()
            a = i.upload_image(image=image2, user=user)
            answer.images.add(a)
        r_elements = ['answers']
        r_html['answers'] = render_to_string('snippets/one_answer.html', {'q': question, 'a':answer})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        print('problem hai')


def tag(request):           # this for what
    if request.method == 'POST':
        t = request.POST['tag']
        tag, created = Tags.objects.get_or_create(tag=t)
        return tag
    else:
        t = request.GET['tag']
        tag = Tags.objects.get(tag=t)
        return tag


def question_tagged(request):
    if 'tag' in request.GET:
        questions = None

        tag = request.GET['tag']
        tags = tag.strip()
        tag_list = tags.split(' ')
        for ta in tag_list:

            t = Tags.objects.get(tag=ta)
            q = Question.objects.filter(tags=t.id)
            if questions is None:
                questions = q
            else:
                questions = questions | q

        return render(request, 'forum/questions.html', locals())
    else:
        return render(request, 'forum/questions.html')

# @login_required

def questions(request):
    questions = Question.objects.all().select_related('user__userprofile__workplaceprofile').order_by('-date')
    user = request.user
    if user.is_authenticated():
        if user.userprofile.primary_workplace:
            t = user.userprofile.primary_workplace.workplace_type
            workplaces = Workplace.objects.filter(workplace_type=t).order_by('?')[:5]           # change it soon
        else:
            workplaces = Workplace.objects.all().order_by('?')[:5]          # change it soon
    else:
        workplaces = Workplace.objects.all().order_by('?')[:5]          # change it soon
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
        return
            # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
    else:
        # return render(request, 'home.html', {'result_list': result_list})
        return render(request, 'forum/questions.html', {'result_list': result_list, 'workplaces':workplaces})


def w_questions(request):           # for team
    user = request.user
    wt = user.userprofile.primary_workplace.workplace_type
    questions = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=wt)

    return render(request, 'forum/questions.html', locals())


def s_questions(request):           # for segments
    user = request.user
    workplace = user.userprofile.primary_workplace
    segments = workplace.segments.all()
    questions = None
    for segment in segments:
        q = Question.objects.filter(Q(tags=segment) | Q(user__userprofile__primary_workplace__segments=segments))

        if questions is None:
            questions = q
        else:
            questions = questions & q

    return render(request, 'forum/questions.html', locals())


def delete_question(request):
    id = request.GET.get('id')
    question = Question.objects.get(id=id)
    if request.user == questions.user:
        question.delete()
    return redirect('/forum')


def delete_answer(request):
    id = request.GET.get('id')
    answer = Answer.objects.get(id=id)
    if request.user == answer.user:
        answer.delete()
    return redirect('/forum')


def delete_question_image(request):
    qid = request.GET.get('qid')
    pid = request.GET.get('pid')
    image = Images.objects.get(id=pid)
    question = Question.objects.get(id=qid)
    question.images.remove(image)
    return 0


def category(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        if querystring == 't':
            questions = Question.objects.filter(category=1)
        elif querystring == 'g':
            questions = Question.objects.filter(category=0)
        elif querystring == 'unanswered':
            questions = Question.objects.filter(answered=False)
        elif querystring == 'sae':
            questions = Question.objects.filter(user__userprofile__primary_workplace__workplace_type='C')
        elif querystring == 'scholar':
            questions = Question.objects.filter(user__userprofile__primary_workplace__workplace_type='O')
        elif querystring == 'sme':
            questions = Question.objects.filter(user__userprofile__primary_workplace__workplace_type='B')
        elif querystring == 'lsi':
            questions = Question.objects.filter(user__userprofile__primary_workplace__workplace_type='A')
        paginator = Paginator(questions, 5)
        page = request.GET.get('page')
        workplaces = Workplace.objects.all().order_by('?')[:5]
        try:
            result_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result_list = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            return
            # result_list = paginator.page(paginator.num_pages)
        if page:
            return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
        else:
            # return render(request, 'home.html', {'result_list': result_list})
            return render(request, 'forum/questions.html', {'result_list': result_list, 'workplaces': workplaces})


def q_tags(request):
    q_tag = Tags.objects.all().order_by('-count')
    paginator = Paginator(q_tag, 30)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'forum/20_tags.html', {'result_list': result_list})
    else:
        # return render(request, 'home.html', {'result_list': result_list})
        return render(request, 'forum/q_tags.html', {'result_list': result_list})
    # return render(request, 'forum/q_tags.html', locals())

# def un


def set_things_right(request):
    questions = Question.objects.all()

    for question in questions:
        if question.get_answer_count() >0:
            question.answered=True
            question.save()
    return redirect('/')


def popular(request):
    questions = Question.objects.all().order_by('-votes')[:5]
    return questions



