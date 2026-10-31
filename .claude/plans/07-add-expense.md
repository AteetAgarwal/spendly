# Plan: Implement Add Expense Feature

## Context
The "Add Expense" feature allows authenticated users to record their daily spending. This is a core functional requirement of the Spendly app, enabling users to populate their transaction history which is then visualized on the profile page. This implementation replaces the current stub route `/expenses/add`.

## Recommended Approach

### 1. Database Layer (`database/db.py`)
Create a helper function `create_expense` to handle data insertion.
- **Function**: `create_expense(user_id, amount, category, date, description)`
- **Implementation**: Use `get_db()` and a parameterized `INSERT INTO expenses` query.
- **File**: `database/db.py`

### 2. Route Implementation (`app.py`)
Update the `/expenses/add` route to handle the form lifecycle.
- **Authentication**: Implement a check for `session.get('user_id')` at the start of the route. Redirect to `login` if missing.
- **GET Logic**: Render the `add_expense.html` template.
- **POST Logic**: 
    - Extract `amount`, `category`, `date`, and `description` from `request.form`.
    - Validate required fields (`amount`, `category`, `date`). Flash error and re-render if invalid.
    - Call `create_expense` using the `user_id` from the session.
    - Flash success message and redirect to `profile`.
- **File**: `app.py`

### 3. UI/Templates
- **New Page**: Create `templates/add_expense.html` extending `base.html`. It will contain a form with inputs for amount (number), category (select), date (date), and description (textarea).
- **Navigation**: Add a link to "Add Expense" inside the authenticated user block in `templates/base.html`.
- **Files**: `templates/add_expense.html`, `templates/base.html`

## Critical Files
- `database/db.py`
- `app.py`
- `templates/base.html`
- `templates/add_expense.html`

## Verification Plan
1. **Auth Check**: Attempt to access `/expenses/add` while logged out $\rightarrow$ verify redirect to `/login`.
2. **Form Access**: Log in and navigate to `/expenses/add` $\rightarrow$ verify page renders correctly.
3. **Validation Test**: Submit the form with missing required fields $\rightarrow$ verify error flash message and form persistence.
4. **Success Path**: Submit a valid expense $\rightarrow$ verify success flash message and redirect to `/profile`.
5. **Data Persistence**: Verify the new expense appears in the transaction list on the profile page.
