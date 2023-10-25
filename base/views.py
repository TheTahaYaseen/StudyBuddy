from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Room
from .forms import RoomForm

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

def create_room(request):
    form = RoomForm()
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form, "isUpdate": False}
    return render(request, "base/room_form.html", context)

def update_room(request, primary_key):
    
    room = Room.objects.get(id = primary_key)
    
    form = RoomForm(instance = room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form, "isUpdate": True}

    return render(request, "base/room_form.html", context)