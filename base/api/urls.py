from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_routes),
    path("rooms/", views.get_rooms),
    path("rooms/<str:primary_key>", views.get_room),
]