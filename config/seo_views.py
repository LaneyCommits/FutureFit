"""robots.txt and sitemap.xml for search engines."""
from datetime import datetime
from xml.sax.saxutils import escape

from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone as dj_tz

from blog.models import Post

from config.seo_utils import get_public_base_url

# Named URL patterns to expose to crawlers (main marketing / discovery pages).
SITEMAP_NAMED_URLS = [
    "home",
    "career_quiz_home",
    "resume_home",
    "resume_templates",
    "resume_tips",
    "resume_ai_tools",
    "schools_home",
    "jobs_home",
    "blog_index",
    "chat_home",
]


def robots_txt(request):
    base = get_public_base_url(request)
    lines = ["User-agent: *", "Allow: /", ""]
    if base and "localhost" not in base and "127.0.0.1" not in base:
        lines.insert(2, f"Sitemap: {base}/sitemap.xml")
    body = "\n".join(lines)
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    base = get_public_base_url(request)
    urls = []
    for name in SITEMAP_NAMED_URLS:
        try:
            path = reverse(name)
        except Exception:
            continue
        urls.append(
            {
                "loc": f"{base}{path}",
                "lastmod": None,
                "changefreq": "weekly",
                "priority": "0.8" if name == "home" else "0.7",
            }
        )

    for post in Post.objects.filter(published=True).only("slug", "updated_at"):
        try:
            path = reverse("blog_detail", kwargs={"slug": post.slug})
        except Exception:
            continue
        lm = dj_tz.localtime(post.updated_at)
        urls.append(
            {
                "loc": f"{base}{path}",
                "lastmod": lm,
                "changefreq": "monthly",
                "priority": "0.6",
            }
        )

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        parts.append("<url>")
        parts.append(f"<loc>{escape(u['loc'])}</loc>")
        if u["lastmod"]:
            if isinstance(u["lastmod"], datetime):
                parts.append(f"<lastmod>{u['lastmod'].strftime('%Y-%m-%d')}</lastmod>")
        parts.append(f"<changefreq>{u['changefreq']}</changefreq>")
        parts.append(f"<priority>{u['priority']}</priority>")
        parts.append("</url>")
    parts.append("</urlset>")
    xml = "\n".join(parts)
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")
