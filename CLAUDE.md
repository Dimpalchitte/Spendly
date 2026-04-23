# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (use a virtual environment)
pip install -r requirements.txt

# Run the dev server (http://localhost:5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_foo.py

# Run a specific test
pytest tests/test_foo.py::test_function_name
```

## Architecture

**Spendly** is a Flask + SQLite expense tracker app (currency: Indian Rupees ₹). It uses server-side rendering via Jinja2 templates — no frontend build step.

### Key files

| File | Purpose |
|---|---|
| `app.py` | Flask app, all route definitions |
| `database/db.py` | SQLite helpers: `get_db()`, `init_db()`, `seed_db()` |
| `templates/base.html` | Shared Jinja2 layout (navbar, footer, CSS/JS links) |
| `static/css/style.css` | Single stylesheet with full design system (CSS variables for dark/light theme) |
| `static/js/main.js` | Vanilla JS (currently only the YouTube modal on the landing page) |

### Routing structure

Routes are all defined in `app.py`. The app is being built incrementally in numbered steps:

- **Step 1** — `database/db.py` (SQLite setup)
- **Step 2** — register/login templates (`/register`, `/login`)
- **Step 3** — logout (`/logout`)
- **Step 4** — profile (`/profile`)
- **Steps 7–9** — CRUD for expenses (`/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`)

Placeholder routes currently return plain strings; they will be replaced with full implementations as each step is completed.

### Database

SQLite file (`expense_tracker.db`) is gitignored and not committed. `database/db.py` must expose:
- `get_db()` — connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `init_db()` — `CREATE TABLE IF NOT EXISTS` for all tables
- `seed_db()` — sample data for local development

### Templates

All pages extend `templates/base.html` using `{% block content %}`. The base layout includes the navbar (Sign in / Get started links) and footer (Terms, Privacy links), plus the shared stylesheet and `main.js`.
