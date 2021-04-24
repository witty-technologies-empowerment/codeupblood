from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.conf import settings 
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


import random
import string

import requests
import json

from donor.models import DonorDetail as DD, NewDonor as ND
from recipient.models import RecipientDetail as RD
from .models import AccountPath as AP

# Create your views here.

def AccountHome(request):
    user_login = request.user
    if request.user.is_authenticated:
        check_path = AP.objects.filter(username=user_login)
        for x in check_path:
            path = x.path
        if path == 'admin':
            pass
        elif path == 'donor':
            return HttpResponseRedirect(reverse('donor:home'))
        else:
            # return HttpResponseRedirect(reverse('reci:home'))
            pass
    else:
        if request.method == 'POST':
            path = request.POST.get('path')
            if path == 'donor':
                return HttpResponseRedirect(reverse('donor:home'))
            else:
                # return HttpResponseRedirect(reverse('reci:home'))
                pass
        return render(request, 'accounts/home.html',)


def donor_login(request, Nuser=None):
    user_login = request.user
    if request.user.is_authenticated:
        check_path = AP.objects.filter(username=user_login)
        for x in check_path:
            path = x.path
        if path == 'admin':
            pass
        elif path == 'donor':
            return HttpResponseRedirect(reverse('donor:home'))
        else:
            # return HttpResponseRedirect(reverse('reci:home'))
            pass
    else:
        next_url = None
        next_ = False
        display = False
        error = ''
    if 'next' in str(request):
        next_url = request.GET.get('next')
        next_ = True
    if request.method == 'POST':
        # user_name = request.POST.get('emailID')
        email = request.POST.get('username')
        email = str(email).strip().lower()
        pass_word = request.POST.get('password')
        password = str(pass_word).strip().lower()
        if '@' in email:
            get_email = User.objects.filter(email=email)
            if get_email.exists():
                for x in get_email:
                    username = x.username
            else:
                error = 'Invalid Login email'
                display = True
                context = {
                    'error':error,
                    'display':display,
                }
                return render(request, 'accounts/donor_login.html', context)
        else:
            get_username = User.objects.filter(username=email)
            if get_username.exists():
                username = email
            else:
                error = 'Invalid Login User'
                display = True
                context = {
                    'error':error,
                    'display':display,
                }
                return render(request, 'accounts/donor_login.html', context)
        get_active = User.objects.filter(username=username.lower(), is_active=True)
        if get_active.exists():
            user = authenticate(username=username.lower(), password=password)
        else:
            get_user = User.objects.filter(username=username.lower())
            if get_user.exists():
                error = 'Invalid Login Details'
                display = True
                context = {
                    'error':error,
                    'display':display,
                }
                return render(request, 'accounts/donor_login.html', context)
            else:
                error = 'Account Deactivated'
                display = True
                xdisplay = True
                context = {
                    'error':error,
                    'display':display,
                    'xdisplay':xdisplay,
                }
                return render(request, 'accounts/donor_login.html', context)
        if user:
            if user.is_active:
                login(request, user)
                # data = RA()
                # data.user = username
                # data.activity_type = 'login'
                # now = datetime.now()
                # date = now.strftime('%Y-%m-%dT%TZ')
                # data.time = date
                # data.status = 'You logged in near ' + location
                # data.save()
                # send_sms.send(sender=None, smstype='login-'+str(location), user = request.user)
                if 'admin' in username:
                    url = str('/_')
                    return HttpResponseRedirect(url)
                else:
                    if next_:
                        if('signout' not in next_url):
                            return HttpResponseRedirect(next_url)
                        else:
                            return HttpResponseRedirect(reverse('donor:home'))
                    else:
                        return HttpResponseRedirect(reverse('donor:home'))
            else:
                error = 'Invalid Login'
                display = True
                context = {
                    'error':error,
                    'display':display,
                }
            return render(request, 'accounts/donor_login.html', context)
        else:
            error = 'Invalid Login'
            display = True
            context = {
                'error':error,
                'display':display,
            }
        return render(request, 'accounts/donor_login.html', context)
    else:
        if Nuser != None:
            context = {
                    'Nuser':Nuser,
                    'error':error,
                    'display':display,
                }
        else:
            context = {
                    'error':error,
                    'display':display,
                }
        return render(request, 'accounts/donor_login.html', context)
    return render(request, 'accounts/donor_login.html')


def donor_reg(request):
    xcheck = False
    user_login = request.user
    full_name = ''
    username = ''
    email = ''
    user_id = ran_gen(6,'ABCDEFGHIJKLMPQRSTUVWXYZ123456789')
    while xcheck:
        check_id = AP.objects.filter(username=user_id)
        if check_id.exists():
            user_id = ran_gen(6,'ABCDEFGHIJKLMPQRSTUVWXYZ123456789')
            xcheck = False
        else:
            xcheck = True

    display = False
    xList = []
    if request.user.is_authenticated:
        check_path = AP.objects.filter(username=user_login)
        for x in check_path:
            path = x.path
        if path == 'admin':
            pass
        elif path == 'donor':
            return HttpResponseRedirect(reverse('donor:home'))
        else:
            # return HttpResponseRedirect(reverse('reci:home'))
            pass
    
    else:
        if request.method == 'POST':
            f_name = request.POST.get('name')
            full_name = f_name.lower().lstrip().rstrip()
            user_name = request.POST.get('username')
            username = user_name.lower().lstrip().rstrip()
            # gen_der = request.POST.get('gender')
            # gender = gen_der.lower().lstrip().rstrip()
            # blood_type = request.POST.get('bloodtype')
            # bloodtype = blood_type.lower().lstrip().rstrip()
            e_mail = request.POST.get('email')
            email = e_mail.lower().lstrip().rstrip()
            # tele_phone = request.POST.get('telephone')
            # telephone = tele_phone.lower().lstrip().rstrip()
            # sta_te = request.POST.get('state')
            # state = sta_te.lower().lstrip().rstrip()
            pass_ = request.POST.get('pass')
            password = pass_.lower().lstrip().rstrip()
            pass_2 = request.POST.get('pass2')
            password2 = pass_2.lower().lstrip().rstrip()

            checkemail = User.objects.filter(email=email)
            checkuser = User.objects.filter(username=username)

            if password != password2:
                error = {'error':"Both passwords didn't match"}
                display = True
                xList.append(error)
            if len(password) < 6 :
                error = {'error':"Password should be at least 6 charaters long"}
                display = True
                xList.append(error)
            if checkuser.exists():
                error = {'error':str(username) + " is not available"}
                display = True
                xList.append(error)
            if checkemail.exists():
                error = {'error':str(email) + " has been used"}
                display = True
                xList.append(error)
                email = ''
            if ' ' not in full_name:
                error = {'error':"Please provide full name with a space"}
                display = True
                xList.append(error)
            if not display:
                random_number = random.randint(0,16777215)
                hex_number = format(random_number,'x')
                hex_number = '#'+hex_number
                # RefCode = ran_gen(8,'ABCDEFGHIJKLMPQRSTUVWXYZ123456789')
                name = full_name.split(' ')
                namex = full_name.replace(' ', '-')
                detail = User()
                detail.first_name = name[0]
                detail.last_name = name[1]
                detail.username = username
                detail.email = email
                detail.set_password(password)
                detail.active = True
                detail.staff_status = False
                detail.superuser_status = False
                detail.save()
                a = AP()
                a.username = username
                a.color_code = hex_number
                a.path = 'donor'
                a.save()
                a = DD()
                a.full_name = full_name
                a.username = username
                a.gender = ''
                a.bloodtype = ''
                a.email = email
                a.telephone = ''
                a.state = ''
                a.password = password
                a.save()
                a = ND()
                a.user = username
                a.expires = datetime.now() + timedelta(hours=24)
                a.save()
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        try:
                            URL = 'https://safewayfx.com/api/v1/codeupblood/newUser/'+namex+'/'+email+'/'+username
                            print(URL)
                            ress = json.loads(requests.get(URL).json())
                            print(str(ress))
                        except Exception as e:
                            print('>>>'+str(e))
                        login(request, user)
                        return HttpResponseRedirect(reverse('accounts:donor_add'))
    data = {
        'user_id':'CB-'+user_id,
        'display':display,
        'xLists':xList,
        'full_name':full_name,
        'username':username,
        'email':email,
    }
    return render(request, 'accounts/donor_reg.html', data)


def donor_recover(request):
    return render(request, 'accounts/donor_pwd.html')


def rec_login(request):
    return render(request, 'accounts/rec_login.html')


def rec_reg(request):
    user_id = ran_gen(6,'ABCDEFGHIJKLMPQRSTUVWXYZ123456789')
    data = {
        'user_id':user_id,
    }
    return render(request, 'accounts/rec_reg.html', data)


def rec_recover(request):
    return render(request, 'accounts/rec_pwd.html')


def donor_add(request):
    user_login = request.user
    display = False
    # if request.user.is_authenticated:
    #     check_path = AP.objects.filter(username=user_login)
    #     check_ = DD.objects.filter(username=user_login)
    #     for x in check_path:
    #         path = x.path
    #     if path == 'admin':
    #         return HttpResponseRedirect(reverse('admin'))
    #     elif path == 'donor':
    #         if check_.exists():
    #             return HttpResponseRedirect(reverse('donor:home'))
    #     else:
    #         # return HttpResponseRedirect(reverse('reci:home'))
    #         pass
    # else:
    if request.method == 'POST':
        te_le = request.POST.get('tele')
        tele = te_le.lower().lstrip().rstrip()
        addre_ss = request.POST.get('address')
        address = addre_ss.lower().lstrip().rstrip()
        locali_ty = request.POST.get('locality')
        locality = locali_ty.lower().lstrip().rstrip()
        sta_te = request.POST.get('state')
        state = sta_te.lower().lstrip().rstrip()
        count_ry = request.POST.get('country')
        country = count_ry.lower().lstrip().rstrip()
        gend_er = request.POST.get('gender')
        gender = gend_er.lower().lstrip().rstrip()
        bloodty_pe = request.POST.get('bloodtype')
        bloodtype = bloodty_pe.lower().lstrip().rstrip()

        xList = []

        checkPhone = DD.objects.filter(telephone=tele)
        if checkPhone.exists():
            error = {'error':"Telephone already exists"}
            display = True
            xList.append(error)
        if not display:
            checkPhone = DD.objects.filter(username=user_login)
            for x in checkPhone:
                a = DD()
                a.pk = x.pk
                a.full_name = x.full_name
                a.username = x.username
                a.gender = gender
                a.bloodtype = bloodtype
                a.email = x.email
                a.telephone = tele
                a.address = address
                a.city = locality
                a.state = state
                a.country = country
                a.password = x.password
                a.created = x.created
                a.save()
            return HttpResponseRedirect(reverse('donor:home'))
            

    return render(request, 'accounts/donor_add.html')


@login_required(login_url='/accounts')
def any_user_signout(request):
	auth = request.user
	message = 'You have successfully signed out'
	logout(request)
	context = {
			'message':message,
			'auth':auth,
			}
	return HttpResponseRedirect(reverse('accounts:home'))


#================= FUCTIONS =================#
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))