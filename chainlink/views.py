from django.shortcuts import render
from chainlink.models import BloodDonation
from django.generic.views import (
    CreateView, 
    DetailView, 
    View
)

from chainlink.forms import BloodTestForm, BloodDonationForm, PackageForm



# *********************************** [REST_API VIEWS] ******************
# *********************************** [HTTP VIEWS] **********************
#* BloodTest Views
def blood_test(request):
    if request.method == 'POST':
        form = BloodTestForm(request.POST)
        if form.is_valid():
            form.save()
    
    template_name = 'chainlink/bloodtest_form.html'
    context = {'form': BloodTestForm()}
    return render(request, template_name, context)

#* BloodDonation Views
def create_donation_point_code(code_length):
    return ''.join()


def create_donation_point(request):
    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            form.save()
    
    template_name = 'chainlink/bloodtest_form.html'
    context = {'form': BloodDonationForm()}
    return render(request, template_name, context)

#* Package Views
def create_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save()
            # todo: call set_exp_date method on package
            # package.exp_date = 
    
    template_name = 'chainlink/bloodtest_form.html'
    context = {'form': BloodDonationForm()}
    return render(request, template_name, context)

def distribute_packages(request):
    pass

