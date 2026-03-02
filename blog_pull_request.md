## Summary

- Convert the existing `blog` app from a stub into a simple database-backed blog.
- Add a `Post` model and admin integration so new posts can be created via the Django admin UI.
- Implement list/detail views and templates for blog posts, plus a site-wide navigation link to the blog.
- Update configuration to include the deployed `site_url` in trusted domains / `CSRF_TRUSTED_ORIGINS`.
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

- Implemented `PostListView` and

### Configuration and tooling

- Added `site_url` to `CSRF_TRUSTED_ORIGINS` / trusted domains in `config/settings.py` to support the deployed site URL.
- Removed `db.sqlite3` from `.gitignore` and `.dockerignore` so the SQLite database can be included where appropriate (for example in Docker builds or when sharing a pre-populated dev database).