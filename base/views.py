from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

rooms = [
    {
        "id": 1,
        "name": "Learn Python" 
    },
    {
        "id": 2,
        "name": "Frontend Flags " 
    },
    {
        "id": 3,
        "name": "Backend Bosses" 
    },
    {
        "id": 4,
        "name": "Peak Pythoners" 
    },
]

def home(request):
    context = {"rooms" : rooms}
    return render(request,  "base/home.html", context)

def room(request, primary_key):
    room = None
    for iteration in rooms:
        if iteration["id"] == int(primary_key):
            room = iteration 
                        
    context = {"room": room}
    return render(request,  "base/room.html", context)   