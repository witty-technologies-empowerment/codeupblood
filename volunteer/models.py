from django.db import models

# Create your models here.

class Volunteer(models.Model):
	telegram = models.CharField(max_length=100, blank=True)
	first_name = models.CharField(max_length=100, blank=False)
	last_name = models.CharField(max_length=100, blank=False)
	email = models.CharField(max_length=250, blank=False)
	phone = models.CharField(max_length=50, blank=False)
	city = models.CharField(max_length=50, blank=False)
	state = models.CharField(max_length=50, blank=False)
	tell_us = models.CharField(max_length=500, blank=False)
	where = models.CharField(max_length=50, blank=False)
	what = models.CharField(max_length=500, blank=False)
	why = models.CharField(max_length=500, blank=False)
	verified = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['created']

	def __str__(self):
		if self.verified:
			return self.first_name + " " + self.last_name + " is volunteering"
		else:
			return self.first_name + " " + self.last_name + " has submitted a volunteering form"

