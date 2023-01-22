
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:id>", views.profiles, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("save/<int:id>", views.save, name="save"),
    path("following", views.following, name="following"),

    # Json
    path("jsons", views.jsons, name="jsons"),

    # API
    path("new_post", views.new_post, name="new_post"),
    path("like_post/<int:id>", views.like_post, name="like_post"),

    # path("network/<str:view_post>", views.view_post, name="view_post"),
]
