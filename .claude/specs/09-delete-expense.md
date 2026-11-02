---
# Spec: Delete Expense

## Overview
This feature adds the ability for a logged-in user to delete an expense from their account. It is part of the Spendly roadmap to allow full CRUD operations (Create, Read, Update, Delete) on expenses.

Users will have a delete option accessible from their profile page's transaction list. Upon deletion, the expense is removed from the database and the user is redirected back to their profile view with a success message.

## Depends on
- User authentication (login/logout)
- Expense listing in profile with correct ownership
- Expense CRUD helpers in database/db.py

## Routes
- `GET /expenses/<id>/delete` — performs deletion of the expense with given id — logged-in user access only

## Database changes
No database changes.

## Templates
- **Modify:** `profile.html` to add delete links/buttons for each expense entry

## Files to change
- `app.py` to add route for `/expenses/<id>/delete` and handle deletion logic
- `templates/profile.html` to show delete action per transaction
- `database/db.py` to add helper function `delete_expense(id)`

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

## Definition of done
- User can click delete on an expense in their profile transactions
- The expense is deleted from the database
- User is redirected back to `/profile` with a confirmation flash message
- Unauthorized users cannot delete expenses they don't own (403)
- Nonexistent expense IDs return 404
- The deletion route and helper function have tests
---
