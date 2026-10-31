---
# Spec: Add Expense

## Overview
This feature allows logged-in users to add new expenses to their tracker. It provides a form to input the amount, category, date, and an optional description, ensuring that expenses are correctly linked to the authenticated user.

## Depends on
- 03-login-and-logout (User must be authenticated)
- 01-database-setup (Database schema for expenses must exist)

## Routes
- `GET /expenses/add` — Renders the expense addition form — logged-in
- `POST /expenses/add` — Processes the form submission and saves the expense to the database — logged-in

## Database changes
No database changes. The `expenses` table already exists with the necessary columns (`user_id`, `amount`, `category`, `date`, `description`).

## Templates
- **Create:** `templates/add_expense.html` — A form for inputting expense details.
- **Modify:** `templates/base.html` — Add a link to the "Add Expense" page in the navigation.

## Files to change
- `app.py` — Implement the `GET` and `POST` handlers for `/expenses/add`.
- `database/db.py` — Add a helper function `create_expense()` to handle the database insertion.
- `templates/base.html` — Update navigation.

## Files to create
- `templates/add_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Ensure the `user_id` is retrieved from the session and not provided by the user in the form.
- Validate that `amount`, `category`, and `date` are provided before saving.

## Definition of done
- [ ] Logged-in user can navigate to `/expenses/add`.
- [ ] Unauthenticated user is redirected to the login page when accessing `/expenses/add`.
- [ ] User can submit a valid expense via the form.
- [ ] Valid submissions result in a redirect back to the profile page with a success flash message.
- [ ] Missing required fields trigger a validation error flash message and re-render the form.
- [ ] Newly added expenses appear correctly in the profile page transaction list.
---
