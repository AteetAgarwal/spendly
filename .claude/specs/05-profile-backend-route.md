# Spec: Backend Route for Profile Page

## Overview
This feature replaces the stubbed `/profile` route with a fully functional backend implementation. It will authenticate the user via session, retrieve their profile information from the database, and aggregate their spending data (total expenses and category-wise breakdown) to provide a meaningful summary on the profile page.

## Depends on
- 01-database-setup
- 03-login-and-logout

## Routes
- `GET /profile` — Fetches user data and expense aggregations, renders the profile page — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` — Replace hardcoded mock data with dynamic values passed from the backend.

## Files to change
- `app.py` — Implement the logic for the `/profile` route.
- `database/db.py` — Add helper functions to fetch user profile and aggregated expense data.
- `templates/profile.html` — Update to use Jinja2 variables for user and expense data.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- The route must check for `session.get("user_id")` and redirect to `/login` if the user is not authenticated.

## Definition of done
- [ ] Logged-out users are redirected to `/login` when visiting `/profile`.
- [ ] Logged-in users see their actual name and email on the profile page.
- [ ] The total spending amount is correctly calculated and displayed from the `expenses` table for the logged-in user.
- [ ] Category-wise spending totals are correctly calculated and displayed.
- [ ] The page renders correctly without errors when a user has no expenses.
