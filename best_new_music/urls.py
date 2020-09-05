from django.urls import path
from . import views

urlpatterns = [
    path("", views.bestnewmusic, name="best_new_music"),
    path("added/", views.added, name="added"),
]
