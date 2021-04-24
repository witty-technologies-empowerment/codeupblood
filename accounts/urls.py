from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountHome, name='accounthome'),
    path('donor/auth', views.donor_login, name='donor_login'),
    path('recipient/auth', views.rec_login, name='rec_login'),
    path('donor/auth/register', views.donor_reg, name='donor_reg'),
    path('recipient/auth/register', views.rec_reg, name='rec_reg'),
    path('donor/passwordrecover', views.donor_recover, name='donor_recover'),
    path('recipient/passwordrecover', views.rec_recover, name='rec_recover'),
    path('donor/auth/register/contact/details', views.donor_add, name='donor_add'),
    # path('contact', views.contact, name='contact'),
    # path('campaign', views.camp, name='camp'),
    # path('campaign/view', views.camp_view , name='camp_view '),
    # path('blog', views.blog , name='blog'),
    # path('blog/view', views.blog_view , name='blog_view'),
]