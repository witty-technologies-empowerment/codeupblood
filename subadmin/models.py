from django.db import models

# Create your models here.

class subAdmin(models.Model):
	user = models.CharField(max_length=20)
	allowed = models.BooleanField(default=False)
	activated = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['-created']

	def __str__(self):
		if self.allowed:
			return self.user + " is ALLOWED to make changes"
		else:
			return self.user + " is not ALLOWED to make changes"



class ActivationCode(models.Model):
	email = models.CharField(max_length=100, unique=True)
	code = models.CharField(max_length=10, blank=True)
	expire = models.DateTimeField(auto_now_add=False, blank=True)
	pkz = models.CharField(max_length=64, unique=True)
	sub_pk = models.CharField(max_length=10, unique=True)
	used = models.BooleanField(default=False)
	sent = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
	    ordering = ['-created']
	
	def __str__(self):
		return 'Activation Code for ' + self.email + " (Expires - " + str(self.expire) + ")"