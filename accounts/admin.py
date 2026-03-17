from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

    list_display = BaseUserAdmin.list_display + ("email", "is_active")
    list_filter = BaseUserAdmin.list_filter + ("is_active",)
    search_fields = BaseUserAdmin.search_fields + ("email",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "major_key", "base_style")
    list_filter = ("major_key", "base_style")
    search_fields = ("user__username", "user__email")
