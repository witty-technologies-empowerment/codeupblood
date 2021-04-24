from django.urls import path
from . import views

app_name = 'subadmin' 

urlpatterns = [
    path('', views.SAHome, name='SAHome'),
    path('register', views.SAReg, name='sareg'),
    path('register/waiting!=<xuser>', views.Waiting, name='sawaiting'),
    path('login', views.SALogin, name='salogin'),
    path('activate/<demail>/pk=<pk>-<subpk>', views.admin_active, name='saactive'),
    path('all_users/donors', views.SADonor , name='sadonor'),
    path('all_users/recipent', views.SAReci , name='sareci'),
    path('appointments', views.SAAppoint , name='saappoint'),
    path('partners', views.SAPart , name='sapart'),
    path('sponsors', views.SASpon , name='saspon'),
    path('say-hello', views.SASay , name='sasay'),
    path('subscribers', views.SASub , name='sasub'),
    path('payments', views.SAPay , name='sapay'),
    path('survey', views.SASur , name='sasurv'),
    path('blog', views.SABlog , name='sablog'),
    path('campaigns', views.SACamp , name='sacamp'),
    path('faqs', views.SAFaq , name='safaq'),
    path('feedbacks', views.SAFeebback , name='safeedback'),
    path('gallery', views.SAGallery , name='sagallery'),
    path('homeslides', views.SAHslide , name='sahside'),
    path('hospital', views.SAHos , name='sahospital'),
    path('logout', views.LogOut , name='logout'),
]