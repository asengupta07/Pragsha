from django.shortcuts import render
from django import forms
from .models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    phone = forms.CharField(max_length=10, label="Phone Number")
    dob = forms.DateField(input_formats=[
        '%d/%m/%Y',
        '%Y-%m-%d',      # '2006-10-25'
        '%d-%m-%Y',      # '25-10-2006'
        '%m/%d/%Y',      # '10/25/2006'
        '%m/%d/%y'       # '10/25/06'
        ], label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    aaadhar = forms.CharField(label="Aadhar Number", min_length=12, max_length=12, widget=forms.PasswordInput)
    address = forms.CharField(max_length=100, label="Address", widget=forms.Textarea)
    password = forms.CharField(max_length=100, label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, label="Confirm Password", widget=forms.PasswordInput)
    emer1_name = forms.CharField(max_length=100, label="Emergency Contact 1 Name")
    emer1_number = forms.CharField(max_length=10, label="Emergency Contact 1 Number")
    emer1_address = forms.CharField(max_length=100, required=False, label="Emergency Contact 1 Address", widget=forms.Textarea)
    emer2_name = forms.CharField(max_length=100, label="Emergency Contact 2 Name")
    emer2_number = forms.CharField(max_length=10, label="Emergency Contact 2 Number")
    emer2_address = forms.CharField(max_length=100, required=False, label="Emergency Contact 2 Address", widget=forms.Textarea)
    class Meta:
        model = User
        fields = ['name', 'phone', 'dob', 'aaadhar', 'address', 'emer1_name', 'emer1_number', 'emer1_address', 'emer2_name', 'emer2_number', 'emer2_address', 'password']


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': RegisterForm()
        })
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            form.cleaned_data.pop('confirm_password')
            hashed_password = make_password(form.cleaned_data['password'])
            form.instance.password = hashed_password
            form.save()
            return render(request, 'register.html', {
                'form': RegisterForm(),
                'success': True
            })
        else:
            return render(request, 'register.html', {
                'form': form
            })