from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    starttime = models.DateTimeField()
    createtime = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return self.name


class Guest(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.IntegerField()
    createtime = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20)
    sign = models.BooleanField()


