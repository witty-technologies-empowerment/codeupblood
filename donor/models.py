from django.db import models
import random
import string
from datetime import datetime
from django.utils import timezone


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def makeID():
    _str = ran_gen(6,'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return _str

# Create your models here.

class DonorDetail(models.Model):
    full_name  = models.CharField(max_length=150, blank=False)
    username   = models.CharField(max_length=150, blank=False)
    gender     = models.CharField(max_length=150, blank=False)
    bloodtype  = models.CharField(max_length=150, blank=False)
    email      = models.CharField(max_length=150, blank=False)
    telephone  = models.CharField(max_length=150, blank=False)
    address      = models.CharField(max_length=150, blank=False)
    city      = models.CharField(max_length=150, blank=False)
    state      = models.CharField(max_length=150, blank=False)
    country      = models.CharField(max_length=150, blank=False)
    password   = models.CharField(max_length=150, blank=False)
    created    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.username + ' - accounts'


class Appointment(models.Model):
    full_name          = models.CharField(max_length=150, blank=False)
    username           = models.CharField(max_length=150, blank=False)
    date               = models.DateField(auto_now_add=False)
    time               = models.TimeField(auto_now_add=False)
    donor_id           = models.CharField(max_length=20, blank=False)
    telephone          = models.CharField(max_length=20, blank=False)
    hospital           = models.CharField(max_length=500, blank=False)
    hospital_location  = models.CharField(max_length=750, blank=False)
    state              = models.CharField(max_length=50, blank=False)
    lga                = models.CharField(max_length=100, blank=False)
    d_id               = models.CharField(max_length=50, blank=False, default=makeID())
    x_status           = models.CharField(max_length=100, default='pending')
    attended           = models.BooleanField(default=False, blank=False)
    status             = models.BooleanField(default=False, blank=False)
    next_appointment_due_date_time = models.DateTimeField(auto_now_add=False)
    created            = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.attended:
            return self.username + ' with donor ID ' +  self.donor_id + ' [attended the appointment]'
        else:
            return self.username + ' with donor ID ' +  self.donor_id + ' [upcoming appointment]'

    def xDate(self):
        return self.date.strftime('%Y/%m/%d')
    
    def zDate(self):
        return self.date.strftime('%Y-%m-%d')
    
    def passDate(self):
        aDate = self.date.strftime('%b %d, %Y')
        aTime = self.time.strftime('%H:%M:00')
        xTime = aDate + ' ' + aTime
        return xTime
    
    def yDate(self):
        # Tuesday, February 09, 2019
        return self.date.strftime('%A, %B %d, %Y')



class FAQ(models.Model):
    title            = models.CharField(max_length=125, blank=False)
    answer_space_one = models.CharField(max_length=1000, blank=True)
    answer_space_two = models.CharField(max_length=1000, blank=True)
    show_on_dashboard           = models.BooleanField(default=True, blank=False)
    show_on_home             = models.BooleanField(default=True, blank=False)
    created          = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.show_on_dashboard:
            return 'Question with title ' + self.title + ' [showing]'
        else:
            return 'Question with title ' + self.title + ' [not showing]'



class SafetyTip(models.Model):
    title            = models.CharField(max_length=125, blank=False)
    answer = models.CharField(max_length=1000, blank=True)
    show_on_dashboard           = models.BooleanField(default=True, blank=False)
    show_on_home             = models.BooleanField(default=True, blank=False)
    created          = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.show_on_dashboard:
            return 'Safety Tip with title ' + self.title + ' [showing]'
        else:
            return 'Safety Tip with title ' + self.title + ' [not showing]'



class NewDonor(models.Model):
    user    = models.CharField(max_length=125, blank=False)
    expires = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        now = timezone.now()
        if self.expires < now :
            return self.user + ' new status has expired'
        else:
            return self.user + ' is still NEW'



class Donated(models.Model):
    user    = models.CharField(max_length=125, blank=False)
    has_donated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.has_donated:
            return self.user + ' has donated'
        else:
            return self.user + ' has NOT donated'
