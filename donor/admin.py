from django.contrib import admin
from .models import DonorDetail, Appointment, FAQ, NewDonor, Donated, SafetyTip

# Register your models here.

admin.site.register(DonorDetail)
admin.site.register(Appointment)
admin.site.register(FAQ)
admin.site.register(NewDonor)
admin.site.register(Donated)
admin.site.register(SafetyTip)