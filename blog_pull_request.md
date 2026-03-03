## Summary

- Created the  `blog` app at `/resources/`
- Add a `Post` model and admin integration so new posts can be created via the Django admin UI.
- Implement list/detail views and templates for blog posts, plus a site-wide navigation link.
- Add static HTML copies in `docs/` for GitHub Pages deployment (resources list page and applying-to-college article).
- Update configuration to use a `site_url` environment variable if there is one
- Adjust `.gitignore` and `.dockerignore` so `db.sqlite3` can be included when needed (e.g., Docker builds or sharing a pre-populated dev database).


## Changes

### Data model and migrations

- Added a `Post` model in `blog/models.py` with:
  - `title`, `slug`, `excerpt`, `body`
  - `created_at`, `updated_at`
  - `published` flag
- Generated an initial migration (`blog/migrations/0001_initial.py`) to create the `blog_post` table.

### Admin

- Registered `Post` with the Django admin in `blog/admin.py`.
- Configured `PostAdmin` with:
  - `list_display = ("title", "published", "created_at")`
  - `list_filter = ("published", "created_at")`
  - `search_fields = ("title", "body")`
  - `prepopulated_fields = {"slug": ("title",)}` so slugs are auto-filled from titles.
- This allows blog posts to be added, edited, and searched through `/admin/`.

### Views and URLs

- Implemented `PostListView` and `PostDetailView` in `blog/views.py`.
- Updated `blog/urls.py` so `/resources/` shows the list and `/resources/<slug>/` shows individual posts.

### Static docs for GitHub Pages

- Created `docs/resources.html` — static copy of the Additional Resources list page with one article card linking to the applying-to-college article.
- Created `docs/resources-applying-to-college.html` — static copy of the full "A Step-by-Step Guide to Applying to College" article with all eight sections.
- Added the "Additional Resources" nav link to all 14 existing docs HTML files so the static site matches the Django site navigation.

### Configuration and tooling

- Added `site_url` to `CSRF_TRUSTED_ORIGINS` / trusted domains in `config/settings.py` to support the deployed site URL.
- Removed `db.sqlite3` from `.gitignore` and `.dockerignore` so the SQLite database can be included where appropriate (for example in Docker builds or when sharing a pre-populated dev database).