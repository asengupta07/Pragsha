from django.db import models

# Create your models here.
class Agency(models.Model):
    agency_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    regId = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Speciality(models.Model):
    speciality_id = models.AutoField(primary_key=True)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    agency_id = models.ForeignKey(Agency, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.IntegerField() 