from django.db import models
from django.utils import timezone
from authentification.models import User

class Broadcast(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude=models.FloatField(default=0.0)
    timestamp = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    type = models.TextField()


class Query(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    description = models.TextField()
    locality = models.TextField()
    tags = models.CharField(max_length=100) # comma separated
    timestamp = models.DateTimeField(default=timezone.now)
    is_answered = models.BooleanField(default=False)
    answer = models.TextField(default="")