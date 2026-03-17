from django.urls import path
from . import views

urlpatterns = [
    path('', views.jobs_home, name='jobs_home'),
]
