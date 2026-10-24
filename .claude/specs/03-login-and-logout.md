# Spec: Login and Logout

## Overview
This feature implements the complete authentication lifecycle for Spendly. It upgrades the existing stub routes to allow users to securely sign into their accounts and sign out. This enables the application to track the current user's identity via the session, which is a prerequisite for all personalized expense tracking features.

## Depends on
- 02-registration

## Routes
- `GET /login` — render login form — public
- `POST /login` — validate credentials, establish session, redirect to profile — public
- `GET /logout` — clear session, redirect to landing — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/login.html` — update form to use `method="POST"`, `url_for('login')`, and add a block for flash error messages.
- **Modify:** `templates/base.html` — update the navigation bar to conditionally show "Sign in" and "Get started" vs. "Logout" and "Profile" based on the user's session status.

## Files to change
- `app.py` — implement `POST /login` and `GET /logout` route handlers.
- `templates/login.html` — wire up the login form.
- `templates/base.html` — implement conditional navigation.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified using `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `session` for tracking the logged-in user (e.g., `session['user_id'] = user['id']`)
- Use `flash()` for authentication errors (e.g., "Invalid email or password")
- Ensure `app.secret_key` is configured for session and flash support

## Definition of done
- [ ] `GET /login` renders the login form correctly.
- [ ] Submitting valid credentials creates a session and redirects to `/profile`.
- [ ] Submitting invalid credentials (wrong password or non-existent email) renders the login page with an error message.
- [ ] `GET /logout` clears the session and redirects to the landing page.
- [ ] Navigation bar updates dynamically: showing "Logout" and "Profile" when signed in, and "Sign in" / "Get started" when signed out.
- [ ] Attempting to access `/logout` while not signed in redirects to the landing page or login page gracefully.
