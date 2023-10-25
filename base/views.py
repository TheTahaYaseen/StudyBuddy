from django.http import HttpResponse
from django.shortcuts import render

from .models import Room

# Create your views here.

def home(request):
    rooms = Room.objects.all()
    context = {"rooms" : rooms}
    print(rooms)
    return render(request,  "base/home.html", context)

def room(request, primary_key):
    room = Room.objects.get(id = primary_key)
    context = {"room": room}
    return render(request,  "base/room.html", context)   