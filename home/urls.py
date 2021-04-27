from django.urls import path
from . import views

app_name = 'home' 

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('ourhospital', views.hos, name='hos'),
    path('campaign', views.camp, name='camp'),
    path('campaign/view', views.camp_view , name='camp_view '),
    path('blog', views.blog , name='blog'),
    path('blog/view/<shrt>/<lng>', views.blog_view , name='blog_view'),
    path('gallery', views.gallery , name='gallery'),
    path('faq', views.faq , name='faq'),
    path('ourteams', views.team , name='team'),
    path('testimonies', views.test , name='test'),
    path('service', views.serv , name='serv'),
]