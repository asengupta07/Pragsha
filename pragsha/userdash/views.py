from django import forms
from .models import Broadcast
from authentification.models import User
from django.shortcuts import render, redirect


class BroadcastForm(forms.ModelForm):
    latitude=forms.FloatField(widget=forms.HiddenInput())
    longitude=forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Broadcast
        fields = ['latitude', 'longitude']

def dashboard(request):
    if "user_id" in request.session:
        if request.method == 'POST':
            form = BroadcastForm(request.POST)
            if form.is_valid():
                
                user = list(User.objects.filter(user_id=request.session["user_id"]))[0]
                broadcast = Broadcast(
                    name = user.name,
                    latitude = form.cleaned_data['latitude'],
                    longitude = form.cleaned_data['longitude'],
                    user = user
                )
                broadcast.save()
                return redirect('dashboard')
        else:
            form = BroadcastForm()
        return render(request, 'dashboard.html', {'form': form})
    else:
        return redirect("/user/login")

