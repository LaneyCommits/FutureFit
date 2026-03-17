"""Profile model (email verification removed)."""
from django.conf import settings
from django.db import models


class Profile(models.Model):
    """One-to-one profile: avatar, bio, AI personalization, job preferences."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    email_verified = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    bio = models.TextField(blank=True)

    major_key = models.CharField(max_length=64, blank=True, default='')
    PREFERRED_JOB_TYPE_CHOICES = [
        ('', 'Any'),
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    preferred_job_type = models.CharField(
        max_length=32, choices=PREFERRED_JOB_TYPE_CHOICES, default='', blank=True,
    )
    PREFERRED_REMOTE_CHOICES = [
        ('', 'Any'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('onsite', 'On-site'),
    ]
    preferred_remote = models.CharField(
        max_length=16, choices=PREFERRED_REMOTE_CHOICES, default='', blank=True,
    )
    preferred_location = models.CharField(max_length=128, blank=True, default='')
    min_salary = models.PositiveIntegerField(null=True, blank=True)

    # AI personalization (for chatbot and AI tools)
    custom_instructions = models.TextField(
        blank=True,
        help_text='How you want the AI to respond (e.g. tone, style).',
    )
    BASE_STYLE_CHOICES = [
        ('', 'Default'),
        ('friendly', 'Friendly'),
        ('professional', 'Professional'),
        ('concise', 'Concise'),
        ('detailed', 'Detailed'),
    ]
    base_style = models.CharField(
        max_length=32,
        choices=BASE_STYLE_CHOICES,
        default='',
        blank=True,
    )
    ai_toggles = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"
