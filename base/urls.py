from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("", views.home, name = "home"),
    # path("room/<datatype:identifier>", views.room, name = "room")
    path("room/<str:primary_key>", views.room, name = "room"),
    path("create-room/", views.create_room, name = "create-room"),
    path("update-room/<str:primary_key>", views.update_room, name = "update-room"),
    path("delete-room/<str:primary_key>", views.delete_room, name = "delete-room")
]