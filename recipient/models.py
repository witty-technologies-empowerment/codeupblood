from django.db import models

# Create your models here.

class RecipientDetail(models.Model):
    full_name  = models.CharField(max_length=150, blank=False)
    username   = models.CharField(max_length=150, blank=False)
    gender     = models.CharField(max_length=150, blank=False)
    bloodtype  = models.CharField(max_length=150, blank=False)
    email      = models.CharField(max_length=150, blank=False)
    telephone  = models.CharField(max_length=150, blank=False)
    state      = models.CharField(max_length=150, blank=False)
    password   = models.CharField(max_length=150, blank=False)
    created    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.username + ' - accounts'