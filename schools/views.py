import json
from django.conf import settings
from django.shortcuts import render
from .schools_data import (
    get_schools,
    get_states,
    get_cost_brackets,
    get_all_major_labels,
)


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

    return render(request, 'schools/home.html', {
        'schools_json': schools_json,
        'schools_count': len(schools),
        'states': states,
        'cost_brackets': cost_brackets,
        'majors': majors,
        'preselect_major': preselect_major,
    })
