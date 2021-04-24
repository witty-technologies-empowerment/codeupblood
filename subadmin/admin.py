from django.contrib import admin
from .models import subAdmin, ActivationCode

# Register your models here.

admin.site.register(subAdmin)
admin.site.register(ActivationCode)