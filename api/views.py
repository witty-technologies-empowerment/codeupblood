from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
import calendar
import requests
from django.contrib.auth.models import User
import random
import string
import json
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from subadmin.models import ActivationCode as AC
from donor.models import Appointment as APP, DonorDetail as DD
from accounts.models import AccountPath as AP
from home.models import (RequestAppointment as RA, SayHello as SH, Subscriber as sub,Hospital as hos)
from volunteer.models import (Volunteer as volu)

# <meta name="theme-color" content="#ffffff" />


# Create your views here.
def getStat(request):
    MONTHS_NUM = 6
    double_months_list = calendar.month_name[1:] * 2
    today_month = datetime.now().month + 12
    first_month = today_month - MONTHS_NUM
    last_months = double_months_list[first_month:today_month][::-1]
    nlast_months = []
    for x in range(len(last_months)):
        get = last_months[x][:3]
        nlast_months.insert(0, get)
    

    status = {
        'status': 200,
        'mnth':nlast_months,
        'dataOne':[0, 0, 0, 0, 0, 0],
        'dataTwo':[0, 0, 0, 0, 0, 0],
        }

    return JsonResponse(status, safe=False)


def CheckDate(request, date):
    _formart = '%d/%m/%Y %H:%M:%S'
    _a_formart = '%m/%d/%Y %H:%M'
    try:
        location = json.loads(requests.get('http://worldtimeapi.org/api/timezone/Africa/Lagos.json').text)
        a = location['datetime'][:10]
        b = location['datetime']
        now = datetime.now()
        year = a[:4]
        mnth = a[5:7]
        day = a[8:]
        time = b[11:19]
        newDate = day+'/'+mnth+'/'+year+' '+time
        znow = datetime.strptime(newDate, _formart)
    except Exception as e:
        print(e)
        now = datetime.now()
        ynow = now.strftime(_formart)
        znow = datetime.strptime(ynow, _formart)
    date = date.replace('_','/')
    date = date.replace(')(',' ')
    ynow = znow.strftime(_formart)
    znow = datetime.strptime(ynow, _formart)
    xnow = datetime.strptime(date, _formart)
    xdate = xnow.strftime(_a_formart)
    allowed = znow + timedelta(hours=2)
    xallowed = allowed.strftime(_a_formart)
    if xnow < znow:
        status = {
			'status': 400,
			'message':'Your Appointment Date should be greater than '+ xdate,
			}
    elif xnow >= znow and xnow < allowed:
        status = {
			'status': 401,
			'message':'Your can Book an Appointment two hours of your current time, Try any date greater than '+xallowed,
			}

    else:
        status = {
			'status': 200,
			}

    return JsonResponse(status, safe=False)


def createAppointment(request):
    user_login = request.user
    get_user = DD.objects.filter(username=user_login)
    for x in get_user:
        full_name = x.full_name
        telephone = x.telephone
    if request.method == 'POST':
        date = request.POST.get('timepicker')
        state = request.POST.get('state')
        lga = request.POST.get('lga')
        hospital = request.POST.get('hospital')
        get_hos_loc = hos.objects.filter(name=hospital)
        for a in get_hos_loc:
            address = a.address
        date = date.replace('_','/')
        date = date.replace(')(',' ')
        xdate = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
        xDate = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
        xTime = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
        try:
            a = APP()
            a.full_name = full_name
            a.username = user_login
            a.date = xDate
            a.time = xTime
            a.donor_id = 'CBID-'+ran_gen(6,'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789')
            a.telephone = telephone
            a.hospital = hospital
            a.hospital_location = address
            a.state = state
            a.lga = lga
            a.next_appointment_due_date_time = xdate + timedelta(days=84)
            a.save()
            status = {
                'status': 200,
                'mess': full_name.title() +', Your appointment was successfully created.'
            }
        except Exception as e:
            print(e)
            status = {
                'status': 500,
                'mess': full_name.title() +', Your appointment could not be created.'
            }

    return JsonResponse(status, safe=False)


def getAppointment(request, name):
    getappointments = APP.objects.filter(username=name)
    xList = []
    for x in getappointments:
        status = ''
        if not x.attended:
           color = 'blue'
        else:
           color = 'red'

        try:
            location = json.loads(requests.get('http://worldtimeapi.org/api/timezone/Africa/Lagos.json').text)
            znow = datetime.strptime(location['datetime'], '%Y-%m-%d %H:$M:%S')
        except Exception as e:
            print(e)
            now = datetime.now()
            ynow = now.strftime('%Y-%m-%d')
            znow = datetime.strptime(ynow, "%Y-%m-%d")
        
        adate = x.date.strftime('%Y-%m-%d')
        ddate = datetime.strptime(adate, "%Y-%m-%d")
        if znow > ddate:
            status = '[passed]'
            color = 'red'
        elif znow == ddate:
            color = 'green'
            status = '[current]'
        else:
            color = 'blue'
            status = '[upcoming]'
        date = x.date.strftime('%d/%m/%Y')
        time = x.time.strftime('%I:%M%p ')
        val = {'eventName': x.hospital + ' at ' + x.hospital_location + ' by ' + time + ' ' + status, 
			'calendar': 'Important', 
			'color':color, 
			'date': date, 
		}
        xList.append(val)
    data = xList
    status = {
			'status': 200,
			'data':data,
			'dataOne':[0, 0, 0, 0, 0, 0],
			'dataTwo':[0, 0, 0, 0, 0, 0],
			}

    return JsonResponse(status, safe=False)


def Request(request,name,email,phone,center,date,time,message):
    full_name = name.lower().lstrip().rstrip()
    email = email.lower().lstrip().rstrip()
    phone = phone.lower().lstrip().rstrip()
    center = center.lower().lstrip().rstrip()
    datex = date.lower().lstrip().rstrip()
    time = time.lower().lstrip().rstrip()
    message = message.lower().lstrip().rstrip()
    try:
        URL = 'https://safewayfx.com/api/v1/codeupblood/request/'+full_name+'/'+phone+'/'+email+'/'+center+'/'+datex+'/'+time+'/'+message
        ress = json.loads(requests.get(URL).text)
        if ress['status'] == 200 and ress['message'] == 'success':
            a = RA()
            a.name = full_name
            a.email = email
            a.phone = phone
            a.location = center
            a.date = datex
            a.time = time
            a.message = message
            a.save()
            status = {
                'status': ress['status'],
                }

    except Exception as e:
        print('>>>'+str(e))
        status = {
                'status': 500,
                'message': 'Internal Server Error'
                }

    return JsonResponse(status, safe=False)


def Hello(request,user_name,user_email,email_subject,email_message):
    full_name = user_name.lower().lstrip().rstrip()
    email = user_email.lower().lstrip().rstrip()
    subject = email_subject.lower().lstrip().rstrip()
    message = email_message.lower().lstrip().rstrip()
    try:
        # URL = 'https://safewayfx.com/api/v1/codeupblood/request/'+full_name+'/'+phone+'/'+email+'/'+center+'/'+datex+'/'+time+'/'+message
        # ress = json.loads(requests.get(URL).text)
        # if ress['status'] == 200 and ress['message'] == 'success':
        a = SH()
        a.name = full_name
        a.email = email
        a.subject = subject
        a.messagee = message
        a.expire = datetime.now() + timedelta(hours=24)
        a.save()
        status = {
            'status': 200,
            }

    except Exception as e:
        print('>>>'+str(e))
        status = {
                'status': 500,
                'message': 'Internal Server Error'
                }

    return JsonResponse(status, safe=False)


def Email(request,email):
    user = request.user
    email = email.lower().lstrip().rstrip()
    try:
        # URL = 'https://safewayfx.com/api/v1/codeupblood/request/'+full_name+'/'+phone+'/'+email+'/'+center+'/'+datex+'/'+time+'/'+message
        # ress = json.loads(requests.get(URL).text)
        # if ress['status'] == 200 and ress['message'] == 'success':
        if user != 'AnonymousUser':
            # user = user.lower().lstrip().rstrip()
            a = sub()
            a.name = user
            a.email = email
            a.expire = datetime.now() + timedelta(hours=24)
            a.save()
        else:
            a = sub()
            a.email = email
            a.expire = datetime.now() + timedelta(hours=24)
            a.save()
        status = {
            'status': 200,
            }

    except Exception as e:
        print('>>>'+str(e))
        status = {
                'status': 500,
                'message': 'Internal Server Error'
                }

    return JsonResponse(status, safe=False)


def Lga(request,lga):
    user = request.user
    if ' ' in lga and '-' in lga:
        _lga = lga.split(' ')
        lga = ''
        for x in range(len(_lga)):
            if '-' in _lga[x]:
                __lga = _lga[x].split('-')
                for y in range(len(__lga)):
                    lga = lga+__lga[y].title()
            else:
                lga = lga+_lga[x].title()
    elif ' ' in lga:
        _lga = lga.split(' ')
        lga = ''
        for x in range(len(_lga)):
            lga = lga+_lga[x].title()
    elif '-' in lga:
        _lga = lga.split('-')
        lga = ''
        for x in range(len(_lga)):
            lga = lga+_lga[x].title()
    else:
        lga = lga.title()
    try:
        LGA = hos.objects.filter(lga=lga.lower()).order_by('-created')
        if LGA.exists():
            xList = []
            for x in LGA:
                xList.append(x.name)
            status = 200
            data = xList
        else:
            status = 404
            data = {'hospital': 'No hospital found in this location'}
    except:
        status = 404
        data = {'hospital': 'No hospital found in this location'}

    status = {
            'status': status,
            'data':data,
            'message': 'Internal Server Error',
            }

    return JsonResponse(status, safe=False)


def confirm(request, demail):
	check = User.objects.filter(email=demail)
	if check.exists():
		for x in check:
			cemail = x.email
	else:
		cemail = 'Nil'
	if cemail == demail:
		status = {
				'email':demail,
				'status': 406,
			}
	else:
		status = {
				'status': 200,
			}

	return JsonResponse(status, safe=False)


def Send_code(request, demail):
	email = demail
	# xemail = 'www.spbiology@gmail.com'
	xemail = 'codeupblood@gmail.com'
	pkz = ran_gen(64,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
	subpk = ran_gen(10,'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
	now = datetime.now()
	xdate = now.strftime("%Y-%m-%d %H:%M:%S")
	year = now.strftime('%Y')
	one = email.replace("@", "{")
	try:
		subject = 'Activation Code Notification [CodeUp Blood]'
		c = {   'email': email,
				'one':one,  
		        'year' : year,
		        'pk':pkz,
		        'subpk':subpk,
		        }   
		text_content = render_to_string('email/AC.txt', c)
		html_content = render_to_string('email/AC.html', c)
		recipient_list = [xemail]
		yemail = EmailMultiAlternatives(subject, text_content, 'CodeUp Blood <lifeline@codeupblood.com>', recipient_list, headers={'Message-ID': 'Activation Code Notification [CodeUp Blood]'})
		yemail.attach_alternative(html_content, "text/html")
		yemail.send()
		passed = True
	except Exception as e:
		print(e)
		passed = False
		# passed = False
	if passed:
		try:
			data = AC()
			data.email = email
			data.pkz = pkz
			data.sub_pk = subpk
			data.expire = datetime.strptime(xdate, "%Y-%m-%d %H:%M:%S")
			data.save()
			status = {
				'email': email,
				'status': 200,
			}
		except:
			status = {
				'email': email,
				'status': 406,
			}

	else:
		status = {
			'email': email,
			'status': 500,
		}

	return JsonResponse(status, safe=False)


def createVolunteer(request,fname,lname,email,phone,city,state,tellus,where,what,why): 

    try:
        a = volu()
        a.first_name = fname
        a.last_name = lname
        a.email = email
        a.phone = phone
        a.city = city
        a.state = state
        a.tell_us = tellus
        a.where = where
        a.what = what
        a.why = why
        a.save()
        status = {
			'status': 200,
            'message':'Your form was successfully submited, You will be contacted soon'
		}
    except Exception as e:
        print(e)
        status = {
			'status': 500,
            'message':'An error occured, Try Again'
		}
    return JsonResponse(status, safe=False)





#================= FUCTIONS =================#
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))