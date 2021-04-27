from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
import random
import string
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from .models import (subAdmin as SA,ActivationCode as AC)
from accounts.models import (AccountPath as AP,)
from donor.models import DonorDetail as DD, NewDonor as ND, Donated as DO, FAQ
from home.models import (
    Partner as PA,
    Sponsor as SP,
    SayHello as SH,
    Subscriber as sub,
    Blog as blogs,
    Category as cate,
    Campaign as Camp,
    Feedback as feeds,
    Gallery as gall,
    HomeSlide as HS,
    Hospital as hos)
from survey.models import Survey as SUR
import timeago
# from donor.views import iniT, HexCode
# Create your views here.


def WAIT(xuser):
    checkStat = SA.objects.filter(user=xuser)
    if checkStat.exists():
        for x in checkStat:
            stat = x.activated
    else:
        stat = None
    return stat


@login_required(login_url='/admin/login')
def SAHome(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_donor = DD.objects.all()
    count = 0
    countd = 0
    for x in all_donor:
        get_this_user = User.objects.filter(username=x.username)
        if get_this_user.exists():
            count = count + 1
        get_this_userd = User.objects.filter(username=x.username,is_active=False)
        if get_this_userd.exists():
            countd = countd + 1
    data = {
        'userCount':count,
        'activeCount':countd,
        'dash_':True,
        # 'init':iniT(user_login),
		# 'hex_number':HexCode(user_login),
    }
    return render(request, 'subadmin/home.html', data)


# @login_required(login_url='/admin/login')
# def SAHome(request):


def SALogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('subadmin:SAHome'))
    else:
        if request.method == 'POST':
            user_name = request.POST.get('username')
            username = str(user_name).lower()
            email = request.POST.get('email')
            pass_word = request.POST.get('password')
            password = str(pass_word).lower()
            try:
                allow = SA.objects.filter(user=username)
                for x in allow:
                    allowed = x.allowed
                if allowed:
                    user = authenticate(username=username, password=password)
                    if user:
                        if user.is_active:
                            login(request, user)
                            c= WAIT(username)
                            if c != None:
                                if c:
                                    return HttpResponseRedirect(reverse('subadmin:SAHome'))
                                else:
                                    logout(request)
                                    url = str('/admin/register/waiting!='+username.lower())
                                    return HttpResponseRedirect(url)
                            else:
                                return HttpResponseRedirect(reverse('subadmin:sareg'))
                        else:
                            error = 'Invalid Login details'
                            context = {
                            'error':error,
                            }
                            return render(request, 'subadmin/login.html', context)
                    else:
                        error = 'Invalid Login details'
                    context = {
                    'error':error,
                    }
                    return render(request, 'subadmin/login.html', context)
                else:
                    error = '403: Access Denied for '+username
                context = {
                'error':error,
                }
                return render(request, 'subadmin/login.html', context)
            except:
                error = '406: Cant process request for '+username
                context = {
                'error':error,
                }
                return render(request, 'subadmin/login.html', context)
        else:
            return render(request, 'subadmin/login.html')


def SAReg(request):
    error = 0
    show = False
    comp = False
    if request.method == 'POST':
        co_de = request.POST.get('code')
        code = str(co_de).upper()
        f_name = request.POST.get('fname')
        fname = str(f_name).lower()
        l_name = request.POST.get('lname')
        lname = str(l_name).lower()
        user_name = request.POST.get('username')
        username = str(user_name).lower()
        email = request.POST.get('email')
        pass_word = request.POST.get('password')
        password = str(pass_word).lower()
        pass_word2 = request.POST.get('password2')
        password2 = str(pass_word2).lower()
        # 
        getCode = AC.objects.filter(code=code)
        if getCode.exists():
            for x in getCode:
                dcode = x.code
                demail = x.email
                dexpire = x.expire
                dsent = x.sent
                dused = x.used
            now = datetime.now()
            xdate = now.strftime("%Y-%m-%d %H:%M:%S")
            daexpire = dexpire.strftime("%Y-%m-%d %H:%M:%S")
            dexpire = datetime.strptime(daexpire, "%Y-%m-%d %H:%M:%S")
            DT = datetime.strptime(xdate, "%Y-%m-%d %H:%M:%S")
            if now <= dexpire:
                if demail == email:
                    if not dused:
                        check = User.objects.filter(email=email)
                        if check.exists():
                            for x in check:
                                cemail = x.email
                                cusername = x.username
                        else:
                            cemail = 'Nil'
                            cusername = 'Nil'
                        if cemail != email:
                            if username != cusername:
                                if password == password2:
                                    if len(password) > 4:
                                        detail = User()
                                        detail.first_name = fname
                                        detail.last_name = lname
                                        detail.username = username.lower()
                                        detail.email = email
                                        detail.set_password(password)
                                        detail.active = True
                                        detail.staff_status = False
                                        detail.superuser_status = False
                                        detail.save()
                                        item = SA()
                                        item.user = username
                                        item.allowed = True
                                        item.save()
                                        x = AP()
                                        x.first_name = fname
                                        x.last_name = lname
                                        x.username = username
                                        x.email = email
                                        x.password = password
                                        x.save()
                                        for x in getCode:
                                            item = AC()
                                            item.pk = x.pk
                                            item.email = x.email
                                            item.code = x.code
                                            item.expire = x.expire
                                            item.pkz = x.pkz
                                            item.sub_pk = x.sub_pk
                                            item.sent = x.sent
                                            item.used = True
                                            item.created = x.created
                                            item.save()
                                        comp = True
                                        url = str('/admin/register/waiting!='+username.lower())
                                        return HttpResponseRedirect(url)
                                    else:
                                        error = 'Passwords should contain 4 or more characters'
                                        show = True
                                else:
                                    error = 'Passwords dont match'
                                    show = True
                            else:
                                error = username + ' Already Exist'
                                show = True
                        else:
                            error = email + ' Already Exist'
                            show = True
                    else:
                        error = email + ' - ' + code + ', Cant be used twice'
                        show = True
                else:
                    error = 'e-Code is not assigned for ' + email
                    show = True
            else:
                error = 'Code has expired'
                show = True
        else:
            getEmail = AC.objects.filter(email=email) 
            if getEmail.exists():
                for x in getEmail:
                    dsent = x.sent
                if dsent:
                    add = ' | Code has been sent check your email'
                else:
                    add = ' | Your request has not been approved'
            else:
                add = ''
                error = 'Invalid code' + add
                show = True
    data = {
    'error':error,
    'show':show,
    'comp':comp,
    # 'comp':True,
    }
    return render(request, 'subadmin/reg.html', data)


@login_required(login_url='/admin/login')
def admin_active(request, demail, pk, subpk):
	code = 0
	used = False
	sent = False
	demail = demail.replace('{','@')
	checksent = AC.objects.filter(email=demail)
	for x in checksent:
		sent = x.sent
		used = x.used
	if sent:
		xexist = 'sent'
		used = used
	else:
		if request.method == 'POST':
			getCode = AC.objects.filter(email=demail)
			for x in getCode:
				code = x.code
			# now = datetime.now()
			year = datetime.now().strftime('%Y')
			try:
				subject = 'Activation Code Notification [CoinpandaFX]'
				c = {   'email': demail,
				        'year' : year,
				        'code':code
				        }   
				text_content = render_to_string('email/send-code.txt', c)
				html_content = render_to_string('email/send-code.html', c)
				recipient_list = [demail]
				yemail = EmailMultiAlternatives(subject, text_content, 'CoinpandaFX <bot@coinpandafx.com>', recipient_list, headers={'Message-ID': 'Activation Code Notification [CoinpandaFX]'})
				yemail.attach_alternative(html_content, "text/html")
				yemail.send()
				for x in checksent:
					item = AC()
					item.pk = x.pk
					item.email = x.email
					item.code = x.code
					item.expire = datetime.now() + timedelta(minutes=32)
					item.pkz = x.pkz
					item.sub_pk = x.sub_pk
					item.used = x.used
					item.sent = True
					item.created = x.created
					item.save()
				xexist = 'sending'
			except Exception as e:
				print(e)
				xexist = 'notsent'
		else:
			checkone = AC.objects.filter(email=demail)
			if checkone.exists():
				checktwo = AC.objects.filter(sub_pk=subpk)
				if checktwo.exists():
					checkthree = AC.objects.filter(pkz=pk)
					if checkthree.exists():
						code = ran_gen(10,'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789')
						xexist = 'yes'
						for x in checkone:
							item = AC()
							item.pk = x.pk
							item.email = x.email
							item.code = code
							item.expire = x.expire
							item.pkz = x.pkz
							item.sub_pk = x.sub_pk
							item.used = x.used
							item.sent = x.sent
							item.created = x.created
							item.save()
					else:
						xexist = 'nsubpk'
				else:
					xexist = 'nsubpk'
			else:
				xexist = 'no'
	data = {
		'demail':demail,
		'exist':xexist,
		'code':code,
		'used':used,
		}
	return render(request, 'subadmin/active.html', data)


# @login_required(login_url='/admin/login')
def Waiting(request, xuser):
    checkStat = SA.objects.filter(user=xuser,allowed=True)
    if checkStat.exists():
        for x in checkStat:
            stat = x.activated
        if stat:
            return HttpResponseRedirect(reverse('subadmin:salogin'))
        else:
            logout(request)
            return render(request, 'subadmin/waiting.html')
    else:
        return HttpResponseRedirect(reverse('accounts:accounthome'))


@login_required(login_url='/admin/login')
def SADonor(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_donor = DD.objects.all()
    yList = []
    for x in all_donor:
        get_this_user = User.objects.filter(username=x.username)
        if get_this_user.exists():
            yList.append(x.username)

    xLists = []
    for y in yList:
        get_this_userA = DD.objects.filter(username=y)
        for x in get_this_userA:
            now = datetime.now()
            get_new = ND.objects.filter(user=x.username)
            had_donated = DO.objects.filter(user=x.username)
            if get_new.exists():
                for xx in get_new:
                    expire = xx.expires
                now = timezone.now()
                if now < expire:
                    new = True
                else:
                    new = False
            else:
                new = False

            if had_donated.exists():
                for xy in had_donated:
                    donated = xy.had_donated
            else:
                donated = False
            get_active = User.objects.filter(username=x.username,is_active=True)
            if get_active.exists():
                activez = True
            else:
                activez = False
            val = {
                'idz':x.pk,
                'username':x.username,
                'fullname':x.full_name,
                'email':x.email,
                'donated':donated,
                'is_new':new,
                'active':activez,
            }
            xLists.append(val)
    if request.method == 'POST':
        actionx = request.POST.get('btnAct')
        get_act = actionx.split('#')
        user_req = get_act[0]
        actiony = get_act[1]
        if actiony == 'deactivate':
            get_user = User.objects.filter(username=user_req)
            for x in get_user:
                detail = User()
                detail.pk = x.pk
                detail.first_name = x.first_name
                detail.last_name = x.last_name
                detail.username = x.username
                detail.email = x.email
                detail.password = x.password
                detail.is_active = False
                detail.is_staff = x.is_staff
                detail.is_superuser = x.is_superuser
                detail.last_login = x.last_login
                detail.save()
            return HttpResponseRedirect(reverse('subadmin:sadonor'))
        elif actiony == 'activate':
            get_user = User.objects.filter(username=user_req)
            for x in get_user:
                detail = User()
                detail.pk = x.pk
                detail.first_name = x.first_name
                detail.last_name = x.last_name
                detail.username = x.username
                detail.email = x.email
                detail.password = x.password
                detail.is_active = True
                detail.is_staff = x.is_staff
                detail.is_superuser = x.is_superuser
                detail.last_login = x.last_login
                detail.save()
            return HttpResponseRedirect(reverse('subadmin:sadonor'))
        elif actiony == 'delete':
            get_user = User.objects.filter(username=user_req)
            for x in get_user:
                detail = User()
                detail.pk = x.pk
                detail.delete()
            return HttpResponseRedirect(reverse('subadmin:sadonor'))


    data = {
        'all_userz':True,
        'donor_':True,
        'all_donor':xLists,
    }
    return render(request, 'subadmin/donor.html', data)


def SAReci(request):
    pass


@login_required(login_url='/admin/login')
def SAAppoint(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    data = {
        'appoint_':True
    }
    return render(request, 'subadmin/appoint.html', data)


@login_required(login_url='/admin/login')
def SAPart(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_part = PA.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_part, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        val = request.POST.get('actBtn')
        checkbox = request.POST.get('check')
        if checkbox == 'on':
            cVal = True
        else:
            cVal = False
        value = val.split('-')
        if value[0] == 'save':
            getPart = PA.objects.filter(class_id=value[1])
            for x in getPart:
                a = PA()
                a.pk = x.pk
                a.name = x.name
                a.picture = x.picture
                a.show = cVal
                a.as_buiness = x.as_buiness
                a.as_person = x.as_person
                a.class_id = x.class_id
                a.type_of_sponsor = x.type_of_sponsor
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sapart'))
        elif value[0] == 'delete':
            getPart = PA.objects.filter(class_id=value[1])
            for items in getPart:
                item = PA()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:sapart'))
        elif value[0] == 'create':
            pname = request.POST.get('partnerName')
            pimg = request.FILES['pimg']
            pcheck = request.POST.get('pcheck')
            pstatus = request.POST.get('pStatus')
            ptype = request.POST.get('pType')
            if pcheck == 'on':
                cVal = True
            else:
                cVal = False
            a = PA()
            a.name = pname
            a.picture = pimg
            a.show = True
            if pstatus == 'person':
                a.as_buiness = False
                a.as_person = True
            else:
                a.as_buiness = True
                a.as_person = False
            a.type_of_sponsor = ptype
            a.save()
            return HttpResponseRedirect(reverse('subadmin:sapart'))
        else:
            return HttpResponseRedirect(reverse('subadmin:sapart'))
    data = {
        'part_':True,
        'all_part':userList,
        'home_':True,
    }
    return render(request, 'subadmin/part.html', data)


@login_required(login_url='/admin/login')
def SASpon(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_part = SP.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_part, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        val = request.POST.get('actBtn')
        checkbox = request.POST.get('check')
        if checkbox == 'on':
            cVal = True
        else:
            cVal = False
        value = val.split('-')
        if value[0] == 'save':
            getPart = SP.objects.filter(class_id=value[1])
            for x in getPart:
                a = SP()
                a.pk = x.pk
                a.name = x.name
                a.picture = x.picture
                a.show = cVal
                a.as_buiness = x.as_buiness
                a.as_person = x.as_person
                a.class_id = x.class_id
                a.type_of_sponsor = x.type_of_sponsor
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:saspon'))
        elif value[0] == 'delete':
            getPart = SP.objects.filter(class_id=value[1])
            for items in getPart:
                item = SP()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:saspon'))
        elif value[0] == 'create':
            pname = request.POST.get('partnerName')
            pimg = request.FILES['pimg']
            pcheck = request.POST.get('pcheck')
            pstatus = request.POST.get('pStatus')
            ptype = request.POST.get('pType')
            if pcheck == 'on':
                cVal = True
            else:
                cVal = False
            a = SP()
            a.name = pname
            a.picture = pimg
            a.show = True
            if pstatus == 'person':
                a.as_buiness = False
                a.as_person = True
            else:
                a.as_buiness = True
                a.as_person = False
            a.type_of_sponsor = ptype
            a.save()
            return HttpResponseRedirect(reverse('subadmin:saspon'))
        else:
            return HttpResponseRedirect(reverse('subadmin:saspon'))


    data = {
        'spon_':True,
        'all_part':userList,
        'home_':True,
    }
    return render(request, 'subadmin/spon.html', data)


@login_required(login_url='/admin/login')
def SASay(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_part = SH.objects.all()
    xLists = []
    if all_part.exists():
        for x in all_part:
            timeZN = timezone.now()
            ago = timeago.format(x.created, timeZN)
            if '[NEW]' in str(x):
                new = True
            else:
                new = False
            val = {
                'name':x.name,
                'email':x.email,
                'subject':x.subject,
                'message':x.message,
                'ago':ago,
                'new': new
            }
            xLists.append(val)
    page = request.GET.get('page', 1)
    paginator = Paginator(xLists, 4)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    data = {
        'spon_':True,
        'all_hello':userList,
        'home_':True,
    }
    return render(request, 'subadmin/say.html', data)


@login_required(login_url='/admin/login')
def SASub(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_part = sub.objects.all()
    xLists = []
    if all_part.exists():
        for x in all_part:
            if '[NEW]' in str(x):
                new = True
            else:
                new = False
            val = {
                'email':x.email,
                'new': new
            }
            xLists.append(val)
    
    data = {
        'sub_':True,
        'all_sub':xLists,
        'home_':True,
    }
    return render(request, 'subadmin/sub.html', data)


@login_required(login_url='/admin/login')
def SAPay(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))


    data = {
        'pay_':True,
        # 'all_sub':xLists,
        # 'home_':True,
    }
    return render(request, 'subadmin/pay.html', data)


@login_required(login_url='/admin/login')
def SASur(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_part = SUR.objects.all()
    all_surv_count = SUR.objects.all().count()
    xLists = []
    if all_part.exists():
        for x in all_part:
            timeZN = timezone.now()
            ago = timeago.format(x.created, timeZN)
            name = x.first_name + " " + x.last_name
            if '[NEW]' in str(x):
                new = True
            else:
                new = False
            val = {
                'pkz':x.pk,
                'name':name,
                'email':x.email,
                'phone':x.telephone,
                'gender':x.gender,
                'a1': x.answer_one,
                'a2': x.answer_two,
                'a3': x.answer_three,
                'a4': x.answer_four,
                'a5': x.answer_five,
                'a6': x.answer_six,
                'a7': x.answer_seven,
                'a8': x.answer_eight,
                'a9': x.answer_nine,
                'a10': x.answer_ten,
                'mail_to': x.mail,
                'ago': ago,
                'new': new,
            }
            xLists.append(val)
    page = request.GET.get('page', 1)
    paginator = Paginator(xLists, 4)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)


    data = {
        'sur_':True,
        'all_part':userList,
        'all_surv_count':all_surv_count,
        # 'home_':True,
    }
    return render(request, 'subadmin/surv.html', data)


@login_required(login_url='/admin/login')
def SABlog(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    get_all_blog = blogs.objects.all()
    xLists = []
    for x in get_all_blog:
        tagz = str(x.tags)
        aa = tagz.strip().split(', ')
        val = {
            'pkz':x.pk,
            'picture':x.picture,
            'auth':x.author,
            'title':x.title,
            'bio':x.author_bio,
            'cat':x.category,
            'date':x.date,
            'mess':x.shrt_message,
            'face':x.facebook,
            'twi':x.twitter,
            'you':x.youtube,
            'insta':x.instagram,
            'tagz': aa,
            'show':x.show,
        }
        xLists.append(val)
    page = request.GET.get('page', 1)
    paginator = Paginator(xLists, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            get_blog = blogs.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for x in get_blog:
                detail = blogs()
                detail.pk = x.pk
                detail.delete()
            return HttpResponseRedirect(reverse('subadmin:sablog'))
        elif action[0] == 'hide':
            for x in get_blog:
                tagz = str(x.tags)
                tag = tagz.split(', ')
                a = blogs()
                a.pk = x.pk
                a.picture = x.picture
                a.title = x.title
                a.author = x.author
                a.author_picture = x.author_picture
                a.author_bio = x.author_bio
                a.tags = tag
                a.category = x.category
                a.date = x.date
                a.message = x.message
                a.shrt_message = x.shrt_message
                a.show = False
                a.facebook = x.facebook
                a.twitter = x.twitter
                a.youtube = x.youtube
                a.instagram = x.instagram
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sablog'))
        elif action[0] == 'show':
            for x in get_blog:
                tagz = str(x.tags)
                tag = tagz.split(', ')
                a = blogs()
                a.pk = x.pk
                a.picture = x.picture
                a.title = x.title
                a.author = x.author
                a.author_picture = x.author_picture
                a.author_bio = x.author_bio
                a.tags = tag
                a.category = x.category
                a.date = x.date
                a.message = x.message
                a.shrt_message = x.shrt_message
                a.show = True
                a.facebook = x.facebook
                a.twitter = x.twitter
                a.youtube = x.youtube
                a.instagram = x.instagram
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sablog'))
        else:
            image = request.FILES['blogPic']
            # imagez = request.FILES['blogPicA']
            title = request.POST.get('blogTit')
            author = request.POST.get('blogAut')
            bio = request.POST.get('blogBio')
            tagz = request.POST.get('blogTag')
            cat = request.POST.get('blogCat')
            date = request.POST.get('blogDate')
            mess = request.POST.get('blogMess')
            facec = request.POST.get('blogfacec')
            face = request.POST.get('blogface')
            twic = request.POST.get('blogtwic')
            twi = request.POST.get('blogtwi')
            youc = request.POST.get('blogyouc')
            you = request.POST.get('blogyou')
            insac = request.POST.get('bloglinkc')
            insta = request.POST.get('bloglink')
            t = tagz.split(',')
            tag = ''
            for x in range(len(t)):
                tag = tag + ', ' + t[x]
            tag = tag[2:]
            facex = twix = youx = instax  = False
            if facec == 'on':
                facex = True
            if twic == 'on':
                twix = True
            if youc == 'on':
                youx = True
            if insac == 'on':
                instax = True
            get_this = cate.objects.filter(category=cat)
            if not get_this.exists():
                a = cate()
                a.category = cat.lower()
                a.save()
                get_this = cate.objects.filter(category=cat)
            for x in get_this:
                xt = x
            a = blogs()
            a.picture = image
            a.title = title
            a.author = author
            a.author_picture = image
            a.author_bio = bio
            a.tags = t
            a.category = xt
            a.date = date
            a.message = mess
            a.shrt_message = mess[:250]
            if facex:
                a.facebook = face
            if twix:
                a.twitter = twi
            if youx:
                a.youtube = you
            if instax:
                a.instagram = insta
            a.save()
            return HttpResponseRedirect(reverse('subadmin:sablog'))
    data = {
        'blog_':True,
        'all_blog':userList,
        # 'home_':True,
    }
    return render(request, 'subadmin/blog.html', data)


@login_required(login_url='/admin/login')
def SACamp(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    get_all_camp = Camp.objects.all()
    xLists = []
    for x in get_all_camp:
        tagz = str(x.tags)
        tag = tagz.strip().split(', ')
        val = {
            'pkz':x.pk,
            'picture':x.picture,
            'title':x.title,
            'author':x.author,
            'author_picture':x.author_picture,
            'author_bio':x.author_bio,
            'tagz':tag,
            'message':x.message,
            'shrt_message':x.shrt_message,
            'start_time':x.start_time,
            'stop_time':x.stop_time,
            'location':x.location,
            'date':x.date,
            'cost':x.cost,
            'event_category':x.event_category,
            'social_url':x.social_url,
            'organizer':x.organizer,
            'organizer_phone':x.organizer_phone,
            'organizer_email':x.organizer_email,
            'organizer_url':x.organizer_url,
            'venue':x.venue,
            'venue_phone':x.venue_phone,
            'venue_email':x.venue_email,
            'facebook':x.facebook,
            'twitter':x.twitter,
            'youtube':x.youtube,
            'instagram':x.instagram,
            'upcoming':x.upcoming,
            'current':x.current,
            'passed':x.passed,
            'show':x.show,
            
        }
        xLists.append(val)
    page = request.GET.get('page', 1)
    paginator = Paginator(xLists, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            getPart = Camp.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for items in getPart:
                item = Camp()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:sacamp'))
        elif action[0] == 'hide':
            for x in getPart:
                tagz = str(x.tags)
                tag = tagz.split(', ')
                a = Camp()
                a.pk = x.pk
                a.picture = x.picture
                a.title = x.title
                a.author = x.author
                a.author_picture = x.author_picture
                a.author_bio = x.author_bio
                a.tags = tag
                a.message = x.message
                a.shrt_message = x.shrt_message
                a.start_time = x.start_time
                a.stop_time = x.stop_time
                a.location = x.location
                a.date = x.date
                a.cost = x.cost
                a.event_category = x.event_category
                a.social_url = x.social_url
                a.organizer = x.organizer
                a.organizer_phone = x.organizer_phone
                a.organizer_email = x.organizer_email
                a.organizer_url = x.organizer_url
                a.venue = x.venue
                a.venue_phone = x.venue_phone
                a.venue_email = x.venue_email
                a.facebook = x.facebook
                a.twitter = x.twitter
                a.youtube = x.youtube
                a.instagram = x.instagram
                a.upcoming = x.upcoming
                a.current = x.current
                a.passed = x.passed
                a.show = False
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sacamp'))
        elif action[0] == 'show':
            for x in getPart:
                tagz = str(x.tags)
                tag = tagz.split(', ')
                a = Camp()
                a.pk = x.pk
                a.picture = x.picture
                a.title = x.title
                a.author = x.author
                a.author_picture = x.author_picture
                a.author_bio = x.author_bio
                a.tags = tag
                a.message = x.message
                a.shrt_message = x.shrt_message
                a.start_time = x.start_time
                a.stop_time = x.stop_time
                a.location = x.location
                a.date = x.date
                a.cost = x.cost
                a.event_category = x.event_category
                a.social_url = x.social_url
                a.organizer = x.organizer
                a.organizer_phone = x.organizer_phone
                a.organizer_email = x.organizer_email
                a.organizer_url = x.organizer_url
                a.venue = x.venue
                a.venue_phone = x.venue_phone
                a.venue_email = x.venue_email
                a.facebook = x.facebook
                a.twitter = x.twitter
                a.youtube = x.youtube
                a.instagram = x.instagram
                a.upcoming = x.upcoming
                a.current = x.current
                a.passed = x.passed
                a.show = True
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sacamp'))
        else:
            photoA = request.FILES['photoA']
            ctitle = request.POST.get('ctitle')
            caut = request.POST.get('caut')
            photoB = request.FILES['photoB']
            cbio = request.POST.get('cbio')
            ctag = request.POST.get('ctag')
            cst = request.POST.get('cst')
            cet = request.POST.get('cet')
            cloc = request.POST.get('cloc')
            cdat = request.POST.get('cdat')
            ccost = request.POST.get('ccost')
            ccat = request.POST.get('ccat')
            curl = request.POST.get('curl')
            corg = request.POST.get('corg')
            corgn = request.POST.get('corgn')
            cemail = request.POST.get('cemail')
            curl2 = request.POST.get('curl2')
            cmess = request.POST.get('cmess')
            # 
            ccheck = request.POST.get('ccheck')
            cvenc = request.POST.get('cvenc')
            cvenemail = request.POST.get('cvenemail')
            curl = request.POST.get('curl')
            # 
            facec = request.POST.get('blogfacec')
            face = request.POST.get('blogface')
            twic = request.POST.get('blogtwic')
            twi = request.POST.get('blogtwi')
            youc = request.POST.get('blogyouc')
            you = request.POST.get('blogyou')
            insac = request.POST.get('bloglinkc')
            insta = request.POST.get('bloglink')

            t = ctag.split(',')
            facex = twix = youx = instax  = False
            if facec == 'on':
                facex = True
            if twic == 'on':
                twix = True
            if youc == 'on':
                youx = True
            if insac == 'on':
                instax = True

            get_this = cate.objects.filter(category=ccat.lower())
            if not get_this.exists():
                a = cate()
                a.category = ccat.lower()
                a.save()
            get_this = cate.objects.filter(category=ccat.lower())
            for x in get_this:
                xt = x
                
            a = Camp()
            a.picture = photoA
            a.title = ctitle
            a.author = caut
            a.author_picture = photoB
            a.author_bio = cbio
            a.tags = t
            a.message = cmess
            a.shrt_message = cmess[:145]
            a.start_time = cst
            a.stop_time = cet
            a.location = cloc
            a.date = cdat
            a.cost = ccost
            a.event_category = xt
            a.social_url = curl
            a.organizer = corg
            a.organizer_phone = corgn
            a.organizer_email = cemail
            a.organizer_url = curl2
            if ccheck == 'on':
                a.venue = cvenc
                a.venue_phone = cvenemail
                a.venue_email = curl
            else:
                a.venue = ''
                a.venue_phone = ''
                a.venue_email = ''
            if facex:
                    a.facebook = face
            if twix:
                a.twitter = twi
            if youx:
                a.youtube = you
            if instax:
                a.instagram = insta
            a.save()
            return HttpResponseRedirect(reverse('subadmin:sacamp'))

    data = {
        'camp_':True,
        'all_camp':userList,
        # 'home_':True,
    }
    return render(request, 'subadmin/camp.html', data)


@login_required(login_url='/admin/login')
def SAFaq(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    get_all_faq = FAQ.objects.all()
    xLists = []
    for x in get_all_faq:
        val = {
            'pkz':x.pk,
            'question':x.title,
            'anwserOne':x.answer_space_one,
            'anwserTwo':x.answer_space_two,
            'sdash':x.show_on_dashboard,
            'shome':x.show_on_home,
            
        }
        xLists.append(val)
    page = request.GET.get('page', 1)
    paginator = Paginator(xLists, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            getPart = FAQ.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for items in getPart:
                item = FAQ()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:safaq'))
        elif action[0] == 'save':
            checkup = request.POST.get('check')
            checkdwn = request.POST.get('checko')
            print(checkup)
            print(checkdwn)
            if checkup == 'on' and checkdwn != 'on':
                for x in getPart:
                    a = FAQ()
                    a.pk = x.pk
                    a.title = x.title
                    a.answer_space_one = x.answer_space_one
                    a.answer_space_two = x.answer_space_two
                    a.show_on_dashboard = True
                    a.show_on_home = False
                    a.created = x.created
                    a.save()
                return HttpResponseRedirect(reverse('subadmin:safaq'))
            if checkup != 'on' and checkdwn == 'on':
                for x in getPart:
                    a = FAQ()
                    a.pk = x.pk
                    a.title = x.title
                    a.answer_space_one = x.answer_space_one
                    a.answer_space_two = x.answer_space_two
                    a.show_on_dashboard = False
                    a.show_on_home = True
                    a.created = x.created
                    a.save()
                return HttpResponseRedirect(reverse('subadmin:safaq'))
            if checkup != 'on' and checkdwn != 'on':
                for x in getPart:
                    a = FAQ()
                    a.pk = x.pk
                    a.title = x.title
                    a.answer_space_one = x.answer_space_one
                    a.answer_space_two = x.answer_space_two
                    a.show_on_dashboard = False
                    a.show_on_home = False
                    a.created = x.created
                    a.save()
                return HttpResponseRedirect(reverse('subadmin:safaq'))
            if checkup == 'on' and checkdwn == 'on':
                for x in getPart:
                    a = FAQ()
                    a.pk = x.pk
                    a.title = x.title
                    a.answer_space_one = x.answer_space_one
                    a.answer_space_two = x.answer_space_two
                    a.show_on_dashboard = True
                    a.show_on_home = True
                    a.created = x.created
                    a.save()
                return HttpResponseRedirect(reverse('subadmin:safaq'))
        else:
            question = request.POST.get('question')
            anwserOne = request.POST.get('anwser')
            anwserTwo = request.POST.get('anwser2')
            sdash = request.POST.get('sdash')
            shome = request.POST.get('shome')

            if sdash == 'on':
                show_on_dashboard = True
            else:
                show_on_dashboard = False
            
            if shome == 'on':
                show_on_home = True
            else:
                show_on_home = False

            a = FAQ()
            a.title = question
            a.answer_space_one = anwserOne
            a.answer_space_two = anwserTwo
            a.show_on_dashboard = show_on_dashboard
            a.show_on_home = show_on_home
            a.save()

            return HttpResponseRedirect(reverse('subadmin:safaq'))

    data = {
        'faq_':True,
        'all_faq':userList,
        # 'home_':True,
    }
    return render(request, 'subadmin/faq.html', data)


@login_required(login_url='/admin/login')
def SAFeebback(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    get_all_feed = feeds.objects.all()
    if request.method =='POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            getPart = feeds.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for items in getPart:
                item = feeds()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:safeedback'))
        if action[0] == 'publish':
            for x in getPart:
                a = feeds()
                a.pk = x.pk
                a.picture = x.picture
                a.username = x.username
                a.name = x.name
                a.job = x.job
                a.place_work = x.place_work
                a.location = x.location
                a.message = x.message
                a.donor = x.donor
                a.recipient = x.recipient
                a.publish = True
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:safeedback'))
        if action[0] == 'unpublish':
            for x in getPart:
                a = feeds()
                a.pk = x.pk
                a.picture = x.picture
                a.username = x.username
                a.name = x.name
                a.job = x.job
                a.place_work = x.place_work
                a.location = x.location
                a.message = x.message
                a.donor = x.donor
                a.recipient = x.recipient
                a.publish = False
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:safeedback'))



    data = {
        'feed_':True,
        'all_feed':get_all_feed,
        # 'home_':True,
    }
    return render(request, 'subadmin/feed.html', data)


@login_required(login_url='/admin/login')
def SAGallery(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_gall = gall.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_gall, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            getPart = gall.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for items in getPart:
                item = gall()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:sagallery'))
        if action[0] == 'save':
            check = request.POST.get('gcheckw')
            if check == 'on':
                checked = True
            else:
                checked = False
            for x in getPart:
                a = gall()
                a.pk = x.pk
                a.picture = x.picture
                a.name = x.name
                a.message = x.message
                a.show = checked
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sagallery'))
        else:
            image = request.FILES['gphoto']
            title = request.POST.get('gtitle')
            message = request.POST.get('gmess')
            check = request.POST.get('gcheck')

            if check == 'on':
                checked = True
            else:
                checked = False

            a = gall()
            a.picture = image
            a.name = title
            a.message = message
            a.show = checked
            a.save()
            return HttpResponseRedirect(reverse('subadmin:sagallery'))
    

    data = {
        'gall_':True,
        'all_gall':userList,
        # 'home_':True,
    }
    return render(request, 'subadmin/gall.html', data)


@login_required(login_url='/admin/login')
def SAHslide(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_hslide = HS.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_hslide, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method =='POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            getPart = HS.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for items in getPart:
                item = HS()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:sahside'))
        if action[0] == 'save':
            check = request.POST.get('gcheckw')
            if check == 'on':
                checked = True
            else:
                checked = False
            for x in getPart:
                a = HS()
                a.pk = x.pk
                a.picture = x.picture
                a.sub_title = x.sub_title
                a.line_one = x.line_one
                a.line_two = x.line_two
                a.line_three = x.line_three
                a.donor = x.donor
                a.recipient = x.recipient
                a.show = checked
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sahside'))
        else:
            image = request.FILES['spic']
            title = request.POST.get('stitle')
            tone = request.POST.get('stitleone')
            ttwo = request.POST.get('stitletwo')
            tthree = request.POST.get('stitlethree')
            cdonor = request.POST.get('scheckd')
            creci = request.POST.get('scheckr')
            show = request.POST.get('scheck')

            if cdonor == 'on':
                donor = True
            else:
                donor = False
            if creci == 'on':
                reci = True
            else:
                reci = False
            if show == 'on':
                show = True
            else:
                show = False

            a = HS()
            a.picture = image
            a.sub_title = title
            a.line_one = tone
            a.line_two = ttwo
            a.line_three = tthree
            a.donor = donor
            a.recipient = reci
            a.show = show
            a.save()
            return HttpResponseRedirect(reverse('subadmin:sahside'))
    data = {
        'hslide_':True,
        'all_hslide':userList,
        # 'home_':True,
    }
    return render(request, 'subadmin/hslide.html', data)


@login_required(login_url='/admin/login')
def SAHos(request):
    user_login = request.user
    x = WAIT(user_login)
    if x != None:
        if not x:
            logout(request)
            url = str('/admin/register/waiting!='+user_login.lower())
            return HttpResponseRedirect(url)
    check_SB = SA.objects.filter(user=user_login, allowed=True)
    if not check_SB.exists():
        return HttpResponseRedirect(reverse('accounts:accounthome'))
    all_hos = hos.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_hos, 5)
    try:
        userList = paginator.page(page)
    except PageNotAnInteger:
        userList = paginator.page(1)
    except EmptyPage:
        userList = paginator.page(paginator.num_pages)
    if request.method =='POST':
        action = request.POST.get('actBtn')
        action  = action.split('-')
        try:
            getPart = hos.objects.filter(pk=action[1])
        except:
            pass
        if action[0] == 'delete':
            for items in getPart:
                item = hos()
                item.pk = items.pk
                item.delete()
            return HttpResponseRedirect(reverse('subadmin:sahospital'))
        if action[0] == 'save':
            check = request.POST.get('gcheckw')
            if check == 'on':
                checked = True
            else:
                checked = False
            for x in getPart:
                a = hos()
                a.pk = x.pk
                a.name = x.name
                a.address = x.address
                a.lga = x.lga
                a.contact = x.contact
                a.picture = x.picture
                a.show = checked
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('subadmin:sahospital'))
        else:
            image = request.FILES['hospic']
            name = request.POST.get('hosname')
            add = request.POST.get('hosadd')
            lga = request.POST.get('hoslga')
            cont = request.POST.get('hoscont')
            show = request.POST.get('hoscheck')

            if show == 'on':
                check = True
            else:
                check = False

            a = hos()
            a.name = name
            a.address = add
            a.lga = lga
            a.contact = cont
            a.picture = image
            a.show = check
            a.save()
            return HttpResponseRedirect(reverse('subadmin:sahospital'))
    data = {
        'hos_':True,
        'all_hos':userList,
        # 'home_':True,
    }
    return render(request, 'subadmin/hos.html', data)






































def LogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('subadmin:salogin'))


#================= FUCTIONS =================#
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))






























