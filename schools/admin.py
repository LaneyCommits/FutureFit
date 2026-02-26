from django.contrib import admin
from .models import College


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "institution_type", "tuition_in", "acceptance_rate")
    list_filter = ("institution_type", "state")
    search_fields = ("name", "city")
