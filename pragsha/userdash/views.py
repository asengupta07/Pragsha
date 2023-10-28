from .models import Query
from django.shortcuts import render, redirect
from django.http import JsonResponse as JSON
import json
from datetime import timedelta


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