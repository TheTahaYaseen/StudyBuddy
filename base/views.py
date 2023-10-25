from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login, logout

from django.db.models import Q

from .models import Room, Topic, User
from .forms import RoomForm


# Create your views here.

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            messages.error(request, "Username Does Not Exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home") 
        else:
            messages.error(request, "Username Or Password Is Incorrect!")
        


    context = {}
    return render(request, "base/login_register.html", context)

def home(request):

    search = request.GET.get("search")

    if search == None or search == "All":
        rooms = Room.objects.all()
    else:    
        rooms = Room.objects.filter(
            Q(topic__name__icontains=search) |
            Q(name__icontains=search) |
            Q(description__icontains=search) 
        )

    rooms_count = rooms.count()

    topics = Topic.objects.all()
    context = {"rooms" : rooms, "topics": topics, "rooms_count": rooms_count}
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

def delete_room(request, primary_key):
    room = Room.objects.get(id = primary_key)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"objectToDelete": f"The Room: {room}"}
    return render(request, "base/delete.html", context)