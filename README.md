# FutureFit

**Project7** is a Django web app that helps students get from campus to career. The name comes from seven moves that actually help: know your resume gaps, discover careers that fit your personality, tailor your story, beat ATS, explore roles by type, get AI feedback, and take the next step.

## Features

- **Resume Gap Analysis** — Paste your resume and a job description (or a job type like "Database Administrator") to see gaps and get AI tailoring and ATS tips.
- **Career Discovery Quiz** — Take a short quiz by major or explore majors and careers; get personalized job suggestions.

## Setup

### 1. Clone or download the project

```bash
cd Project7
```

### 2. Create and activate a virtual environment

Already created:

```bash
# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

If you need to recreate it:

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project structure

```
Project7/
├── config/             # Django project settings
├── resume_analysis/     # Gap analysis app (views, forms, analysis logic)
├── career_quiz/        # Career quiz app (questions, scoring, results)
├── templates/           # Base and app templates
├── static/css/         # Styles
├── manage.py
├── requirements.txt
└── README.md
```

## Pushing to GitHub

1. Create a new repository on GitHub (do not initialize with a README if you already have one).
2. In the project folder:

```bash
git init
git add .
git commit -m "Initial commit: Project7 Django app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

The included `.gitignore` excludes `venv/`, `db.sqlite3`, `__pycache__/`, and other files you typically don’t want in the repo.



## License

MIT (or your choice).
