from django.shortcuts import render

# Create your views here.

def viewVolunteer(request):
    return render(request, 'volunteer/home.html')