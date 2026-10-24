# Plan: Login and Logout Implementation

## Context
This change implements the complete authentication lifecycle for Spendly. It transforms the stub login and logout routes into a functional system that uses Flask sessions to track user identity. This is critical for subsequent features (like the Profile and Expense tracking) that require an authenticated user context.

## Recommended Approach

### 1. Routing Layer (`app.py`)
Modify the authentication routes to manage the user session:

- **`POST /login`**:
    1. Extract `email` and `password` from the form.
    2. Validate that both fields are provided.
    3. Use `database.db.get_user_by_email(email)` to retrieve the user record.
    4. Use `werkzeug.security.check_password_hash(user['password_hash'], password)` to verify the password.
    5. If verified, store the user's ID in the session: `session['user_id'] = user['id']`.
    6. Redirect to `url_for('landing')`.
    7. On failure (invalid email or password), use `flash()` to send a generic error message and re-render the login form.

- **`GET /logout`**:
    1. Clear the user session using `session.clear()`.
    2. Redirect the user to `url_for('landing')`.

- **Auth Guard**:
    - Add checks to `/login` and `/register` to redirect already authenticated users to `url_for('profile')`.

### 2. Template Layer

- **`templates/login.html`**:
    - Set `<form method="POST" action="{{ url_for('login') }}">`.
    - Replace the existing error block with a flash message loop:
      ```html
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          {% for message in messages %}
            <div class="auth-error">{{ message }}</div>
          {% endfor %}
        {% endif %}
      {% endwith %}
      ```

- **`templates/base.html`**:
    - Implement conditional navigation in the `.nav-links` section:
      - **If `session.get('user_id')`**: Show links to `Profile` and `Logout`.
      - **Otherwise**: Show links to `Sign in` and `Get started`.

## Critical Files
- `app.py`
- `templates/login.html`
- `templates/base.html`

## Verification Plan
- **Happy Path**: Login with seeded user (`demo@spendly.com` / `demo123`) $\rightarrow$ Verify redirect to landing page and updated navbar.
- **Invalid Credentials**: Login with wrong password or non-existent email $\rightarrow$ Verify "Invalid email or password" flash message.
- **Logout Flow**: Click "Logout" while signed in $\rightarrow$ Verify redirect to landing page and navbar reverting to signed-out state.
- **Unauthorized Logout**: Navigate to `/logout` while signed out $\rightarrow$ Verify graceful redirect to landing page.
- **Session Persistence**: Login $\rightarrow$ Navigate to other pages $\rightarrow$ Verify that the user remains signed in.
- **Auth Guard**: While signed in, try to visit `/login` or `/register` $\rightarrow$ Verify redirection to `/profile`.
