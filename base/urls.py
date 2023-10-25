from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    # path("room/<datatype:identifier>", views.room, name = "room")
    path("room/<str:primary_key>", views.room, name = "room")
]