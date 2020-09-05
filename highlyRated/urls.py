from django.urls import path
from . import views

urlpatterns = [
    path("", views.highly_rated, name="highly_rated"),
    path("added/", views.added, name="added"),
]
