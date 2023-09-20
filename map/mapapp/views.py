import csv
from django.shortcuts import render, redirect
from .models import MyModel

def add_data(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST['name']
        description = request.POST['description']

        # Create a new record in the database
        MyModel.objects.create(name=name, description=description)

        # Write the data to a CSV file
        with open('data.csv', mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, description])

        return redirect('add_data')  # Redirect back to the form

    return render(request, 'mapapp/add_data.html')



# Create your views here.
