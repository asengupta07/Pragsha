from django.db import models
from agency.models import Agency

# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    to_agency = models.ForeignKey(Agency, related_name="to_agency", on_delete=models.CASCADE)
    from_agency = models.ForeignKey(Agency, related_name="from_agency", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# class Unread(models.Model):
#     agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
#     Unread = models.BooleanField(default=True)