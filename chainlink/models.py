from pyexpat import model
from django.db import models
from uuid import  uuid4
from django.utils import timezone


class BloodDonationCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    timestamp = models.DateTimeField(auto_now=timezone.now)

    def __str__()-> str:
        return self.code


class BloodDonation(models.Model):
    BLOOD_GROUP = [
        ('A-', 'A-'), 
        ('A+', 'A+'), 
        ('B-', 'B-'), 
        ('B+', 'B+'), 
        ('AB-', 'AB-'), 
        ('AB+', 'AB+'), 
        ('O-', 'O-'), 
        ('O+', 'O+'), 
    ]
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    firstname  = models.CharField(max_length=30)
    lastname  = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER, max_length=6)
    practicals_phone = models.CharField(max_length=11)
    blood_group = models.CharField(max_length=3, auto_created=True, default=timezone.now)
    reg_code = models.CharField(max_length=32, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_created=timezone.now)

    def __str__(self) -> str:
        return f'{self.fullname} | {self.timestamp}'

class BloodPackage(models.Model):
    id  = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    donation = models.ForeignKey(BloodDonation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_created=True, default=timezone.now)
    exp_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self._id} - {self.timestamp}'

    def set_exp_date(self):
        # TODO: add 4wks to exp_date
        pass

class Distribution(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    donation_point = models.ForeignKey(BloodDonation, on_delete=models.CASCADE)
    destination = models.TextField()
    timestamp = models.DateTimeField(auto_created=True, default=timezone.now)

    def __str__(self) -> str:
        pass

class Storage(models.Model):
    pass

    def __str__() -> str:
        pass

class Transfusion(models.Model):
    timestamp = models.DateTimeField(auto_created=True, default=timezone.now)

    def __str__(self) -> str:
        pass
