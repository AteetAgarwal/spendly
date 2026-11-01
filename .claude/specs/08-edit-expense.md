---
# Spec: Edit Expense

## Overview
This feature allows logged-in users to edit their existing expenses. It provides a form pre-populated with the existing expense details, allowing users to update the amount, category, date, and description.

## Depends on
- 07-add-expense (for expense creation and corresponding routes)
- User authentication to identify the owner of the expense

## Routes
- `GET /expenses/<id>/edit` — Render the edit form for a specific expense — logged-in
- `POST /expenses/<id>/edit` — Process form submission and update the expense in the database — logged-in

## Database changes
No database changes. The existing `expenses` table supports updates.

## Templates
- **Create:** `templates/edit_expense.html` — A form similar to the add expense form but for editing.
- **Modify:** None

## Files to change
- `app.py` — Add the route handlers for GET and POST to edit an expense.
- `database/db.py` — Add helper functions for fetching a single expense by id and updating it.

## Files to create
- `templates/edit_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate that the expense belongs to the current user before allowing updates.

## Definition of done
- The edit expense form pre-populates existing expense data correctly.
- Users can successfully update expense amount, category, date, and description.
- Validation errors are displayed if required fields are missing.
- Unauthorized access attempts redirect or show an error.
- Database is updated accurately with the changes.
- Tests exist covering the GET and POST edit routes.

---
