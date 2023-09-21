import json
from django.shortcuts import render, redirect
from agency.models import Location, Agency

# Create your views here.
def map_view(request):
    if 'agency_id' not in request.session:
        return redirect('/agency/login')
    agency_id = request.session['agency_id']
    markers = Location.objects.all()
    marker_data = json.dumps([{
        'name': marker.agency_id.name,
        'latitude': marker.latitude,
        'longitude': marker.longitude,
    } for marker in markers if marker.agency_id.agency_id != agency_id])
    agency_name = Agency.objects.get(agency_id=agency_id).name
    return render(request, 'agencydash/map.html', {'marker_data': marker_data, 'agency_name': agency_name})