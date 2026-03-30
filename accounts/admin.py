from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailVerificationState, Profile

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
    list_display = ("user", "email_verified", "major_key", "base_style")
    list_filter = ("email_verified", "major_key", "base_style")
    search_fields = ("user__username", "user__email")


@admin.register(EmailVerificationState)
class EmailVerificationStateAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "last_sent_at", "failed_attempts")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("code_hash", "expires_at", "last_sent_at", "failed_attempts", "user")

    def has_add_permission(self, request):
        return False
