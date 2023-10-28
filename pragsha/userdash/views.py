from .models import Query, Broadcast
from authentification.models import User
from agency.models import Agency, Location, Speciality, Department
from django.shortcuts import render, redirect
from django.http import JsonResponse as JSON
import json
from datetime import timedelta
import requests
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

def dashboard(request):
    if not 'user_id' in request.session:
        return redirect('/user/login')
    return render(request, 'dashboard.html')

def get_queries(request):
    if not 'user_id' in request.session:
        return redirect('/user/login')
    Queries = list(Query.objects.filter(is_answered=True))
    qjson = [
        {
            'author': q.user.name,
            'question': q.question,
            'description': q.description,
            'locality': q.locality,
            'tags': q.tags.split(','),
            'timestamp': clean_time(q.timestamp),
            'answer': [s.strip("'") for s in q.answer.split("','")]
        }
    for q in Queries]
    return JSON(qjson, safe=False)

def clean_time(time):
    ist_offset = timedelta(hours=5, minutes=30)
    return (time+ist_offset).strftime("%d-%m-%Y %H:%M")


def sos(request):
    if not 'user_id' in request.session:
        return redirect('/user/login')
    return render(request, 'sos.html')

def broadcast(request):
    if not 'user_id' in request.session:
        return redirect('/user/login')
    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(user_id=user_id)
        broadcast = Broadcast(
            user=user,
            name=user.name,
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude'],
            type=request.POST['type']
        )
        broadcast.save()
    return render(request, 'sos1.html')


def get_response(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('question')
        qjson = json.dumps(
            {
                'question': question
            }
        )
        response = requests.post('https://f27a-34-87-132-227.ngrok.io',data=qjson)
        response = {
            'response': response.json()['answer'].strip().rstrip("User")
        }
        return JSON(response, safe=False)
    

def chatbot(request):
    if not 'user_id' in request.session:
        return redirect('/user/login')
    return render(request, 'chatbot.html')


def map(request):
    if 'user_id' not in request.session:
        return redirect('/user/login')
    if request.method == 'GET':
        markers = Location.objects.all()
        marker_data = json.dumps([{
            'name': marker.agency_id.name,
            'latitude': marker.latitude,
            'longitude': marker.longitude,
            'id': marker.agency_id.agency_id,
        } for marker in markers])
        agencies = Agency.objects.all()
        ags = []
        for agency in agencies:
            specs = Speciality.objects.filter(agency_id=agency)
            depts = Department.objects.filter(agency_id=agency)
            spec_name = [spec.name for spec in specs][0]
            dept_names = ast.literal_eval([dept.name for dept in depts][0])
            ags.append(dict(agency_id=agency.agency_id, name=agency.name, email=agency.email, depts=dept_names, specs=spec_name))
        available_departments = [{'key': key, 'value': value} for key, value in DEPTS.items()]
        return render(request, 'usermap.html', {
            'marker_data': marker_data,
            'agency_name': 'YOU',
            'ags': json.dumps(ags),
            'available_departments': available_departments,
        })
