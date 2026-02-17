import json
import os
import ssl
import urllib.request
import urllib.error

import certifi

from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .resume_data import RESUME_TEMPLATES, RESUME_TIPS


def resume_home_view(request):
    majors = [
        {'key': k, 'label': v['label'], 'icon': v['icon'], 'focus': v['focus']}
        for k, v in RESUME_TEMPLATES.items()
    ]
    return render(request, 'resume/home.html', {
        'majors': majors,
    })


def resume_templates_view(request):
    majors = [
        {'key': k, 'label': v['label'], 'icon': v['icon'], 'focus': v['focus']}
        for k, v in RESUME_TEMPLATES.items()
    ]
    return render(request, 'resume/templates.html', {
        'majors': majors,
    })


def resume_template_detail_view(request, major_key):
    template_data = RESUME_TEMPLATES.get(major_key)
    if not template_data:
        raise Http404("Resume template not found for this major.")
    return render(request, 'resume/template_detail.html', {
        'major_key': major_key,
        'template': template_data,
    })


def resume_tips_view(request):
    return render(request, 'resume/tips.html', {
        'tips': RESUME_TIPS,
    })


def resume_ai_tools_view(request):
    return render(request, 'resume/ai_tools.html')


# --------------- AI API endpoints ---------------

GEMINI_MODEL = 'gemini-2.0-flash'
GEMINI_URL = (
    'https://generativelanguage.googleapis.com/v1beta/models/'
    + GEMINI_MODEL + ':generateContent'
)


def _get_gemini_key():
    return os.environ.get('GEMINI_API_KEY', '')


def _call_gemini(prompt):
    """Call the Gemini API and return the generated text."""
    api_key = _get_gemini_key()
    if not api_key or api_key == 'your-gemini-api-key-here':
        return None, 'Gemini API key not configured. Add GEMINI_API_KEY to your .env file.'

    url = GEMINI_URL + '?key=' + api_key
    payload = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 1024,
        },
    }).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            text = data['candidates'][0]['content']['parts'][0]['text']
            return text, None
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        try:
            err_data = json.loads(body)
            msg = err_data.get('error', {}).get('message', str(e))
        except Exception:
            msg = str(e)
        return None, msg
    except Exception as e:
        return None, str(e)


def ai_status_view(request):
    """Check if the AI backend is available."""
    key = _get_gemini_key()
    configured = bool(key and key != 'your-gemini-api-key-here')
    return JsonResponse({'available': configured})


@csrf_exempt
@require_POST
def ai_enhance_bullet_view(request):
    """Enhance a resume bullet point."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    bullet = body.get('bullet', '').strip()
    major = body.get('major', 'college')
    if not bullet:
        return JsonResponse({'error': 'Please provide a bullet point.'}, status=400)

    prompt = (
        f'You are an expert resume writer for {major} students. '
        'Rewrite this resume bullet point to be more impactful. Use a strong action verb, '
        'add specificity, and quantify results where possible. Keep it to ONE concise bullet point (one sentence). '
        'Return ONLY the improved bullet point, no explanation or extra text.\n\n'
        f'Original: {bullet}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip().lstrip('-•* ')})


@csrf_exempt
@require_POST
def ai_generate_summary_view(request):
    """Generate a professional resume summary."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    major = body.get('major', 'your field')
    role = body.get('role', '')
    level = body.get('level', 'entry-level')
    skills = body.get('skills', '')

    prompt = (
        f'You are an expert resume writer. Write a professional resume summary (2-3 sentences) for a '
        f'{level} {major} student'
        + (f' targeting a {role} role' if role else '') + '. '
        + (f'Key skills: {skills}. ' if skills else '')
        + 'Make it confident, specific, and tailored. Return ONLY the summary paragraph, no labels or explanation.'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})


@csrf_exempt
@require_POST
def ai_suggest_skills_view(request):
    """Suggest skills based on major and target role."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    major = body.get('major', 'your field')
    role = body.get('role', '')

    prompt = (
        f'You are a career advisor for {major} students. '
        + (f'The student is targeting a {role} role. ' if role else '')
        + 'List 12-15 relevant skills they should include on their resume, separated into '
        '"Technical Skills" and "Soft Skills" categories. Format as two short lists. '
        'Return ONLY the skill lists, no extra explanation. Use bullet points.'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})


@csrf_exempt
@require_POST
def ai_tailor_resume_view(request):
    """Tailor resume content to a job description."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    resume = body.get('resume', '').strip()
    job = body.get('job', '').strip()
    if not resume or not job:
        return JsonResponse({'error': 'Please provide both resume content and a job description.'}, status=400)

    prompt = (
        'You are an expert resume consultant. A student has the following resume content and wants to tailor it '
        'to a specific job posting. Rewrite their resume content to better match the job description by:\n'
        '1. Incorporating relevant keywords from the job posting\n'
        '2. Reordering bullet points to highlight the most relevant experience\n'
        '3. Strengthening bullet points with action verbs and quantified results\n'
        '4. Keeping the same overall structure\n\n'
        'Return ONLY the improved resume content, formatted with clear section headers and bullet points. '
        'Do not include any explanation or commentary.\n\n'
        f'--- RESUME CONTENT ---\n{resume}\n\n'
        f'--- JOB DESCRIPTION ---\n{job}'
    )
    text, err = _call_gemini(prompt)
    if err:
        return JsonResponse({'error': err}, status=502)
    return JsonResponse({'result': text.strip()})
