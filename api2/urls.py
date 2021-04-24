from django.urls import path
from . import views as vw
from .views import UserRecordView
from rest_framework.authtoken import views

app_name = 'api2'

urlpatterns = [
    path('create_user_id', vw.CreateUserID, name='createuserid'),
    path('user/', UserRecordView.as_view(), name='users'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]