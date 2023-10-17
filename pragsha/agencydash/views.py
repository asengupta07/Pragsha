import json
from django.shortcuts import render, redirect
from agency.models import Location, Agency, Department, Speciality
import ast
from userdash.models import Broadcast
from agencydash.helper import funky

DEPTS = {
    'National Disaster Management Authority': 'NDMA',
    'National Disaster Response Force': 'NDRF',
    'India Meteorological Department': 'IMD',
    'National Remote Sensing Centre': 'NRSC',
    'Central Water Commission': 'CWC',
    'Fire Service and Civil Defence': 'FSCD',
    'Indian Coast Guard': 'ICG',
    'National Health Mission': 'NHM',
    'National Institute of Disaster Management': 'NIDM',
    'National Disaster Relief Fund': 'NDReF',
    'State Disaster Relief Fund': 'SDRF',
    'Indian Red Cross Society': 'IRCS',
    'Central Industrial Security Force': 'CISF',
    'National Disaster Response Corps': 'NDRC',
    'State Disaster Management Authority': 'SDMA',
    'Non-Governmental Organisation': 'NGO',
    'Other': 'Other'
}

# Inside the map_view function
def response(request):
    if 'agency_id' not in request.session:
        return redirect('/agency/login')
    if request.method == 'GET':
        return redirect('/agency/dashboard')
    if request.method == 'POST':
        agency_id = request.session['agency_id']
        id = request.POST['id']
        address = request.POST['address']
        broadcast = Broadcast.objects.get(id=id)
        mission = {
            'id': id,
            'name': broadcast.name,
            'latitude': broadcast.latitude,
            'longitude': broadcast.longitude,
            'address': address,
            'type': broadcast.type,
            'timestamp': broadcast.timestamp,
        }
        markers = Location.objects.all()
        marker_data = json.dumps([{
            'name': marker.agency_id.name,
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            'id': marker.agency_id.agency_id,
        } for marker in markers if marker.agency_id.agency_id != agency_id])
        emergency = json.dumps({
            'latitude': mission['latitude'],
            'longitude': mission['longitude'],
        })
        agencies = Agency.objects.all()
        ags = []
        for agency in agencies:
            specs = Speciality.objects.filter(agency_id=agency)
            depts = Department.objects.filter(agency_id=agency)
            spec_name = [spec.name for spec in specs][0]
            dept_names = ast.literal_eval([dept.name for dept in depts][0])
            ags.append(dict(agency_id=agency.agency_id, name=agency.name, email=agency.email, depts=dept_names, specs=spec_name))
        
        agency_name = Agency.objects.get(agency_id=agency_id).name
        available_departments = [{'key': key, 'value': value} for key, value in DEPTS.items()]
        
        return render(request, 'agencydash/map.html', {
            'marker_data': marker_data,
            'agency_name': agency_name,
            'ags': json.dumps(ags),
            'available_departments': available_departments,
            'mission': mission,
            'emergency': emergency,
        })


def dash(request):
    if 'agency_id' not in request.session:
        return redirect('/agency/login')
    addresses = funky()
    markers = Broadcast.objects.all()
    marker_data = json.dumps([{
        'name': marker.name,
        'latitude': marker.latitude,
        'longitude': marker.longitude,
        'id': marker.id,
    } for marker in markers])
    disasters = [{
        'name': marker.name,
        'latitude': marker.latitude,
        'longitude': marker.longitude,
        'address': addresses[marker.id],
        'type': marker.type,
        'id': marker.id,
    } for marker in markers]
    return render (request, 'agencydash/dash.html', {
        'marker_data': marker_data,
        'disasters': disasters,
        'agency_name': 'YOU',
    })
    
    