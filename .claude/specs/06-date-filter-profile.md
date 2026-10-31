# Spec: Date Filter for Profile Page

## Overview
Currently, the profile page displays a fixed set of recent transactions and overall summary statistics. To make the data more useful, this feature introduces date filtering, allowing users to view their spending habits and transactions over specific time periods (e.g., last 7 days, last 30 days, or a custom range). This is a critical step in evolving the profile page from a static summary to an interactive financial dashboard.

## Depends on
- `04-profile-page` (Profile page UI)
- `05-profile-backend-route` (Profile backend logic)

## Routes
No new routes. The existing `GET /profile` route will be modified to accept optional query parameters for filtering.
- `GET /profile?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` — filters stats and transactions by the given date range.

## Database changes
No database changes. The `expenses` table already contains a `date` column (TEXT) which can be used for filtering with standard SQLite date comparisons.

## Templates
- **Modify:** `templates/profile.html`
  - Add a filter section (form) above the stats grid.
  - Include inputs for "Start Date" and "End Date".
  - Add a "Clear Filter" button.
  - Ensure the form submits via GET to `/profile`.

## Files to change
- `app.py` — update the `profile()` route to handle `start_date` and `end_date` query parameters.
- `database/queries.py` — update `get_summary_stats`, `get_recent_transactions`, and `get_category_breakdown` to accept optional date filters.
- `templates/profile.html` — add the UI for date filtering.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with werkzeug.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- Use standard HTML `<input type="date">` for date selection.
- Handle empty or invalid date ranges gracefully by defaulting to all-time data.

## Definition of done
- [ ] Date filter form is visible on the profile page.
- [ ] Selecting a date range and submitting the form updates the "Total Spent", "Transactions", and "Top Category" stats correctly.
- [ ] The "Recent Transactions" table only shows entries within the selected date range.
- [ ] The "Spending Breakdown" updates to reflect the selected date range.
- [ ] Clicking "Clear Filter" returns the page to the all-time view.
- [ ] Invalid dates do not crash the application.
