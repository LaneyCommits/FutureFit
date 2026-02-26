"""
Import colleges from College Scorecard (ed.gov) Most-Recent-Cohorts-Institution data.
Maps CIPTITLE programs to our 16 major keys for quiz/filter compatibility.

Supports: local CSV/ZIP path, local directory (finds Most-Recent-Cohorts-Institution.csv),
or --url to download.
"""
import csv
import io
import os
import re
import zipfile
from decimal import Decimal
from urllib.request import urlopen

from django.core.management.base import BaseCommand
from django.db import transaction

from schools.models import College

# College Scorecard updates URLs periodically. Find the latest at:
# https://collegescorecard.ed.gov/data/ or https://data.ed.gov
DEFAULT_ZIP_URL = (
    "https://ed-public-download.app.cloud.gov/downloads/"
    "Most-Recent-Cohorts-Institution_04192023.zip"
)

INSTITUTION_CSV = "Most-Recent-Cohorts-Institution.csv"

COLS = [
    "UNITID",
    "INSTNM",
    "CITY",
    "STABBR",
    "INSTURL",
    "CONTROL",
    "PREDDEG",
    "UGDS",
    "COSTT4_A",
    "ADM_RATE",
    "CIPTITLE1",
    "CIPTITLE2",
    "CIPTITLE3",
    "CIPTITLE4",
    "CIPTITLE5",
    "CIPTITLE6",
]

# Map CIPTITLE text (case-insensitive substring) to our major keys
# Order: more specific matches first
CIP_TO_MAJOR = [
    # computer_science
    (r"computer science|information technology|cyber|software|networking|systems security", "computer_science"),
    # engineering
    (r"engineering|mechanical|civil|electrical|industrial|chemical|aerospace|biomedical", "engineering"),
    # cosmetology (before health - cosmetology is distinct)
    (r"cosmetology|barber|aesthetician|esthetician|nail technician|manicurist|make.?up artist|hair styling", "cosmetology"),
    # allied_health (clinical support roles - before broad "health")
    (r"medical assistant|clinical assistant|dental assisting|dental hygiene|sonography|ultrasound|radiologic|surgical technolog|phlebotomy|medical records|sterile processing|respiratory care therapy", "allied_health"),
    # health_sciences
    (r"nursing|registered nurse|practical nursing|medical|clinical|pharmacy|therapy|kinesiology|rehabilitation|physical therapy|occupational therapy", "health_sciences"),
    (r"biology|biomedical|anatomy|physiology", "health_sciences"),
    # fire_emergency
    (r"fire science|fire.?fighting|emergency medical|EMT|paramedic", "fire_emergency"),
    # culinary (before hospitality - culinary is cooking/baking)
    (r"culinary|baking|pastry|chef|cooking", "culinary"),
    # aviation_transportation
    (r"aviation|aircraft maintenance|airframe|truck.*driver|commercial vehicle|diesel mechanic", "aviation_transportation"),
    # education
    (r"education|teaching|curriculum", "education"),
    # law
    (r"law|criminal justice|legal|police science", "law"),
    # agriculture
    (r"agriculture|forestry|animal science|horticulture|natural resource", "agriculture"),
    # hospitality
    (r"hospitality|tourism|hotel", "hospitality"),
    # real_estate
    (r"real estate|property", "real_estate"),
    # sports_recreation
    (r"recreation|sport|athletic|parks", "sports_recreation"),
    # trades_construction
    (r"construction|trades|welding|automotive|manufacturing|precision production|electrician|plumbing|carpentry|HVAC|machine tool|metal", "trades_construction"),
    # environmental
    (r"environmental|sustainability|ecology|conservation", "environmental"),
    # communications
    (r"journalism|communication|media|broadcasting|public relations|advertising|cinematography|film|video production", "communications"),
    # humanities (before arts_design so "liberal arts" matches humanities not "arts")
    (r"liberal arts|general studies|liberal studies|humanities|interdisciplinary studies", "humanities"),
    (r"english|history|philosophy|language|literature|writing|rhetoric|religious studies", "humanities"),
    # arts_design
    (r"art|design|graphic|fine arts|architecture|music|theatre|theater|drama|jewelry", "arts_design"),
    # business
    (r"business|administration|accounting|finance|marketing|management|economics|office|secretarial|clerical", "business"),
    # social_sciences
    (r"psychology|sociology|political science|anthropology|criminology", "social_sciences"),
]


def clean(s):
    if s is None:
        return ""
    s = str(s).strip()
    return "" if s in {"NULL", "PrivacySuppressed", "NA", "N/A"} else s


def parse_int(val, default=None):
    if not val:
        return default
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def parse_decimal(val, default=None):
    if not val:
        return default
    s = str(val).strip()
    if s in ("NULL", "PrivacySuppressed", "NA", "N/A", ""):
        return default
    try:
        return Decimal(s)
    except (ValueError, TypeError, Exception):
        return default


def cip_titles_to_major_keys(titles):
    """Map list of CIPTITLE strings to our major keys (unique, ordered)."""
    seen = set()
    result = []
    for t in titles:
        if not t:
            continue
        t_lower = t.lower()
        for pattern, major in CIP_TO_MAJOR:
            if re.search(pattern, t_lower) and major not in seen:
                seen.add(major)
                result.append(major)
    return result


def control_to_type(control):
    """CONTROL: 1=Public, 2=Private nonprofit, 3=Private for-profit."""
    n = parse_int(control)
    if n == 1:
        return "public"
    if n == 2:
        return "private"
    if n == 3:
        return "for_profit"
    return "public"


def undergrad_to_size(ugds):
    """Convert UGDS to small/medium/large for frontend."""
    n = parse_int(ugds)
    if n is None:
        return "medium"
    if n < 2000:
        return "small"
    if n < 15000:
        return "medium"
    return "large"


def normalize_url(url):
    if not url:
        return ""
    url = url.strip()
    if url and not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


class Command(BaseCommand):
    help = "Download College Scorecard institution data and import colleges."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default="",
            help="Local path: CSV file, ZIP file, or directory containing Most-Recent-Cohorts-Institution.csv",
        )
        parser.add_argument("--url", default=os.getenv("SCORECARD_ZIP_URL", DEFAULT_ZIP_URL))
        parser.add_argument("--limit", type=int, default=0, help="Import only N rows (debug).")
        parser.add_argument(
            "--update-existing",
            action="store_true",
            help="Update rows if UNITID already exists.",
        )
        parser.add_argument(
            "--include-all",
            action="store_true",
            help="Include institutions with no undergrad data (default: degree-granting only).",
        )

    def _resolve_csv_source(self, path_arg, url_arg):
        """Return (file_handle, description) for CSV. Handles local path or URL download."""
        if path_arg:
            path = os.path.abspath(os.path.expanduser(path_arg))
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path not found: {path}")

            if os.path.isfile(path):
                if path.lower().endswith(".csv"):
                    self.stdout.write(f"Reading local CSV: {path}")
                    return open(path, "r", encoding="utf-8-sig", newline=""), path
                if path.lower().endswith(".zip"):
                    self.stdout.write(f"Reading local ZIP: {path}")
                    z = zipfile.ZipFile(path, "r")
                    csv_names = [n for n in z.namelist() if n.lower().endswith(".csv")]
                    if not csv_names:
                        raise RuntimeError("No CSV found in zip.")
                    f = z.open(csv_names[0])
                    return io.TextIOWrapper(f, encoding="utf-8-sig", newline=""), path
            elif os.path.isdir(path):
                csv_path = os.path.join(path, INSTITUTION_CSV)
                if not os.path.isfile(csv_path):
                    raise FileNotFoundError(
                        f"Expected {INSTITUTION_CSV} in directory: {path}"
                    )
                self.stdout.write(f"Reading: {csv_path}")
                return open(csv_path, "r", encoding="utf-8-sig", newline=""), csv_path

        self.stdout.write(f"Downloading: {url_arg}")
        with urlopen(url_arg, timeout=120) as resp:
            zip_bytes = resp.read()
        z = zipfile.ZipFile(io.BytesIO(zip_bytes), "r")
        csv_names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if not csv_names:
            raise RuntimeError("No CSV found in zip.")
        f = z.open(csv_names[0])
        return io.TextIOWrapper(f, encoding="utf-8-sig", newline=""), csv_names[0]

    def handle(self, *args, **opts):
        path_arg = opts["path"]
        url_arg = opts["url"]
        limit = opts["limit"]
        update_existing = opts["update_existing"]
        degree_only = not opts["include_all"]

        source = path_arg or url_arg
        csv_file, desc = self._resolve_csv_source(path_arg, url_arg)

        try:
            reader = csv.DictReader(csv_file)
            missing = [c for c in COLS if c not in reader.fieldnames]
            if missing:
                raise RuntimeError(
                    f"CSV missing columns: {', '.join(missing)}. "
                    "Scorecard format may have changed."
                )

            created = 0
            updated = 0
            skipped = 0

            with transaction.atomic():
                for i, row in enumerate(reader, start=1):
                    if limit and i > limit:
                        break

                    unitid = clean(row["UNITID"])
                    name = clean(row["INSTNM"])
                    if not unitid or not name:
                        skipped += 1
                        continue

                    unitid_int = int(unitid)

                    ugds = parse_int(row.get("UGDS"))
                    if degree_only and (ugds is None or ugds == 0):
                        skipped += 1
                        continue

                    known_for = [
                        clean(row.get(f"CIPTITLE{j}")) for j in range(1, 7)
                    ]
                    known_for = [k for k in known_for if k]
                    strong_majors = cip_titles_to_major_keys(known_for)
                    preddeg = parse_int(row.get("PREDDEG"))
                    if preddeg == 3 and "humanities" not in strong_majors:
                        strong_majors.append("humanities")

                    tuition = parse_int(row.get("COSTT4_A"))
                    adm_rate = parse_decimal(row.get("ADM_RATE"))
                    if adm_rate is not None:
                        adm_rate = min(100, max(0, adm_rate * 100))

                    defaults = {
                        "name": name,
                        "city": clean(row.get("CITY")),
                        "state": clean(row.get("STABBR"))[:2],
                        "website_url": normalize_url(clean(row.get("INSTURL"))),
                        "institution_type": control_to_type(row.get("CONTROL")),
                        "tuition_in": tuition,
                        "acceptance_rate": adm_rate,
                        "undergrad_count": ugds,
                        "strong_majors": strong_majors,
                        "known_for": known_for,
                    }

                    obj = College.objects.filter(unitid=unitid_int).first()
                    if obj:
                        if update_existing:
                            for k, v in defaults.items():
                                setattr(obj, k, v)
                            obj.save()
                            updated += 1
                        else:
                            skipped += 1
                    else:
                        College.objects.create(unitid=unitid_int, **defaults)
                        created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Done. created={created} updated={updated} skipped={skipped}"
                )
            )
        finally:
            if hasattr(csv_file, "close"):
                csv_file.close()
