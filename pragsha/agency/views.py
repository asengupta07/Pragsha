from django.shortcuts import render, redirect
from django import forms
import json
from .models import Agency, Location, Inventory, Department, Speciality
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# DEPTS = [
#     ('NDMA', 'National Disaster Management Authority'),
#     ('NDRF', 'National Disaster Response Force'),
#     ('IMD', 'India Meteorological Department'),
#     ('NRSC', 'National Remote Sensing Centre'),
#     ('CWC', 'Central Water Commission'),
#     ('FSCD', 'Fire Service and Civil Defence'),
#     ('ICG', 'Indian Coast Guard'),
#     ('NHM', 'National Health Mission'),
#     ('NIDM', 'National Institute of Disaster Management'),
#     ('NDRelF', 'National Disaster Relief Fund'),
#     ('SDRF', 'State Disaster Relief Fund'),
#     ('IRCS', 'Indian Red Cross Society'),
#     ('CISF', 'Central Industrial Security Force'),
#     ('NDRC', 'National Disaster Response Corps'),
#     ('SDMA', 'State Disaster Management Authority'),
#     ('NGO', 'Non-Governmental Organisation'),
#     ('Other', 'Other')
# ]

INVENTORY = {
    "Firefighting Equipment": [
        "Fire Extinguishers",
        "Fire Hoses and Nozzles",
        "Fire Hydrant Wrenches",
        "Wildland Firefighting Tools",
    ],
    "Medical Supplies": [
        "Defibrillators",
        "Medical Kits and Supplies",
        "Oxygen Tanks and Masks",
        "Triage Kits",
        "Stretchers and Backboards",
        "Airway Management Equipment",
    ],
    "Emergency Food and Water Supplies": [
        "Non-Perishable Food Items",
        "Water Bottles or Water Purification Systems",
        "Food Preparation and Cooking Equipment",
    ],
    "Shelter and Bedding": [
        "Tents and Shelters",
        "Sleeping Bags and Blankets",
        "Tarps and Plastic Sheeting",
        "Portable Toilets and Sanitation Kits",
    ],
    "Search and Rescue Tools": [
        "First Aid Kits",
        "Stretchers",
        "Shovels and Picks",
        "Flashlights and Headlamps",
        "Life Vests and Personal Flotation Devices",
        "Rope and Harnesses",
        "Hydraulic Rescue Tools",
    ],
    "Personal Protective Equipment (PPE)": [
        "Helmets",
        "Gloves",
        "Respirators and Masks",
        "Hazmat Suits",
        "Safety Goggles",
    ],
    "Transportation": [
        "Emergency Vehicles",
        "Boats and Watercraft",
        "Helicopters and Aircraft",
    ],
    "Communication, Navigation, and Mapping Tools": [
        "GPS Devices",
        "Topographic Maps",
        "Compasses",
        "Two-Way Radios",
        "Satellite Phones",
        "Cell Phone Signal Boosters",
    ],
}


class InventoryForm(forms.ModelForm):
    agency_id = forms.CharField(widget=forms.HiddenInput, required=False)
    name = forms.CharField(max_length=100, label="Name")
    number = forms.IntegerField(label="Number")

    class Meta:
        model = Inventory
        fields = ["name", "number"]


def register(request):
    if request.method == "GET":
        if "agency_id" in request.session:
            return redirect("/agency/dashboard")
        return render(request, "agency/login.html")
    elif request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        regId = request.POST["regId"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        if (
            not name == ""
            or not email == ""
            or not regId == ""
            or not password == ""
            or not confirm_password == ""
            and password == confirm_password
        ):
            if Agency.objects.filter(regId=regId).exists():
                return render(request, "agency/login.html")
            password = make_password(password)
            agency = Agency(name=name, email=email, regId=regId, password=password)
            latitude = request.POST["latitude"]
            longitude = request.POST["longitude"]
            if latitude == "" or longitude == "":
                return render(request, "agency/login.html")
            location = Location(
                agency_id=agency, latitude=latitude, longitude=longitude
            )
            dept = request.POST.getlist("dept")
            if dept == []:
                return render(request, "agency/login.html")
            department = Department(agency_id=agency, name=dept)
            spec = request.POST["spec"]
            if spec == "":
                return render(request, "agency/login.html")
            speciality = Speciality(agency_id=agency, name=spec)
            agency.save()
            speciality.save()
            department.save()
            location.save()
            id = Agency.objects.get(regId=regId).agency_id
            request.session["agency_id"] = id
            return redirect("/agency/dashboard")
        else:
            return render(request, "agency/login.html")


def login(request):
    if request.method == "GET":
        if "agency_id" in request.session:
            return redirect("/agency/dashboard")
        return render(request, "agency/login.html")

    elif request.method == "POST":
        reg_id = request.POST["regId"]
        password = request.POST["password"]
        print(f"reg_id: {reg_id}")
        print(f"password: {password}")
        if not reg_id == "" or not password == "":
            try:
                agency = Agency.objects.get(regId=reg_id)
            except Agency.DoesNotExist:
                print("Does not exist")
                return render(request, "agency/login.html")

            if check_password(password, agency.password):
                request.session["agency_id"] = agency.agency_id
                return redirect("/agency/dashboard")
            else:
                return render(request, "agency/login.html")
        else:
            return render(request, "agency/login.html")


def logout(request):
    if "agency_id" in request.session:
        del request.session["agency_id"]
    return redirect("/agency/login")


@csrf_exempt
def add_inventory(request):
    if request.method == "POST":
        name = request.POST["name"]
        number = request.POST["number"]
        agency_id = Agency.objects.get(
            agency_id=request.session["agency_id"]
        )
        if Inventory.objects.filter(
            name=name,
            agency_id=agency_id
            ).exists():
            Inventory.objects.filter(
                name=name,
                agency_id=agency_id,
            ).update(
                number=Inventory.objects.filter(
                    name=name,
                    agency_id=agency_id,
                )
                .values("number")
                .first()["number"]
                + int(number)
            )
            data = {
                "id": Inventory.objects.filter(
                    name=name,
                    agency_id=agency_id,
                )
                .values("inventory_id")
                .first()["inventory_id"],
                "name": name,
                "number": Inventory.objects.filter(
                    name=name,
                    agency_id=agency_id,
                )
                .values("number")
                .first()["number"],
            }
        else:
            inventory = Inventory(
                agency_id=agency_id,
                name=name,
                number=number,
            )
            inventory.save()
            data = {
                "id": inventory.inventory_id,
                "name": inventory.name,
                "number": inventory.number,
            }
        return JsonResponse({"status": "success", "data": data})
    else:
        inv = Inventory.objects.filter(agency_id=request.session["agency_id"]).values()
        return render(
            request, "agency/inventory.html", {"form": InventoryForm(), "inv": inv, "inventory": INVENTORY}
        )
