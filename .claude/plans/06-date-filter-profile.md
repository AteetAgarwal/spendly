# Implementation Plan: Date Filter for Profile Page

## Objective
Introduce date filtering to the profile page to allow users to view their spending stats and transactions within a specific date range.

## Step-by-Step Execution

### 1. Update Database Queries (`database/queries.py`)
Modify the following functions to accept optional `start_date` and `end_date` parameters. 
- **`get_summary_stats(user_id, start_date=None, end_date=None)`**:
    - Update SQL to include `AND date BETWEEN ? AND ?` if dates are provided.
- **`get_recent_transactions(user_id, limit=10, start_date=None, end_date=None)`**:
    - Update SQL to filter by date range before ordering and limiting.
- **`get_category_breakdown(user_id, start_date=None, end_date=None)`**:
    - Update SQL to filter by date range before grouping by category.

### 2. Update Profile Route (`app.py`)
Modify the `profile()` route to extract query parameters and pass them to the query functions.
- Get `start_date` and `end_date` using `request.args.get()`.
- Pass these values into `get_summary_stats`, `get_recent_transactions`, and `get_category_breakdown`.
- Pass the current filter values back to the template so the input fields can persist their values after submission.

### 3. Update Profile Template (`templates/profile.html`)
Add the UI for date filtering.
- Insert a `<form method="GET" action="{{ url_for('profile') }}">` above the stats grid.
- Add two `<input type="date">` fields for `start_date` and `end_date`.
- Add a "Filter" submit button.
- Add a "Clear" button (which can be a simple link to `/profile` or a reset button).
- Ensure the inputs have `value="{{ start_date }}"` and `value="{{ end_date }}"`.

### 4. Verification & Testing
- **Functional Test**:
    - Verify that selecting a range (e.g., 2026-10-01 to 2026-10-10) updates total spent and transactions list.
    - Verify that "Clear Filter" resets the view.
- **Edge Case Test**:
    - Test with one date provided and the other empty.
    - Test with `start_date` after `end_date` (should return no results, not crash).
    - Test with dates outside the range of any existing data.

## Critical Files
- `database/queries.py`
- `app.py`
- `templates/profile.html`

## Constraints
- Maintain the use of parameterized queries.
- Ensure CSS remains consistent with the existing profile styles.
