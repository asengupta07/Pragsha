from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    dob = models.DateField()
    aaadhar = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    emer1_name = models.CharField(max_length=100)
    emer1_number = models.CharField(max_length=10)
    emer1_address = models.CharField(max_length=100, blank=True)
    emer2_name = models.CharField(max_length=100)
    emer2_number = models.CharField(max_length=10)
    emer2_address = models.CharField(max_length=100, blank=True)