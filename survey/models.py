from django.db import models
from django.utils import timezone


# Create your models here.

class Survey(models.Model):
    email = models.CharField(max_length=250, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    telephone = models.CharField(max_length=20, blank=False)
    gender = models.CharField(max_length=12, blank=False)
    mail = models.BooleanField(default=True)
    answer_one = models.CharField(max_length=500, blank=False)
    answer_two = models.CharField(max_length=20, blank=False)
    answer_three = models.CharField(max_length=20, blank=False)
    answer_four  = models.CharField(max_length=20, blank=False)
    answer_five = models.CharField(max_length=20, blank=False)
    answer_six = models.CharField(max_length=20, blank=False)
    answer_seven = models.CharField(max_length=500, blank=False)
    answer_eight = models.CharField(max_length=20, blank=False)
    answer_nine = models.CharField(max_length=500, blank=False)
    answer_ten = models.CharField(max_length=200, blank=False)
    expire = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        now = timezone.now()
        if now <= self.expire:
            return self.email + " - Survey answer. [NEW]"
        else:
            return self.email + " - Survey answer."
