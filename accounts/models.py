from django.db import models

# Create your models here.

class AccountPath(models.Model):
    username   = models.CharField(max_length=30, blank=False)
    color_code = models.CharField(max_length=10, blank=False)
    path       = models.CharField(max_length=30, blank=False)
    created    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.path == 'donor':
            return self.username + ' is Donor.'
        elif self.path == 'admin':
            return self.username + ' is Admin.'
        else:
            return self.username + ' is Recipient.'
