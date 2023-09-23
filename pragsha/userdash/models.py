from django.db import models
from django.utils import timezone
from authentification.models import User

class Broadcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude=models.FloatField(default=0.0)
    timestamp = models.DateTimeField(default=timezone.now)
    is_accepted = models.BooleanField(default=False)
