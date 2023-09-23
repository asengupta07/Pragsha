from django.db import models
from django.utils import timezone
from authentification.models import User

class Broadcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    latitude = models.FloatField(max_length=200)
    longitude=models.FloatField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)
