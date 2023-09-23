from django.shortcuts import render, redirect
from django import forms
from .models import Agency, Location, Inventory, Department, Speciality
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
DEPTS = [
    ('NDMA', 'National Disaster Management Authority'),
    ('NDRF', 'National Disaster Response Force'),
    ('IMD', 'India Meteorological Department'),
    ('NRSC', 'National Remote Sensing Centre'),
    ('CWC', 'Central Water Commission'),
    ('FSCD', 'Fire Service and Civil Defence'),
    ('ICG', 'Indian Coast Guard'),
    ('NHM', 'National Health Mission'),
    ('NIDM', 'National Institute of Disaster Management'),
    ('NDRelF', 'National Disaster Relief Fund'),
    ('SDRF', 'State Disaster Relief Fund'),
    ('IRCS', 'Indian Red Cross Society'),
    ('CISF', 'Central Industrial Security Force'),
    ('NDRC', 'National Disaster Response Corps'),
    ('SDMA', 'State Disaster Management Authority'),
    ('NGO', 'Non-Governmental Organisation'),
    ('Other', 'Other')
]


class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(max_length=100, label="Email")
    regId = forms.CharField(max_length=100, label="Registration ID")
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, label="Confirm Password", widget=forms.PasswordInput)
    class Meta:
        model = Agency
        fields = ['name', 'email', 'regId', 'password']

class InventoryForm(forms.ModelForm):
    agency_id = forms.CharField(widget=forms.HiddenInput, required=False)
    name = forms.CharField(max_length=100, label="Name")
    number = forms.IntegerField(label="Number")
    class Meta:
        model = Inventory
        fields = ['name', 'number']

class LocationForm(forms.ModelForm):
    agency_id = forms.CharField(widget=forms.HiddenInput, required=False)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']

class DepartmentForm(forms.Form):
    agency_id = forms.CharField(widget=forms.HiddenInput, required=False)
    dept = forms.CharField(max_length=100, label="Department", widget=forms.CheckboxSelectMultiple(choices=DEPTS))


class SpecialityForm(forms.Form):
    agency_id = forms.CharField(widget=forms.HiddenInput, required=False)
    spec = forms.CharField(max_length=100, label="Speciality", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))


def register(request):
    if request.method == 'GET':
        if 'agency_id' in request.session:
            return redirect('/agency/dashboard')
        return render(request, 'agency/registration.html', {
            'form': RegisterForm(),
            'loc': LocationForm(),
            'dept': DepartmentForm(),
            'spec': SpecialityForm()
        })
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        loc = LocationForm(request.POST)
        dept = DepartmentForm(request.POST)
        spec = SpecialityForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm_password'] and loc.is_valid() and dept.is_valid() and spec.is_valid():
            form.cleaned_data.pop('confirm_password')
            hashed_password = make_password(form.cleaned_data['password'])
            form.instance.password = hashed_password
            agency = form.save()
            location = Location(
                agency_id=agency,
                latitude=loc.cleaned_data['latitude'],
                longitude=loc.cleaned_data['longitude']
            )
            department = Department(
                agency_id=agency,
                name=dept.cleaned_data['dept']
            )
            speciality = Speciality(
                agency_id=agency,
                name=spec.cleaned_data['spec']
            )
            speciality.save()
            department.save()
            location.save()
            return render(request, 'agency/registration.html', {
                'form': RegisterForm(),
                'loc': LocationForm(),
                'dept': DepartmentForm(),
                'spec': SpecialityForm(),
                'success': True
            })
        else:
            return render(request, 'agency/registration.html', {
                'form': form,
                'location': loc
            })
        

class LoginForm(forms.Form):
    regId = forms.CharField(max_length=100, label="Registration ID")
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)

def login(request):
    if request.method == 'GET':
        if 'agency_id' in request.session:
            return redirect('/agency/dashboard')
        return render(request, 'agency/login.html', {'form': LoginForm()})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            reg_id = form.cleaned_data['regId']
            password = form.cleaned_data['password']
            try:
                agency = Agency.objects.get(regId=reg_id)
            except Agency.DoesNotExist:
                return render(request, 'agency/login.html', {
                    'form': form,
                    'error_message': 'Invalid Registration ID or Password'
                })

            if check_password(password, agency.password):
                request.session['agency_id'] = agency.agency_id
                return redirect('/agency/dashboard')
            else:
                return render(request, 'agency/login.html', {
                    'form': form,
                    'error_message': 'Invalid Registration ID or Password'
                })
            

def logout(request):
    if 'agency_id' in request.session:
        del request.session['agency_id']
    return redirect('/agency/login')


@csrf_exempt
def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.instance.agency_id = Agency.objects.get(agency_id=request.session['agency_id'])
            if Inventory.objects.filter(name=form.cleaned_data['name'], agency_id=request.session['agency_id']).exists():
                Inventory.objects.filter(name=form.cleaned_data['name'], agency_id=request.session['agency_id']).update(number=Inventory.objects.filter(name=form.cleaned_data['name'], agency_id=request.session['agency_id']).values('number').first()['number'] + form.cleaned_data['number'])
                data = {
                    'id': Inventory.objects.filter(name=form.cleaned_data['name'], agency_id=request.session['agency_id']).values('inventory_id').first()['inventory_id'],
                    'name': form.cleaned_data['name'],
                    'number': Inventory.objects.filter(name=form.cleaned_data['name'], agency_id=request.session['agency_id']).values('number').first()['number'],
                }
            else:
                inventory = form.save()
                data = {
                    'id': inventory.inventory_id,
                    'name': inventory.name,
                    'number': inventory.number,
                }
            return JsonResponse({'status': 'success', 'data': data})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        inv = Inventory.objects.filter(agency_id=request.session['agency_id']).values()
        return render(request, 'agency/inventory.html', {'form': InventoryForm(), 'inv': inv})