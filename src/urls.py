"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import home as hm
from accounts import views as vw
from django.views.generic.base import TemplateView


urlpatterns = [
    path('_/', admin.site.urls),
    path('admin/', include('subadmin.urls')),
    path('home/', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('donor/', include('donor.urls')),
    path('api/v1/', include('api.urls')),
    path('api/v2/', include('api2.urls')),
    path('survey/', include('survey.urls')),
    path('volunteer/', include('volunteer.urls')),
    path('', hm, name='home'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),  #add the robots.txt file
    path('signout', vw.any_user_signout, name='signout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
