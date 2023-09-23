from django import forms
from .models import Broadcast
from django.shortcuts import render, redirect


class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ['name', 'latitude', 'longitude']

def dashboard(request):
    if "user_id" in request.session:
        if request.method == 'POST':
            form = BroadcastForm(request.POST)
            if form.is_valid():
                broadcast = form.save(commit=False)
                broadcast = Broadcast()
                user = User(request.session["user_id"])
                broadcast.user = request.user
                broadcast.save()
                return redirect('dashboard')
        else:
            form = BroadcastForm()
        return render(request, 'dashboard.html', {'form': form})
    else:
        return redirect("/user/login")
