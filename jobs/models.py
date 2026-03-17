import hashlib
from django.db import models
from django.utils import timezone


class JobListingCache(models.Model):
    """Cached job listings from the external API, keyed by query hash."""
    query_hash = models.CharField(max_length=64, unique=True, db_index=True)
    query_desc = models.CharField(max_length=255, blank=True)
    results_json = models.JSONField(default=list)
    fetched_at = models.DateTimeField(auto_now=True)

    TTL_MINUTES = 60

    @property
    def is_stale(self):
        age = (timezone.now() - self.fetched_at).total_seconds()
        return age > self.TTL_MINUTES * 60

    @classmethod
    def make_hash(cls, **kwargs):
        raw = '|'.join(f'{k}={v}' for k, v in sorted(kwargs.items()) if v)
        return hashlib.sha256(raw.encode()).hexdigest()

    def __str__(self):
        return f"JobListingCache({self.query_desc or self.query_hash[:12]})"
