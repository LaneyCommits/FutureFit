"""Fetch campus images from Wikipedia and school websites (batch CLI)."""
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from schools.models import College
from schools.image_fetcher import fetch_wikipedia_image, fetch_website_image


class Command(BaseCommand):
    help = "Fetch campus images from Wikipedia and school websites for colleges missing images."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=0, help="Process only N colleges (0 = all).")
        parser.add_argument(
            "--source",
            choices=["wikipedia", "website", "both"],
            default="both",
            help="Where to fetch from.",
        )
        parser.add_argument("--delay", type=float, default=0.3, help="Seconds between requests.")
        parser.add_argument("--dry-run", action="store_true", help="Don't save to DB.")

    def handle(self, *args, **opts):
        limit = opts["limit"]
        source = opts["source"]
        delay = opts["delay"]
        dry_run = opts["dry_run"]

        qs = College.objects.filter(image_url="").order_by("name")
        if limit:
            qs = qs[:limit]

        total = qs.count()
        self.stdout.write(f"Processing {total} colleges (source={source})")

        fetched = 0
        for i, college in enumerate(qs, start=1):
            url = None
            if source in ("wikipedia", "both"):
                url = fetch_wikipedia_image(college.name, college.city or "", college.state or "")
            if not url and source in ("website", "both") and college.website_url:
                url = fetch_website_image(college.website_url)

            if url:
                fetched += 1
                if not dry_run:
                    with transaction.atomic():
                        college.image_url = url
                        college.save(update_fields=["image_url"])
            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(f"Done. Fetched {fetched} images."))
