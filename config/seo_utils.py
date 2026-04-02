"""Helpers for canonical public URLs (SEO, sitemaps, JSON-LD)."""
from django.conf import settings


def get_public_base_url(request) -> str:
    configured = (getattr(settings, "SITE_PUBLIC_URL", None) or "").strip().rstrip("/")
    if configured:
        return configured
    return request.build_absolute_uri("/").rstrip("/")
