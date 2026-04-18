from django.urls import path

from . import views

urlpatterns = [
    path("types/", views.types_view, name="careers_types"),
    path("recommendations/", views.recommendations_view, name="careers_recommendations"),
    path("jobs/", views.jobs_list_view, name="careers_jobs"),
]
