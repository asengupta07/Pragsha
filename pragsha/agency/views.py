from django.shortcuts import render, redirect
from django import forms
from .models import Agency, Location
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(max_length=100, label="Email")
    regId = forms.CharField(max_length=100, label="Registration ID")
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, label="Confirm Password", widget=forms.PasswordInput)
    class Meta:
        model = Agency
        fields = ['name', 'email', 'regId', 'password']

class LocationForm(forms.ModelForm):
    agency_id = forms.CharField(widget=forms.HiddenInput, required=False)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']


def register(request):
    if request.method == 'GET':
        return render(request, 'registration.html', {
            'form': RegisterForm(),
            'loc': LocationForm()
        })
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        loc = LocationForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm_password'] and loc.is_valid():
            form.cleaned_data.pop('confirm_password')
            hashed_password = make_password(form.cleaned_data['password'])
            form.instance.password = hashed_password
            agency = form.save()
            location = Location(
                agency_id=agency,
                latitude=loc.cleaned_data['latitude'],
                longitude=loc.cleaned_data['longitude']
            )
            location.save()
            return render(request, 'registration.html', {
                'form': RegisterForm(),
                'loc': LocationForm(),
                'success': True
            })
        else:
            return render(request, 'registration.html', {
                'form': form,
                'location': loc
            })
        

class LoginForm(forms.Form):
    regId = forms.CharField(max_length=100, label="Registration ID")
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': LoginForm()})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            reg_id = form.cleaned_data['regId']
            password = form.cleaned_data['password']
            try:
                agency = Agency.objects.get(regId=reg_id)
            except Agency.DoesNotExist:
                return render(request, 'login.html', {
                    'form': form,
                    'error_message': 'Invalid Registration ID or Password'
                })

            if check_password(password, agency.password):
                # Passwords match, log in the user.
                # You can implement your authentication logic here.
                # For example, you can set a session variable or use Django's built-in authentication system.
                # For this example, I'll just redirect to a success page.
                return redirect('/agency/register')  # Replace 'success_page' with your actual success page URL.
            else:
                return render(request, 'login.html', {
                    'form': form,
                    'error_message': 'Invalid Registration ID or Password'
                })