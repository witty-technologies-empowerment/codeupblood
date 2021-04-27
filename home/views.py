from django.shortcuts import render, get_object_or_404
from .models import (
    HomeSlide as HS,
    Feedback as FB,
    Gallery as gal,
    Blog as blogg,
    Campaign as camps,
    RequestAppointment as RA,
    Sponsor as SPO,
    Partner as PAT,
    Gallery as gal,
    Hospital as Hos,
    Category as CAT
)
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

from accounts.models import AccountPath as AP
from donor.models import FAQ as Faq

import requests
import json
import random
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def home(request):
    path = 'None'
    user_login = request.user
    if request.user.is_authenticated:
        check_path = AP.objects.filter(username=user_login)
        for x in check_path:
            path = x.path
        # if path == 'admin':
        #     pass
        # elif path == 'donor':
        #     return HttpResponseRedirect(reverse('donor:home'))
        # else:
        #     # return HttpResponseRedirect(reverse('reci:home'))
        #     pass

    get_slide = HS.objects.all()[:6]
    get_feedback = FB.objects.filter(publish=True)[:5]
    count_donor = FB.objects.filter(publish=True, donor=True).count()
    count_rec = FB.objects.filter(recipient=True).count()
    galleryOne = gal.objects.filter(show=True)[:3]
    galleryTwo = gal.objects.filter(show=True)[3:6]
    get_camp = camps.objects.all()[:5]
    xList = []
    for x in get_camp:
        pkey = x.pk
        date = x.date
        img = x.picture.url
        title = x.title
        shrt_message = x.shrt_message
        start_time = x.start_time
        stop_time = x.stop_time
        location = x.location
        upcoming = x.upcoming
        # current = x.current
        passed = x.passed
        #
        xdate = date.strftime('%d %B, %Y')
        xstart_time = start_time.strftime('%H%p')
        xstop_time = stop_time.strftime('%H%p')
        now = datetime.now()
        ynow = now.strftime('%Y-%m-%d')
        adate = date.strftime('%Y-%m-%d')
        znow = datetime.strptime(ynow, "%Y-%m-%d")
        bdate = datetime.strptime(adate, "%Y-%m-%d")
        if znow == bdate:
            badge = 'primary'
        elif znow > bdate:
            badge = 'danger'
        else:
            if upcoming:
                badge = 'success'

        info = {
            'pkey': pkey,
            'img': img,
            'date': xdate,
            'title': title,
            'shrt_message': shrt_message,
            'start_time': xstart_time,
            'stop_time': xstop_time,
            'location': location,
            'badge': badge,
        }
        xList.append(info)

    data = {
        'get_slide': get_slide,
        'all_feedback': get_feedback,
        'count_donor': count_donor,
        'count_rec': count_rec,
        'galleryOne': galleryOne,
        'galleryTwo': galleryTwo,
        'camps': xList,
        'path': path,
        'saved': 5,
        'happy': 10,
        'happyd': 5,
        'award': 1,
    }
    return render(request, 'home/index.html', data)


def about(request):
    get_feedback = FB.objects.filter(publish=True)[:5]
    count_donor = FB.objects.filter(publish=True, donor=True).count()
    count_rec = FB.objects.filter(publish=True, recipient=True).count()

    #
    data = {
        'all_feedback': get_feedback,
        'count_donor': count_donor,
        'count_rec': count_rec,
        'saved': 5,
        'happy': 10,
        'happyd': 5,
        'award': 1,
    }
    return render(request, 'home/about.html', data)


def contact(request):
    return render(request, 'home/contact.html')


def camp(request):
    get_camp = camps.objects.all()
    spon = SPO.objects.filter(show=True)[:8]
    pathn = PAT.objects.filter(show=True)[:8]
    print(pathn)
    page = request.GET.get('page', 1)
    paginator = Paginator(get_camp, 10)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    data = {
        'allcamp': userList,
        'spon': spon,
        'pathn': pathn,
    }
    return render(request, 'home/camp.html', data)


def camp_view(request):
    return render(request, 'home/camp_view.html')


def blog(request):
    get_blog = blogg.objects.filter(show=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(get_blog, 6)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    data = {
        'allblog': userList
    }
    return render(request, 'home/blog.html', data)


def blog_view(request, shrt, lng):
    blog_view = blogg.objects.filter(shrt_id=shrt, lng_id=lng)
    if not blog_view:
        return render(request, 'home/404.html')
    blog_view_c = blogg.objects.all().count()
    for x in blog_view:
        tag = str(x.tags).split(',')
        pkz = x.pk
        author = x.author
    p_pk = int(pkz-1)
    n_pk = int(pkz+1)
    # get the blog shrt_id
    p_pkz = {'show':False}
    n_pkz = {'show':False}
    if p_pk > 0:
        get_p = blogg.objects.filter(pk=p_pk)
        for zz in get_p:
            p_shrt = zz.shrt_id
            p_lng = zz.lng_id
        p_pkz = {'show':True, 'shrt':p_shrt, 'lng':p_lng}
    if n_pk <= blog_view_c:
        get_p = blogg.objects.filter(pk=n_pk)
        for zxz in get_p:
            n_shrt = zxz.shrt_id
            n_lng = zxz.lng_id
        n_pkz = {'show':True, 'shrt':n_shrt, 'lng':n_lng}
    xLists = []
    for y in range(len(tag)):
        xLists.append(str(tag[y]).strip())
    
    #  for recent post
    __do = True
    yLists = []
    __count = 1
    while __do:
        __key__len = ran_gen(1, '123')
        __key = ran_gen(int(__key__len), '0123456789')
        while __key == 0 or __key == 00 or __key == 000:
            __key = ran_gen(__key__len, '0123456789')
        if __key.startswith('0'):
            __key = __key[:1]
        if __key.startswith('00'):
            __key = __key[:2]
        get_blog = blogg.objects.filter(show=True, pk=__key, author=author)
        if get_blog.exists():
            if __count <= 3:
                for i in get_blog:
                    val = {
                        'title': i.title,
                        'shrt': i.shrt_id,
                        'lng': i.lng_id
                    }
                yLists.append(val)
                __count+=1
            elif __count > 3 and __count < 9:
                __do = False
            else:
                __do = False
    
    ___do = True
    zLists = []
    aLists = []
    ___count = 1
    while  ___do:
        ___key__len = ran_gen(1, '123')
        ___key = ran_gen(int(___key__len), '0123456789')
        while ___key == 0 or ___key == 00 or ___key == 000:
            ___key = ran_gen(___key__len, '0123456789')
        if ___key.startswith('0'):
            ___key = ___key[:1]
        if ___key.startswith('00'):
            ___key = ___key[:2]
        get_blog = blogg.objects.filter(show=True, pk=___key)
        if get_blog.exists():
            if ___count <= 3:
                if int(___key) in aLists:
                    pass
                else:
                    for i in get_blog:
                        val = {
                            'title': i.title,
                            'shrt': i.shrt_id,
                            'lng': i.lng_id,
                            'date':i.xDate,
                        }
                    zLists.append(val)
                    aLists.append(int(___key))
                    ___count+=1
            elif ___count > 3:
                ___do = False
            else:
                ___do = False

    get_tags = blogg.objects.all()
    tLists = []
    for q in get_tags:
        tag = str(q.tags).split(',')
        for y in range(len(tag)):
            tLists.append(str(tag[y]).strip())
    tLists = sorted(tLists)

    eLists = []
    get_cat = CAT.objects.all()
    for j in get_cat:
        count_cat = blogg.objects.filter(category=j.pk).count()
        val = {
            'cat':j.category,
            'no':count_cat
        }
        eLists.append(val)
    # eLists = sorted(eLists)


    data = {
        'blog':blog_view,
        'xLists':xLists,
        'p_pkz':p_pkz,
        'n_pkz':n_pkz,
        'recent':yLists,
        'others':zLists,
        'tags':tLists,
        'cats':eLists
        }
    return render(request, 'home/blog_view.html',  data)


def hos(request):
    get_hos = Hos.objects.filter(show=True)

    return render(request, 'home/hos.html', {'hospital': get_hos})


def gallery(request):
    all_gal = gal.objects.filter(show=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(all_gal, 8)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    data = {
        'getphoto': userList
    }
    return render(request, 'home/gallery.html', data)


def serv(request):
    return render(request, 'home/service.html')


def team(request):
    return render(request, 'home/team.html')


def test(request):
    get_feedback = FB.objects.filter(publish=True)[:5]
    count_donor = FB.objects.filter(publish=True, donor=True).count()
    count_rec = FB.objects.filter(publish=True, recipient=True).count()
    data = {
        'all_feedback': get_feedback,
        'count_donor': count_donor,
        'count_rec': count_rec,
    }
    return render(request, 'home/test.html', data)


def faq(request):
    all_faq = Faq.objects.filter(show_on_home=True)[:8]
    xLists = []
    if all_faq.exists():
        for x in all_faq:
            if x.title.strip().endswith('?'):
                a = len(x.title)
                title = x.title[:int(a)-1]
            else:
                title = x.title
            if int(x.pk) % 2 == 0:
                var = {
                    'idz': ran_gen(6, 'ABCDEFGHIJKLMNPQRSTUVWXYZ'),
                    'path': 'right',
                    'question': title,
                    'answer_one': x.answer_space_one,
                    'answer_two': x.answer_space_two,
                }
                xLists.append(var)
            else:
                var = {
                    'idz': ran_gen(6, 'ABCDEFGHIJKLMNPQRSTUVWXYZ'),
                    'path': 'left',
                    'question': title,
                    'answer_one': x.answer_space_one,
                    'answer_two': x.answer_space_two,
                }
                xLists.append(var)
    a = xLists
    page = request.GET.get('page', 1)
    paginator = Paginator(xLists, 8)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    data = {
        'allfaq': userList,
    }
    return render(request, 'home/faq.html', data)






#================= FUCTIONS =================#
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
