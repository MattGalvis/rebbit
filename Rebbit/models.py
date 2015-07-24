import uuid

from django.db import models
from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.username, self.first_name, self.last_name)

class Sub_rebb(models.Model):
    sub_r = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % (self.sub_r)

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    creator = models.ForeignKey(Person)
    rpost = models.CharField(max_length=500)
    subreddit = models.ForeignKey(Sub_rebb)
    id = str(uuid.uuid4())
    count = 0

    def __unicode__(self):
        return u'%s %s' % (self.rpost, self.subreddit)

class comments(models.Model):
    class Meta:
        unique_together = ('count', 'creator')
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(Person)
    comment = models.CharField(max_length=1000)
    subreddit = models.ForeignKey(Sub_rebb)
    count = models.IntegerField(default=0)

class vote(models.Model):
    pass
