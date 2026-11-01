# Plan for Feature: Edit Expense

## Step 1: Database helpers in `database/db.py`
- Implement helper `get_expense_by_id(expense_id: int)` that fetches an expense from the database by its ID 
  - Returns the expense record or None
- Implement helper `update_expense(expense_id: int, amount: float, category: str, date: str, description: str)` that updates an expense record
  - Use parameterized SQL queries
  - Ensure foreign keys enabled in DB connection


## Step 2: Routes in `app.py`
- Add route `GET /expenses/<id>/edit`
  - Check user is logged in
  - Fetch expense by id using DB helper
  - Validate current user is the owner of the expense
  - Render `edit_expense.html` with expense details to pre-fill form
  - Abort 403 if user not owner, 404 if expense not found

- Add route `POST /expenses/<id>/edit`
  - Check user is logged in
  - Validate form inputs (amount, category, date mandatory)
  - Fetch expense and validate ownership
  - Update expense using DB helper
  - On validation errors, re-render the form with errors and submitted data
  - Redirect to profile or expense list on success


## Step 3: Template `templates/edit_expense.html`
- Extend `base.html`
- Render form fields pre-populated with existing expense data
- Include fields for amount, category, date, description
- Show validation errors if any
- Form submits to POST `/expenses/<id>/edit`


## Step 4: Testing
- Write tests for GET /expenses/<id>/edit
  - User can load form with correct pre-filled data
  - Unauthorized users get 403 or redirect
  - Non-existent expense IDs return 404

- Write tests for POST /expenses/<id>/edit
  - Valid data updates expense successfully
  - Invalid data shows errors
  - Unauthorized user blocked


## Step 5: Validation and security
- Validate that logged in user owns the expense before showing or allowing update
- Use parameterized queries to prevent SQL injection


---

This plan covers all points in the spec and follows project conventions.

Co-Authored-By: Claude Code <noreply@anthropic.com>
