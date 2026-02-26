import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .schools_data import (
    get_schools,
    get_states,
    get_cost_brackets,
    get_all_major_labels,
)
from .image_fetcher import fetch_wikipedia_image, fetch_website_image
from .models import College


def schools_home_view(request):
    """Schools finder page with client-side filtering."""
    schools = get_schools()
    states = get_states()
    cost_brackets = get_cost_brackets()
    majors = get_all_major_labels()

    preselect_major = request.GET.get('major', '')

    # Resolve relative image paths (e.g. images/schools/ncstate.png) to full static URL
    schools_for_json = []
    for s in schools:
        d = dict(s)
        img = d.get('image', '')
        if img.startswith('images/'):
            d['image'] = request.build_absolute_uri(settings.STATIC_URL + img)
        schools_for_json.append(d)

    schools_json = json.dumps(schools_for_json)
    count = len(schools)
    count_display = "Over 5,000" if count >= 5000 else str(count)

    return render(request, "schools/home.html", {
        'schools_json': schools_json,
        'schools_count': count,
        'schools_count_display': count_display,
        'states': states,
        'cost_brackets': cost_brackets,
        'majors': majors,
        "preselect_major": preselect_major,
    })


def fetch_college_images_api(request):
    """Fetch campus images for colleges on the current page. ?ids=unitid1,unitid2,..."""
    ids_param = request.GET.get("ids", "")
    if not ids_param:
        return JsonResponse({"images": {}})

    raw_ids = [x.strip() for x in ids_param.split(",") if x.strip()]
    ids = raw_ids[:12]

    result = {}
    for unitid_str in ids:
        try:
            unitid = int(unitid_str)
        except (ValueError, TypeError):
            continue

        college = College.objects.filter(unitid=unitid).first()
        if not college or college.image_url:
            if college and college.image_url:
                result[str(unitid)] = college.image_url
            continue

        url = fetch_wikipedia_image(college.name, college.city or "", college.state or "")
        if not url and college.website_url:
            url = fetch_website_image(college.website_url)

        if url:
            college.image_url = url
            college.save(update_fields=["image_url"])
            result[str(unitid)] = url

    return JsonResponse({"images": result})
