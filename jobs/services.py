"""
Job market sweep: pull live listings from LinkedIn, Indeed, Glassdoor,
ZipRecruiter, Handshake, and other boards via the JSearch API (RapidAPI).

Falls back to curated career-data results with direct board search links
when the API key is not configured.

Configuration:
  Set RAPIDAPI_KEY in your .env file.
  Free tier: 200 requests/month — cached aggressively to stay within limits.
"""
import logging
import os
import re
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
from urllib.error import URLError

from career_quiz.quiz_data import CAREERS_BY_MAJOR, CAREER_LEARN_MORE

logger = logging.getLogger(__name__)

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', '')
JSEARCH_HOST = 'jsearch.p.rapidapi.com'
JSEARCH_URL = f'https://{JSEARCH_HOST}/search'

# Maps each major to search terms that produce relevant results on job boards
MAJOR_SEARCH_TERMS = {
    'business': 'business analyst OR finance OR marketing OR management',
    'computer_science': 'software engineer OR developer OR data scientist OR IT',
    'engineering': 'mechanical engineer OR civil engineer OR electrical engineer',
    'health_sciences': 'registered nurse OR healthcare OR public health',
    'humanities': 'writer OR editor OR communications OR liberal arts',
    'social_sciences': 'research analyst OR psychology OR sociology OR policy',
    'arts_design': 'graphic designer OR UX designer OR creative',
    'education': 'teacher OR educator OR curriculum',
    'environmental': 'environmental scientist OR sustainability',
    'communications': 'marketing OR journalism OR media OR PR',
    'law': 'paralegal OR legal assistant OR compliance',
    'agriculture': 'agriculture OR forestry OR conservation',
    'hospitality': 'hotel manager OR restaurant OR hospitality',
    'real_estate': 'real estate agent OR property manager OR appraiser',
    'sports_recreation': 'fitness OR sports management OR recreation',
    'trades_construction': 'construction manager OR electrician OR trades',
    'cosmetology': 'cosmetologist OR esthetician OR salon',
    'allied_health': 'medical assistant OR dental hygienist OR sonographer',
    'culinary': 'chef OR cook OR pastry OR culinary',
    'aviation_transportation': 'aircraft mechanic OR diesel technician OR CDL',
    'fire_emergency': 'firefighter OR EMT OR paramedic',
}

JSEARCH_EMPLOYMENT_TYPES = {
    'full_time': 'FULLTIME',
    'part_time': 'PARTTIME',
    'contract': 'CONTRACTOR',
    'internship': 'INTERN',
}

SOURCE_DISPLAY_NAMES = {
    'linkedin.com': 'LinkedIn',
    'indeed.com': 'Indeed',
    'glassdoor.com': 'Glassdoor',
    'ziprecruiter.com': 'ZipRecruiter',
    'dice.com': 'Dice',
    'monster.com': 'Monster',
    'simplyhired.com': 'SimplyHired',
    'careerbuilder.com': 'CareerBuilder',
    'handshake.com': 'Handshake',
    'joinhandshake.com': 'Handshake',
    'snagajob.com': 'Snagajob',
    'wellfound.com': 'Wellfound',
    'lever.co': 'Lever',
    'greenhouse.io': 'Greenhouse',
    'workday.com': 'Workday',
    'myworkdayjobs.com': 'Workday',
}


def _normalize_source(publisher_name, apply_link=''):
    """Turn a raw publisher name or apply URL into a clean display name."""
    if publisher_name:
        low = publisher_name.lower().strip()
        for domain, display in SOURCE_DISPLAY_NAMES.items():
            if domain in low:
                return display
        if low in ('linkedin', 'indeed', 'glassdoor', 'ziprecruiter',
                   'dice', 'monster', 'handshake'):
            return low.capitalize()
        return publisher_name.strip()
    if apply_link:
        low = apply_link.lower()
        for domain, display in SOURCE_DISPLAY_NAMES.items():
            if domain in low:
                return display
    return 'Job board'


def _strip_html(text):
    """Remove HTML tags and normalize whitespace for safe display."""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _format_salary(min_val, max_val, period=''):
    """Build a human-readable salary string."""
    def fmt(n):
        n = int(n)
        if n >= 1000:
            return f'${n:,}'
        return f'${n}'

    if min_val and max_val:
        label = f'{fmt(min_val)} \u2013 {fmt(max_val)}'
    elif min_val:
        label = f'From {fmt(min_val)}'
    elif max_val:
        label = f'Up to {fmt(max_val)}'
    else:
        return ''
    if period and period.upper() not in ('YEAR', 'YEARLY'):
        label += f' / {period.lower()}'
    return label


def _fetch_jsearch(query, job_type='', remote_only=False, location='',
                   num_pages=1, page=1):
    """
    Hit the JSearch API (RapidAPI) and return a parsed list.
    JSearch aggregates from LinkedIn, Indeed, Glassdoor, ZipRecruiter, etc.
    """
    params = {
        'query': query,
        'page': str(page),
        'num_pages': str(num_pages),
        'country': 'us',
        'date_posted': 'month',
    }
    if job_type and job_type in JSEARCH_EMPLOYMENT_TYPES:
        params['employment_types'] = JSEARCH_EMPLOYMENT_TYPES[job_type]
    if remote_only:
        params['remote_jobs_only'] = 'true'
    if location:
        params['query'] = f'{query} in {location}'

    url = f'{JSEARCH_URL}?{urlencode(params)}'
    req = Request(url, headers={
        'x-rapidapi-host': JSEARCH_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY,
        'User-Agent': 'ExploringU/1.0',
    })

    try:
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        logger.warning('JSearch API error: %s', exc)
        return None

    if data.get('status') != 'OK':
        logger.warning('JSearch non-OK status: %s', data.get('status'))
        return None

    results = []
    for item in data.get('data', []):
        min_sal = item.get('job_min_salary')
        max_sal = item.get('job_max_salary')
        sal_period = item.get('job_salary_period', '')
        salary_display = _format_salary(min_sal, max_sal, sal_period)

        emp_type = (item.get('job_employment_type') or '').upper()
        type_key = {
            'FULLTIME': 'full_time',
            'PARTTIME': 'part_time',
            'CONTRACTOR': 'contract',
            'INTERN': 'internship',
        }.get(emp_type, 'full_time')

        city = item.get('job_city') or ''
        state = item.get('job_state') or ''
        loc_parts = [p for p in (city, state) if p]
        if item.get('job_is_remote'):
            loc_parts.append('Remote')
        location_display = ', '.join(loc_parts)

        publisher = item.get('job_publisher') or ''
        apply_link = item.get('job_apply_link') or ''
        source = _normalize_source(publisher, apply_link)

        desc_raw = _strip_html(item.get('job_description') or '')
        if len(desc_raw) > 520:
            desc_raw = desc_raw[:517] + '...'

        results.append({
            'title': item.get('job_title') or '',
            'company': item.get('employer_name') or '',
            'company_logo': item.get('employer_logo') or '',
            'location': location_display,
            'salary': salary_display,
            'salary_sort': min_sal or max_sal or 0,
            'description': desc_raw,
            'url': apply_link,
            'created': item.get('job_posted_at_datetime_utc') or '',
            'job_type': type_key,
            'source': source,
            'is_remote': bool(item.get('job_is_remote')),
        })

    return results


def _build_curated_results(major_key, job_type=''):
    """
    Fallback when no API key is set: use quiz career data and link out
    to real search results on LinkedIn, Indeed, Glassdoor, and Handshake.
    """
    results = []
    seen = set()
    for title, desc, category, majors in CAREERS_BY_MAJOR:
        if major_key and major_key not in majors:
            continue
        if title in seen:
            continue
        seen.add(title)

        q = quote_plus(title)
        learn_more = CAREER_LEARN_MORE.get(title, '')
        short_desc = learn_more[:280] + '...' if len(learn_more) > 280 else learn_more
        if not short_desc:
            short_desc = desc

        boards = [
            ('LinkedIn', f'https://www.linkedin.com/jobs/search/?keywords={q}&location=United%20States'),
            ('Indeed', f'https://www.indeed.com/jobs?q={q}&l=United+States'),
            ('Glassdoor', f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={q}'),
            ('Handshake', f'https://joinhandshake.com/search/jobs?search={q}'),
        ]

        for source_name, board_url in boards:
            results.append({
                'title': title,
                'company': 'Search on ' + source_name,
                'company_logo': '',
                'location': 'United States / Remote',
                'salary': '',
                'salary_sort': 0,
                'description': short_desc,
                'url': board_url,
                'created': '',
                'job_type': job_type or 'full_time',
                'source': source_name,
                'is_remote': False,
                'category': category,
            })

    return results


def fetch_jobs(major_key='', job_type='', sort='relevance', salary_min='',
               location='', remote_only=False):
    """
    Main entry point. Sweeps the job market via JSearch (LinkedIn, Indeed,
    Glassdoor, ZipRecruiter, etc.). Falls back to curated career data with
    direct board search links when RAPIDAPI_KEY is not configured.
    """
    query = MAJOR_SEARCH_TERMS.get(major_key, 'entry level jobs')
    if remote_only:
        query += ' remote'

    results = None
    if RAPIDAPI_KEY:
        results = _fetch_jsearch(
            query=query, job_type=job_type,
            remote_only=remote_only, location=location,
        )

    if results is None:
        results = _build_curated_results(major_key=major_key, job_type=job_type)

    if salary_min:
        try:
            floor = int(salary_min)
            results = [r for r in results if r.get('salary_sort', 0) >= floor
                       or r.get('salary_sort', 0) == 0]
        except (ValueError, TypeError):
            pass

    if sort == 'salary_desc':
        results.sort(key=lambda x: x.get('salary_sort', 0), reverse=True)
    elif sort == 'salary_asc':
        results.sort(key=lambda x: x.get('salary_sort', 0))
    elif sort == 'date_desc':
        results.sort(key=lambda x: x.get('created', ''), reverse=True)

    return results
