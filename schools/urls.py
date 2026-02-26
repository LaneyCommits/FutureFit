"""Schools/colleges app URLs: school finder."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.schools_home_view, name="schools_home"),
    path("api/fetch-images/", views.fetch_college_images_api, name="schools_fetch_images"),
]
