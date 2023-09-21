import json
from django.shortcuts import render
from agency.models import Location

# Create your views here.
def map_view(request):
    markers = Location.objects.all()
    marker_data = json.dumps([{
        'name': 'test',
        'latitude': marker.latitude,
        'longitude': marker.longitude,
    } for marker in markers])
    return render(request, 'agencydash/map.html', {'marker_data': marker_data})