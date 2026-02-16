#!/usr/bin/env python3
"""Export quiz data to JSON for static site. Run from project root: python3 scripts/export_quiz_json.py"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from career_quiz.quiz_data import (
    MAJORS, CAREER_CATEGORIES, CAREERS_BY_MAJOR, CAREER_LEARN_MORE, CAREER_LEARN_MORE_DEFAULT,
    INTEREST_QUESTIONS, BIG_FIVE_QUESTIONS, PERSONALITY_QUESTIONS, JOB_MATCH_QUESTIONS,
)

SHORT_QUESTIONS = INTEREST_QUESTIONS + BIG_FIVE_QUESTIONS
QUESTIONS = INTEREST_QUESTIONS + BIG_FIVE_QUESTIONS + PERSONALITY_QUESTIONS + JOB_MATCH_QUESTIONS

def to_json_questions(qlist):
    return [
        {
            'id': q['id'],
            'text': q['text'],
            'options': [{'key': k, 'label': l, 'categories': c} for k, l, c in q['options']]
        }
        for q in qlist
    ]

def to_json_majors():
    return [{'key': k, 'label': l, 'desc': d, 'keywords': kw} for k, l, d, kw in MAJORS]

def to_json_categories():
    return [{'key': k, 'name': n, 'desc': d} for k, n, d in CAREER_CATEGORIES]

def to_json_careers():
    return [
        {'title': t, 'description': d, 'category': c, 'majors': m}
        for t, d, c, m in CAREERS_BY_MAJOR
    ]

data = {
    'majors': to_json_majors(),
    'categories': to_json_categories(),
    'careers': to_json_careers(),
    'careerLearnMore': CAREER_LEARN_MORE,
    'careerLearnMoreDefault': CAREER_LEARN_MORE_DEFAULT,
    'shortQuestions': to_json_questions(SHORT_QUESTIONS),
    'fullQuestions': to_json_questions(QUESTIONS),
}
print(json.dumps(data, indent=2))
