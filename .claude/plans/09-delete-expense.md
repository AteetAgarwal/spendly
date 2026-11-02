# Plan: 09 Delete Expense Feature

## Summary

Implement deletion for expenses owned by the logged-in user. Provide a delete route, helper function, UI buttons, and tests.

## Steps

1. Add helper function `delete_expense(expense_id: int)` in `database/db.py`:
   - Use parameterized SQL DELETE query for expense row by its ID.
   - Return success status.

2. Add route `GET /expenses/<id>/delete` in `app.py`:
   - Verify user session.
   - Fetch expense by ID.
   - Return 404 if not found.
   - Check ownership, return 403 if not owner.
   - Call `delete_expense` helper.
   - Flash success message.
   - Redirect to `/profile`.

3. Modify `profile.html`:
   - Add a delete button/link per expense row.
   - Add JavaScript confirmation prompt for deletions.

4. Write tests for:
   - `delete_expense` helper coverage.
   - Delete route authorization and error cases (404 and 403).
   - Successful deletion redirects and flash message.

## Files to modify:
- `database/db.py`
- `app.py`
- `templates/profile.html`
- `tests/test_expense.py`

Co-Authored-By: Claude Code <noreply@anthropic.com>
