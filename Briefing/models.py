from django.db import models
from django.conf import settings

from django.contrib.auth.models import User 

class FeedType(models.IntegerChoices):
        RSS = 1
        ATOM = 2
        REST = 3

class Feed(models.Model):
    format = models.IntegerField(choices=FeedType.choices)
    url = models.CharField(max_length=250)
    headers = models.TextField()
    file = models.TextField()
    date_last_scan = models.DateTimeField()

class Site(models.Model):
    title = models.CharField(max_length=150)
    link = models.CharField(max_length=250)
    feed = models.TextField()
    source_type = FeedType.choices

class Tab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    widgets = models.TextField()
    date_modified = models.DateTimeField()
    date_created  = models.DateTimeField(auto_now_add=True, blank=True,editable=False)
