from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('getStat', views.getStat, name='getStat'),
    path('getAppointment/<name>', views.getAppointment, name='getAppointment'),
    path('request/<name>/<email>/<phone>/<center>/<date>/<time>/<message>', views.Request, name='request'),
    path('sayHello/<user_name>/<user_email>/<email_subject>/<email_message>', views.Hello, name='hello'),
    path('sub/<email>', views.Email, name='email'),
    path('locate/hospital/<lga>', views.Lga, name='lga'),
    path('confirm/<demail>', views.confirm, name='confirm'),
    path('Send_code/<demail>', views.Send_code, name='Send_code'),
    path('validate/<date>', views.CheckDate, name='validate'),
    path('createappointment', views.createAppointment, name='appoint'),
    path('create/volunteer/<fname>/<lname>/<email>/<phone>/<city>/<state>/<tellus>/<where>/<what>/<why>', views.createVolunteer, name='vol'),
    # path('blog/view', views.blog_view , name='blog_view'),
]