from django.shortcuts import render
from .models import Survey as SV
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta


# Create your views here.

def Home(request):
    if request.method == 'POST':
        asda = request.POST.get('qOne')
        asdb = request.POST.get('qTwo')
        asdc = request.POST.get('qThree')
        asdd = request.POST.get('qFour')
        asdf = request.POST.get('qFive')
        asdg = request.POST.get('qSix')
        asdh = request.POST.get('qSeven')
        asdi = request.POST.get('qEight')
        asdj = request.POST.get('qNine')
        asdk = request.POST.get('qTen')
        asdl = request.POST.get('fOne')
        asdm = request.POST.get('fTwo')
        asdn = request.POST.get('fThree')
        asdo = request.POST.get('fFour')
        asdp = request.POST.get('fFive')
        asdq = request.POST.get('sendMail')
        
        if asdq == 'on':
            val = True
        else:
            val = False
        a = SV()
        a.email = asdn
        a.first_name = asdl
        a.last_name = asdm
        a.telephone = asdp
        a.gender = asdo
        a.mail = val
        a.answer_one = asda
        a.answer_two =  asdb
        a.answer_three = asdc 
        a.answer_four =  asdd
        a.answer_five =  asdf
        a.answer_six = asdg
        a.answer_seven =  asdh
        a.answer_eight = asdi
        a.answer_nine = asdj 
        a.answer_ten = asdk
        a.expire = datetime.now() + timedelta(hours=24) 
        a.save()

        return HttpResponseRedirect(reverse('survey:done'))


    return render(request, 'survey/home.html')


def done(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('survey:sHome'))
    return render(request, 'survey/done.html')