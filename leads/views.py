from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, RequestContext
from django.template.loader import render_to_string
from leads.models import Leads, Reply
import json
import traceback
from nodes.models import Images, Document
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def edit_add_lead(request, slug):
    user = request.user
    wp = user.userprofile.primary_workplace
    response = {}
    if slug == 'new':
        if request.method == 'POST':
            if request.POST.get('lead'):
                l = Leads.objects.create(lead=request.POST['lead'], user=user, workplace=wp)
                response['l_slug'] = l.slug
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            return render(request, 'leads/edit.html')
    else:
        l =Leads.objects.get(slug=slug)
        direct = l._meta.get_all_field_names()
        print(direct)
        dictionary = {}
        if request.method == 'POST' and user == l.user:
            for key in request.POST:
                if key in direct:
                    try:
                        dictionary[key] = request.POST[key]
                    except:
                        tb = traceback.format_exc()
            else:
                if key == 'city':
                    l.set_tags(request.POST[key])

            for key in dictionary:
                setattr(l, key, dictionary[key])
            l.save()
            image1 = request.FILES.get('photo', None)
            if image1:
                i = Images()
                x = i.upload_image(image=image1, user=user)
                l.image = x
                l.save()
            response['l_id'] = l.id

            doc1 = request.FILES.get('doc', None)
            if doc1:
                d = Document()
                x = d.upload_doc(doc=doc1, user=user)
                l.doc = x
                l.save()
            response['l_id'] = l.id
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            dictionary = {'lead': l, 'first_time': True}
            return render(request, 'leads/edit.html', dict(list(l.__dict__.items()) + list(dictionary.items())))


def leads(request):
    # for now just paginate & show all
    leads = Leads.objects.all().order_by('-date')
    paginator = Paginator(leads, 5)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return
    if page:
        return render(request, 'leads/five_leads.html', {'result_list': result_list})
    else:
        # return render(request, 'home.html', {'result_list': result_list})
        return render(request, 'leads/leads.html', {'result_list': result_list})


def get_lead(request, slug):
    lead = Leads.objects.get(slug=slug)
    return render(request, 'leads/lead.html', locals())


def close_lead(request):
    id = request.POST.get('id')
    lead = Leads.objects.get(id=id)
    print(id)
    if request.user == lead.user:
        if lead.status:
            lead.status = False
            lead.save()
        else:
            lead.status = True
            lead.save()
    return HttpResponse


def reply_lead(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = request.user
        wp = user.userprofile.primary_workplace
        lead = Leads.objects.get(id=id)
        # r = Reply()
        # direct = r._meta.get_all_field_names()
        direct = ['message', 'price', 'time_to_deliver', 'taxes', 'delivery_charges', 'payment_terms', 'quality_assurance']
        dictionary = {}

        reply = Reply.objects.create(user=user, workplace=wp, lead=lead)

        for key in request.POST:
            if key in direct:
                try:
                    dictionary[key] = request.POST[key]
                except:
                    tb = traceback.format_exc()
        for key in dictionary:
            setattr(reply, key, dictionary[key])
        reply.save()
        doc1 = request.FILES.get('doc21', None)
        doc2 = request.FILES.get('doc22', None)
        if doc1:
            d = Document()
            x = d.upload_doc(doc=doc1, user=user)
            reply.doc = x
            reply.save()
        if doc2:
            d = Document()
            x = d.upload_doc(doc=doc2, user=user)
            reply.doc = x
            reply.save()

    return redirect('/leads/'+lead.slug)

