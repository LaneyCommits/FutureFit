from django.urls import path

from . import views

urlpatterns = [
    path("today/", views.today_insight_view, name="insights_today"),
    path("career-match/", views.career_match_view, name="insights_career_match"),
    path("compare/", views.compare_view, name="insights_compare"),
    path("saved-pattern/", views.saved_pattern_view, name="insights_saved_pattern"),
    path("weekly-reflection/", views.weekly_reflection_view, name="insights_weekly"),
    path("career-feed/", views.career_feed_view, name="insights_career_feed"),
]
