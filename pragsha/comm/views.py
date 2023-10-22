from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from .models import Message
from agency.models import Agency
import json

NEW = {}

# Create your views here.
def chat(request):
    if request.method == "POST":
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(agency_id=agency_id)
        to = request.POST["user"]
        print(to)
        message = Message(
            to_agency=Agency.objects.get(agency_id=to),
            from_agency=agency,
            message=request.POST["message"],
        )
        message.save()
        NEW[int(to)] = True
        print(NEW)
        return redirect("/chat/")
    agency_id = request.session["agency_id"]
    agency = Agency.objects.get(agency_id=agency_id)
    messages = list(Message.objects.filter(Q(from_agency=agency) | Q(to_agency=agency)).order_by("created_at").reverse().values())
    for message in messages:
        message["created_at"] = clean_time(message["created_at"])
    users = get_users(messages, agency_id)
    texts = get_messages(users, messages, agency_id)
    # print(json.dumps(texts, indent=4))
    rev = texts
    for key in texts:
        rev[key] = list(reversed(texts[key]))
    # print(json.dumps(rev, indent=4))
    # print(json.dumps(messages, indent=4))
    return render(request, "chat.html", {"texts": texts, "users": list(enumerate(users)), "rev": rev})


def get_users(messages, agency_id):
    users = []
    for message in messages:
        if message["from_agency_id"] == agency_id and message["to_agency_id"] not in users:
            users.append(message["to_agency_id"])
        elif message["to_agency_id"] == agency_id and message["from_agency_id"] not in users:
            users.append(message["from_agency_id"])
    return users


def clean_time(time):
    ist_offset = timedelta(hours=5, minutes=30)
    return (time+ist_offset).strftime("%H:%M:%S")


def get_messages(users, messages, agency_id):
    texts = {}
    for i in users:
        li = []
        for message in messages:
            if i == message["from_agency_id"] or i == message["to_agency_id"]:
                text = {}
                if message["from_agency_id"] == agency_id:
                    text["type"] = "me"
                else:
                    text["type"] = "you"
                text["message"] = message["message"]
                text["time"] = message["created_at"]
                li.append(text)
        texts[i] = li
    return texts
                

def create(request):
    if request.method == "POST":
        agency_id = request.session["agency_id"]
        agency = Agency.objects.get(agency_id=agency_id)
        to = request.POST["to"]
        print(to)
        text = request.POST["message"]
        print(text)
        message = Message(
            to_agency=Agency.objects.get(agency_id=to),
            from_agency=agency,
            message=request.POST["message"],
        )
        message.save()
        return redirect("/chat/")
    else:
        return redirect("/chat/")
    
def update(request):
    agency_id = request.session["agency_id"]
    print(NEW)
    print(agency_id)
    if agency_id in NEW:
        new = {
            "new": NEW[agency_id]
        }
        NEW[agency_id] = False
        return JsonResponse(new)
    else:
        new = {
            "new": False
        }
        return JsonResponse(new)
