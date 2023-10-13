import json
from django.shortcuts import render, redirect
from agency.models import Location, Agency, Department, Speciality
import ast

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

from sklearn.cluster import KMeans
import json
from userdash.models import Broadcast

# Inside the map_view function
def map_view(request):
    if 'agency_id' not in request.session:
        return redirect('/agency/login')
    
    agency_id = request.session['agency_id']
    
    # Retrieve coordinates from the Broadcast database
    broadcast_markers = Broadcast.objects.all()
    coordinates = [(marker.latitude, marker.longitude) for marker in broadcast_markers]

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters as needed
    kmeans.fit(coordinates)

    cluster_centers = kmeans.cluster_centers_

    # Convert cluster_centers to a list of dictionaries for JavaScript
    cluster_centers_data = [{
        'name': 'Cluster Center',
        'latitude': center[0],
        'longitude': center[1],
        'id': -1,  # You can use a unique identifier for cluster centers
    } for center in cluster_centers]

    # Retrieve other data as you did previously
    markers = Location.objects.all()
    marker_data = json.dumps([{
        'name': marker.agency_id.name,
        'latitude': marker.latitude,
        'longitude': marker.longitude,
        'id': marker.agency_id.agency_id,
    } for marker in markers if marker.agency_id.agency_id != agency_id])

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
        'cluster_centers_data': json.dumps(cluster_centers_data),
    })
