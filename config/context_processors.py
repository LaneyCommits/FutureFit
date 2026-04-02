"""Template context: site-wide SEO defaults and JSON-LD."""
import json

from django.conf import settings

from config.seo_utils import get_public_base_url

DEFAULT_SITE_DESCRIPTION = (
    "ExploringU helps students explore careers with a free personality-style career quiz, "
    "resume and cover letter templates, admissions writing tools, college search, student job "
    "listings, and articles on jobs and writing—built for anyone still figuring it out."
)


def site_seo(request):
    base = get_public_base_url(request)
    static_rel = settings.STATIC_URL
    if not static_rel.startswith("/"):
        static_rel = "/" + static_rel.lstrip("/")
    logo_url = f"{base}{static_rel}images/header-logo.png"

    desc = DEFAULT_SITE_DESCRIPTION
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{base}/#website",
                "url": f"{base}/",
                "name": "ExploringU",
                "description": desc,
                "publisher": {"@id": f"{base}/#organization"},
                "inLanguage": "en-US",
            },
            {
                "@type": "Organization",
                "@id": f"{base}/#organization",
                "name": "ExploringU",
                "url": f"{base}/",
                "logo": logo_url,
                "description": desc,
            },
        ],
    }

    return {
        "SITE_PUBLIC_URL": base,
        "SEO_DEFAULT_IMAGE": logo_url,
        "SEO_SITE_DESCRIPTION": desc,
        "seo_json_ld": json.dumps(graph),
        "GOOGLE_SITE_VERIFICATION": getattr(settings, "GOOGLE_SITE_VERIFICATION", "") or "",
    }
