from django.urls import path
from . import views

app_name = 'donor'

urlpatterns = [
    path('', views.DonorHome, name='home'),
    path('pending', views.DonorPending, name='pending'),
    path('completed', views.donorComplete, name='complete'),
    path('medical-report', views.donorMedic, name='medic'),
    path('faq', views.donorFAQ, name='faq'),
    path('safety', views.donorSafety, name='safety'),
    path('profile', views.Profile, name='donorProfile'),
    path('signout', views.donor_signout, name='signout'),
]