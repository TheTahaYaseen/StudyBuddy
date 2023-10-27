from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view, name = "login"),
    path("register", views.register_view, name = "register"),
    path("logout", views.logout_view, name = "logout"),
    path("", views.home, name = "home"),
    # path("room/<datatype:identifier>", views.room, name = "room")
    path("room/<str:primary_key>", views.room, name = "room"),
    path("user-profile/<str:primary_key>", views.user_profile, name = "user-profile"),
    path("create-room/", views.create_room, name = "create-room"),
    path("update-room/<str:primary_key>", views.update_room, name = "update-room"),
    path("delete-room/<str:primary_key>", views.delete_room, name = "delete-room"),
    path("delete-message/<str:primary_key>", views.delete_message, name = "delete-message"),
    path("update-profile/<str:primary_key>", views.update_profile, name = "update-profile")
]