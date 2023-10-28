from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q

from .models import Room, Topic, User, Message
from .forms import RoomForm, UserForm


# Create your views here.

def login_view(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
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

    context = {"page": page}
    return render(request, "base/login_register.html", context)

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()         
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An Error Occured During Registration!")   

    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):

    search = request.GET.get("search") if request.GET.get("search") else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=search) |
        Q(name__icontains=search) |
        Q(description__icontains=search) 
    )

    activity_feed = Message.objects.filter(
            Q(room__name__icontains=search)
    )
    
    rooms_count = rooms.count()

    topics = Topic.objects.all()

    all_topics_count = topics.count()

    context = {"rooms" : rooms, "topics": topics[0:5], "rooms_count": rooms_count, "activity_feed": activity_feed, "search": search, "all_topics_count": all_topics_count}
    
    return render(request,  "base/home.html", context)

def room(request, primary_key):
    
    room = Room.objects.get(id = primary_key)

    conversations = room.message_set.all().order_by("-created")
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", primary_key=room.id)

    context = {"room": room, "conversations": conversations, "participants": participants}
    return render(request,  "base/room.html", context)   

def user_profile(request, primary_key):

    user = User.objects.get(id = primary_key)
    rooms = user.room_set.all()
    activity_feed = user.message_set.all()
    topics = Topic.objects.all()
    all_topics_count = topics.count()

    context = {"user": user, "rooms": rooms, "activity_feed": activity_feed, "topics": topics[0:5], "all_topics_count": all_topics_count}

    return render(request,  "base/profile.html", context)   

@login_required(login_url="/login")
def create_room(request):
    form = RoomForm()
    
    topics = Topic.objects.all()

    if request.method == "POST":
        form = RoomForm(request.POST)
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)


        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get("description"),
        )

        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()

        return redirect('home')

    context = {"form": form, "isUpdate": False, "topics": topics}
    return render(request, "base/room_form.html", context)

@login_required(login_url="/login")
def update_room(request, primary_key):
    
    room = Room.objects.get(id = primary_key)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("Only The Creator / Host Can Update The Room")

    form = RoomForm(instance = room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.topic = topic
        room.name = request.POST.get("name"),
        room.description = request.POST.get("description"),

        return redirect('home')


    context = {"form": form, "isUpdate": True, "topics": topics, "room": room}

    return render(request, "base/room_form.html", context)

@login_required(login_url="/login")
def delete_room(request, primary_key):

    room = Room.objects.get(id = primary_key)

    if request.user != room.host:
        return HttpResponse("Only The Creator / Host Can Delete The Room")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"objectToDelete": f"The Room: {room}"}
    return render(request, "base/delete.html", context)

@login_required(login_url="/login")
def delete_message(request, primary_key):

    message = Message.objects.get(id = primary_key)

    if request.user != message.user:
        return HttpResponse("Only The Commenter Can Delete The Comment")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    context = {"objectToDelete": f"The Message: {message}"}

    return render(request, "base/delete.html", context)

@login_required(login_url="/login")
def update_profile(request):

    user = request.user
    form = UserForm(instance=user) 

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", primary_key= user.id)

    context = {"user": user, "form": form}

    return render(request, "base/update_profile.html", context)

def topics(request):

    search = request.GET.get("search") if request.GET.get("search") else ""

    topics = Topic.objects.filter(
        Q(name__icontains=search)
    )

    context = {"topics": topics}
    return render(request, "base/topics.html", context)

def activities(request):

    search = request.GET.get("search") if request.GET.get("search") else ""

    activities = Message.objects.all()
    
    context = {"activities": activities}
    return render(request, "base/activity.html", context)