#!/usr/bin/env python3
"""Export resume_data.py into a JSON file for the static site."""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from resume.resume_data import RESUME_TEMPLATES, RESUME_TIPS

output = {
    'templates': RESUME_TEMPLATES,
    'tips': RESUME_TIPS,
}

out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'js', 'resume-data.json')
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f'Wrote {out_path}')
