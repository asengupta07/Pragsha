from django.contrib import admin
from .models import Agency, Location, Department, Speciality, Inventory

# Register your models here.
admin.site.register(Agency)
admin.site.register(Location)
admin.site.register(Department)
admin.site.register(Speciality)
admin.site.register(Inventory)
