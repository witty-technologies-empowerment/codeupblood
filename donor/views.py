from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
import calendar
import random
import requests
import json
from django.contrib.auth.models import User
# 
from .models import Appointment as APP, FAQ as faq, DonorDetail as DD, SafetyTip as ST
from accounts.models import AccountPath as AP
from django.contrib.sessions.backends.db import SessionStore


# Create your views here.


def iniT(xuser):
	initLR = User.objects.filter(username=xuser)
	for x in initLR:
		FN = x.first_name
		LN = x.last_name
	init = FN[0].upper()+LN[0].upper()
	return init

def HexCode(xuser):
	get_color = AP.objects.filter(username=xuser)
	for x in get_color:
			hexcode = x.color_code
	if hexcode.startswith('#'):
		hexcode = hexcode
	else:
		random_number = random.randint(0,16777215)
		hex_number = format(random_number,'x')
		hex_number = '#'+hex_number
		for x in get_color:
			a = AP()
			a.pk = x.pk
			a.username = x.username
			a.color_code = hex_number
			a.path = x.path
			a.created = x.created
			a.save()
		return HttpResponseRedirect(reverse('accounts:home'))
	return hexcode

def getTime():
	xList = []
	try:
		location = json.loads(requests.get('http://worldtimeapi.org/api/timezone/Africa/Lagos.json').text)
		datex = location['datetime']
		has_time = True
		xList.append(datex[:19])
		xList.append(has_time)
	except Exception as e:
		print(e)
		datex = ''
		has_time = False
		xList.append(datex)
		xList.append(has_time)
	return xList

@login_required(login_url='/accounts/donor/auth')
def DonorHome(request):
	user_login = request.user

	MONTHS_NUM = 3
	double_months_list = calendar.month_name[1:] * 2
	today_month = datetime.now().month + 12
	first_month = today_month - MONTHS_NUM
	last_months = double_months_list[first_month:today_month][::-1]
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	appointCom = APP.objects.filter(username=user_login,attended=True).count()
	appointPend = APP.objects.filter(username=user_login,x_status='pending').count()
	appointUncom = APP.objects.filter(username=user_login,x_status='uncomplete').count()
	alluser = User.objects.all().count()
	xMnth = last_months[2]
	yMnth = last_months[0]
	if getappointmentx.exists():
		for x in getappointmentx:
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	xList = []
	getappointments = APP.objects.filter(username=user_login)
	appointCom = APP.objects.filter(username=user_login,attended=True).count()
	appointPend = APP.objects.filter(username=user_login,x_status='pending').count()
	appointUncom = APP.objects.filter(username=user_login,x_status='uncomplete').count()
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	for x in getappointments:
		# try:
		# 	location = json.loads(requests.get('http://worldtimeapi.org/api/timezone/Africa/Lagos.json').text)
		# 	znow = datetime.strptime(location['datetime'], '%Y-%m-%d %H:$M:%S')
		# except Exception as e:
		# 	print(e)
		now = datetime.now()
		ynow = now.strftime('%Y-%m-%d')
		znow = datetime.strptime(ynow, "%Y-%m-%d")
		adate = x.date.strftime('%Y-%m-%d')
		ddate = datetime.strptime(adate, "%Y-%m-%d")
		if znow > ddate:
			statusx = 'PASSED'
		elif znow == ddate:
			statusx = 'CURRENT'
		else:
			statusx = 'asdf'
		if x.attended:
			statuc = 'Completed'
		else:
			statuc = 'Uncompleted'
		val = {'pkz': x.pk,
			'hospital': x.hospital, 
			'hospital_location': x.hospital_location, 
			'yDate':x.yDate, 
			'time': x.time, 
			'xDate': x.xDate,
			'status': statusx, 
			'statuc': statuc, 
		}
		xList.append(val)
	now = datetime.now()
	xYear = now.strftime('%Y')
	today = now.strftime('%d/%m/%Y')
	if last_months[0].lower() == 'april' or last_months[0].lower() == 'june' or last_months[0].lower() == 'september' or last_months[0].lower() == 'november':
		zMnth = 30
	elif last_months[0].lower() != 'april' or last_months[0].lower() != 'june' or last_months[0].lower() != 'september' or last_months[0].lower() != 'november':
		zMnth = 31
	elif int(xYear) % 4 == 0 and last_months[0].lower() == 'february ':
		zMnth = 29
	else:
		zMnth = 28
	if request.method == 'POST':
		action = request.POST.get('actBtn')
		action = action.split('-')
		if action[0] == 'delete':
			get_appoint = APP.objects.filter(pk=action[1])
			for x in get_appoint:
				a = APP()
				a.pk = x.pk
				a.delete()
			return HttpResponseRedirect(reverse('donor:home'))
	data = {
		'homey':True,
		'xMnth':xMnth,
		'yMnth':yMnth,
		'xYear':xYear,
		'zMnth':zMnth,
		'today':today,
		'appoints':xList,
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'has_time':getTime()[1],
		'recent':recent,
		'manage':manage,
		'alluser':alluser,
		'date':getTime()[0],
		'appointCom':appointCom,
		'appointPend':appointPend,
		'appointUncom':appointUncom,
	}
	return render(request, 'donor/home.html', data)


@login_required(login_url='/accounts/donor/auth')
def DonorPending(request):
	user_login = request.user
	
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	
	data = {
		'appoint':getappointments,
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'recent':recent,
		'manage':manage,
		'has_time':getTime()[1],
		'date':getTime()[0],
	}
	return render(request, 'donor/pending.html', data)


@login_required(login_url='/accounts/donor/auth')
def donorComplete(request):
	user_login = request.user
	getappointments = APP.objects.order_by('created').filter(username=user_login,attended=True)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	getappointments = APP.objects.order_by('created').filter(username=user_login,attended=True)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False

	data = {
		'appoint':getappointments,
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'has_time':getTime()[1],
		'date':getTime()[0],
		'recent':recent,
		'manage':manage,
	}
	return render(request, 'donor/comp.html', data)


@login_required(login_url='/accounts/donor/auth')
def donorMedic(request):
	user_login = request.user
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	data = {
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'has_time':getTime()[1],
		'date':getTime()[0],
		'recent':recent,
		'manage':manage,
	}
	return render(request, 'donor/medic.html', data)


@login_required(login_url='/accounts/donor/auth')
def donorFAQ(request):
	user_login = request.user
	s = SessionStore()
	print(s.session_key)
	print(']]]]]]')
	print(s)
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	get_all_faq = faq.objects.filter(show_on_dashboard=True).order_by('created')
	data = {
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'has_time':getTime()[1],
		'date':getTime()[0],
		'get_all_faq':get_all_faq,
		'recent':recent,
		'manage':manage,
	}
	return render(request, 'donor/faq.html', data)


@login_required(login_url='/accounts/donor/auth')
def donorSafety(request):
	user_login = request.user
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	get_all_st = ST.objects.filter(show_on_dashboard=True).order_by('created')
	data = {
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'has_time':getTime()[1],
		'date':getTime()[0],
		'get_all_st':get_all_st,
		'recent':recent,
		'manage':manage,
	}
	return render(request, 'donor/sup.html', data)


@login_required(login_url='/accounts/donor/auth')
def Profile(request):
	user_login = request.user
	MONTHS_NUM = 3
	double_months_list = calendar.month_name[1:] * 2
	today_month = datetime.now().month + 12
	first_month = today_month - MONTHS_NUM
	last_months = double_months_list[first_month:today_month][::-1]
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	xMnth = last_months[2]
	yMnth = last_months[0]
	getappointments = APP.objects.order_by('created').filter(username=user_login)
	if getappointments.exists():
		manage = True
	else:
		manage = False
	getappointmentx = APP.objects.order_by('created').filter(username=user_login)[:1]
	if getappointmentx.exists():
		for x in getappointmentx:
			# Aug 5, 2021 15:00:00
			xNext = x.created.strftime('%Y-%m-%d %H:%M:%S')
			yNext = x.next_appointment_due_date_time.strftime('%Y-%m-%d %H:%M:%S')
			xNext = datetime.strptime(xNext, '%Y-%m-%d %H:%M:%S')
			yNext = datetime.strptime(yNext, '%Y-%m-%d %H:%M:%S')
			if yNext > xNext:
				recent = True
			else:
				recent = False
	else:
		recent = False
	details = DD.objects.filter(username=user_login)
	for x in details:
		phone = x.telephone
		add_ = x.address
		city = x.city
		state = x.state
		cou = x.country
		blood = x.bloodtype
		gender = x.gender

	now = datetime.now()
	xYear = now.strftime('%Y')
	today = now.strftime('%d/%m/%Y')
	if last_months[0].lower() == 'april' or last_months[0].lower() == 'june' or last_months[0].lower() == 'september' or last_months[0].lower() == 'november':
		zMnth = 30
	elif last_months[0].lower() != 'april' or last_months[0].lower() != 'june' or last_months[0].lower() != 'september' or last_months[0].lower() != 'november':
		zMnth = 31
	elif int(xYear) % 4 == 0 and last_months[0].lower() == 'february ':
		zMnth = 29
	else:
		zMnth = 28

	address = add_ + ", " + city + ", " + state + ", " + cou + "."
	data = {
		'init':iniT(user_login),
		'hex_number':HexCode(user_login),
		'has_time':getTime()[1],
		'date':getTime()[0],
		# 'get_all_faq':get_all_faq,
		'recent':recent,
		'manage':manage,
		'phone':phone,
		'blood':blood,
		'blood':blood,
		'address':address,
		'gender':gender,
		'xMnth':xMnth,
		'yMnth':yMnth,
		'zMnth':zMnth,
	}
	return render(request, 'donor/profile.html', data)

@login_required(login_url='/accounts/donor/auth')
def donor_signout(request):
	auth = request.user
	message = 'You have successfully signed out'
	logout(request)
	context = {
			'message':message,
			'auth':auth,
			}
	return HttpResponseRedirect(reverse('accounts:donor_login'))

