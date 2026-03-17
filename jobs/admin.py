from django.contrib import admin

from .models import JobListingCache


@admin.register(JobListingCache)
class JobListingCacheAdmin(admin.ModelAdmin):
    list_display = ('query_desc', 'fetched_at')
    search_fields = ('query_desc',)
    readonly_fields = ('query_hash', 'fetched_at')
