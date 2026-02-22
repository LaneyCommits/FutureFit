"""
URL configuration for Project7.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resume_analysis.urls')),
    path('career-quiz/', include('career_quiz.urls')),
    path('resume/', include('resume.urls')),
    path('colleges/', include('schools.urls')),
]
