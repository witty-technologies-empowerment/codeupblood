from django.db import models
from datetime import datetime
from django.utils import timezone
import random
import string
from taggit.managers import TaggableManager
import tagulous
from tagulous.models import TagModel

def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def Date(typex):
    if typex == 'blog':
        now = datetime.now()
        date = now.strftime("%b %d, %Y - %I:%M%r")
    return date

def CreateID(num, type_):
    if type_ == 'classid':
        code = ran_gen(num,'ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    else:
        code = ran_gen(num,'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789')
    return code

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.category


class HomeSlide(models.Model):
    picture = models.ImageField(upload_to='home/slide', blank=False)
    sub_title = models.CharField(max_length=40, blank=True)
    line_one = models.CharField(max_length=20, blank=True)
    line_two = models.CharField(max_length=20, blank=True)
    line_three = models.CharField(max_length=20, blank=True)
    donor = models.BooleanField(default=False)
    recipient = models.BooleanField(default=False)
    show  = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.sub_title + " - home slide."


class Feedback(models.Model):
    picture = models.ImageField(upload_to='home/feedback/picture', blank=False)
    username = models.CharField(max_length=25, blank=False)
    name = models.CharField(max_length=25, blank=False)
    job = models.CharField(max_length=10, blank=True)
    place_work = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=25, blank=True)
    message = models.CharField(max_length=200, blank=False)
    donor = models.BooleanField(default=False)
    recipient = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name + " - Feedback."


    def shrt(self):
        return self.message[:50]


class Campaign(models.Model):
    picture = models.ImageField(upload_to='home/campaign/post', blank=False)
    title = models.CharField(max_length=63, blank=False)
    author = models.CharField(max_length=50, blank=False)
    author_picture = models.ImageField(upload_to='home/campaign/author/picture', blank=False)
    author_bio = models.CharField(max_length=250, blank=False)
    tags = tagulous.models.TagField()
    message = models.CharField(max_length=2500, blank=False)
    shrt_message = models.CharField(max_length=145, blank=True)
    start_time = models.TimeField(auto_now_add=False)
    stop_time = models.TimeField(auto_now_add=False)
    location = models.CharField(max_length=25, blank=False)
    # Details
    date = models.DateField(auto_now_add=False)
    cost = models.CharField(max_length=20, blank=False)
    event_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    social_url = models.CharField(max_length=250, blank=False)
    # Organizer
    organizer = models.CharField(max_length=51, blank=False)
    organizer_phone = models.CharField(max_length=15, blank=False)
    organizer_email = models.CharField(max_length=65, blank=False)
    organizer_url = models.CharField(max_length=250, blank=False)
    # Venue
    venue = models.CharField(max_length=250, blank=False)
    venue_phone = models.CharField(max_length=15, blank=False)
    venue_email = models.CharField(max_length=250, blank=False)
    # social
    facebook = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    youtube = models.CharField(max_length=250, blank=True)
    instagram = models.CharField(max_length=250, blank=True)
    # 
    upcoming = models.BooleanField(default=True)
    current = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    # 
    show = models.BooleanField(default=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title + " - campaign."

    def xDate(self):
        # Tuesday, February 09, 2019 14 January, 2018
        return self.date.strftime('%d %B, %Y')
    
    def Shrt(self):
        return self.message[:145]


class RequestAppointment(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=15, blank=False)
    location = models.CharField(max_length=20, blank=False)
    date = models.CharField(max_length=12, blank=False)
    time = models.CharField(max_length=12, blank=False)
    message = models.CharField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name + " - appointment request."


class Gallery(models.Model):
    picture = models.ImageField(upload_to='home/gallery', blank=False)
    name = models.CharField(max_length=50, blank=False)
    message = models.CharField(max_length=500, blank=False)
    show  = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name + " - image."


class Blog(models.Model):
    picture = models.ImageField(upload_to='home/blog', blank=False)
    title = models.CharField(max_length=35, blank=False)
    author = models.CharField(max_length=50, blank=False)
    author_picture = models.ImageField(upload_to='home/blog/author/image', blank=False)
    author_bio = models.CharField(max_length=215, blank=False)
    # tags = TaggableManager()
    tags = tagulous.models.TagField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False)
    message = models.CharField(max_length=2500, blank=False)
    shrt_message = models.CharField(max_length=250, blank=False)
    # social
    facebook = models.CharField(max_length=250, blank=True)
    twitter = models.CharField(max_length=250, blank=True)
    instagram = models.CharField(max_length=250, blank=True)
    youtube = models.CharField(max_length=250, blank=True)
    show = models.BooleanField(default=True, blank=False)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title + " - blog."

    def xDate(self):
        # Tuesday, February 09, 2019 14 January, 2018
        return self.date.strftime('%B %d, %Y')
    
    def Shrt(self):
        return self.message[:250]


class Sponsor(models.Model):
    picture = models.ImageField(upload_to='home/sponsor', blank=False)
    name = models.CharField(max_length=150, blank=False)
    type_of_sponsor = models.CharField(max_length=150, blank=False)
    class_id = models.CharField(max_length=150, default=CreateID(5, 'classid'))
    as_person  = models.BooleanField(default=False)
    as_buiness  = models.BooleanField(default=False)
    show  = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name + " is a sponsor."


class Partner(models.Model):
    picture = models.ImageField(upload_to='home/partner', blank=False)
    name = models.CharField(max_length=150, blank=False)
    type_of_sponsor = models.CharField(max_length=150, blank=False)
    class_id = models.CharField(max_length=150, default=CreateID(5, 'classid'))
    as_person  = models.BooleanField(default=False)
    as_buiness  = models.BooleanField(default=False)
    show  = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name + " is a partner."


class SayHello(models.Model):
    name = models.CharField(max_length=150, blank=False)
    email = models.CharField(max_length=250, blank=False)
    subject = models.CharField(max_length=750, blank=False)
    message = models.CharField(max_length=10000, blank=False)
    expire = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        now = timezone.now()
        if now <= self.expire:
            return self.name + " said hello. [NEW]"
        else:
            return self.name + " said hello."


class Subscriber(models.Model):
    name = models.CharField(max_length=150, blank=False, default='Anonymous User')
    email = models.CharField(max_length=250, blank=False)
    expire = models.DateTimeField(auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        now = timezone.now()
        if now <= self.expire:
            return self.name + " Subscriber. [NEW]"
        else:
            return self.name + " Subscriber."


class Hospital(models.Model):
    name = models.CharField(max_length=150, blank=False)
    address = models.CharField(max_length=250, blank=False)
    lga = models.CharField(max_length=250, blank=False)
    contact = models.CharField(max_length=250, blank=False)
    picture = models.ImageField(upload_to='home/hospital', blank=False)
    show = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.show:
            return self.name + " in " + self.lga + ". [SHOWING]"
        else:
            return self.name + " in " + self.lga + "."


