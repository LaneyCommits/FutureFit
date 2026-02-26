from django.db import models


class College(models.Model):
    """College/university from College Scorecard (IPEDS) data."""

    unitid = models.BigIntegerField(unique=True, db_index=True)  # IPEDS UNITID
    name = models.CharField(max_length=255, db_index=True)

    city = models.CharField(max_length=128, blank=True, default="")
    state = models.CharField(max_length=2, blank=True, default="", db_index=True)

    website_url = models.URLField(blank=True, default="")
    image_url = models.URLField(
        blank=True,
        default="",
        help_text="Campus image URL (e.g. from Wikipedia or school website)",
    )

    # Institution type: public, private, for_profit
    institution_type = models.CharField(
        max_length=20,
        choices=[
            ("public", "Public"),
            ("private", "Private"),
            ("for_profit", "For-profit"),
        ],
        default="public",
        db_index=True,
    )

    # Cost and admissions (nullable - Scorecard often has PrivacySuppressed)
    tuition_in = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Average cost of attendance or in-state tuition (annual)",
    )
    acceptance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Admission rate 0-100",
    )
    undergrad_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Undergraduate enrollment (for size: small <2k, medium 2k-15k, large 15k+)",
    )

    # Top programs from CIPTITLE1-6, mapped to our major keys
    strong_majors = models.JSONField(
        default=list,
        blank=True,
        help_text="List of major keys matching career_quiz (e.g. computer_science, engineering)",
    )
    known_for = models.JSONField(
        default=list,
        blank=True,
        help_text="Raw CIPTITLE values from Scorecard (e.g. 'Computer Science')",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.state})"
