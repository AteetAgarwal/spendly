# Implementation Plan: Profile Page (Step 04)

## Goals
Implement the `/profile` route to allow authenticated users to view their account details (name and email).

## Step-by-Step Execution

### 1. Database Layer (`database/db.py`)
- Create a helper function `get_user_by_id(user_id)` to fetch user record from the `users` table.
- Ensure the query is parameterized to prevent SQL injection.

### 2. Route Implementation (`app.py`)
- Update the `/profile` route:
    - Check if `user_id` exists in the session.
    - If not, redirect to `url_for('login')` with a flash message.
    - If yes, call `get_user_by_id(user_id)`.
    - Render `profile.html` passing the user object.

### 3. Frontend Development
- **CSS:** Create `static/css/profile.css` for profile-specific styling. Use CSS variables for colors to maintain consistency.
- **Template:** Create `templates/profile.html`:
    - Extend `base.html`.
    - Link the new `profile.css`.
    - Display the user's name and email in a clean, centered profile card.

### 4. Verification (Definition of Done)
- [ ] **Unauthorized Access:** Try accessing `/profile` in an incognito window $\rightarrow$ should redirect to `/login`.
- [ ] **Authorized Access:** Login $\rightarrow$ access `/profile` $\rightarrow$ verify name and email are displayed correctly.
- [ ] **Styling:** Verify the page looks consistent with the landing/login pages and is responsive.
- [ ] **DB Integration:** Verify the data displayed matches the data in `spendly.db` for that user.

## Files Modified/Created
- `database/db.py` (Modify)
- `app.py` (Modify)
- `templates/profile.html` (Create)
- `static/css/profile.css` (Create)
