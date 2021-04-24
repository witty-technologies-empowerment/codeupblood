from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.Home, name='sHome'),
    path('done', views.done, name='done'),
    # path('donor/auth', views.donor_login, name='donor_login'),
]