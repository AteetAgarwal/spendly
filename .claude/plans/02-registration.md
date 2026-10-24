# Plan: Registration Implementation

## Context
This plan implements the user registration flow for Spendly. The goal is to transform the existing stub `/register` route into a functional registration system that allows new users to create accounts. This includes server-side validation, secure password hashing, and duplicate email prevention.

## Recommended Approach

### 1. Database Layer (`database/db.py`)
Add a helper function to handle user creation:
- `create_user(name, email, password)`:
    - Hash the password using `werkzeug.security.generate_password_hash`.
    - Insert the user into the `users` table using a parameterized query.
    - Return the new user's ID.
    - Rely on the `UNIQUE` constraint on the `email` column to handle duplicates (catch `sqlite3.IntegrityError` in the routing layer).

### 2. Routing Layer (`app.py`)
Upgrade the `register()` route to handle both `GET` and `POST` methods:
- **GET**: Render the `register.html` template.
- **POST**:
    1. **Input Validation**: Check that all fields (`name`, `email`, `password`, `confirm_password`) are present and non-empty.
    2. **Password Matching**: Verify that `password == confirm_password`.
    3. **Persistence**: Call `create_user()`.
    4. **Error Handling**: 
       - Catch `sqlite3.IntegrityError` to handle duplicate email registration.
       - On any validation or integrity error, use `flash()` to send an error message and re-render the registration form.
    5. **Success**: Use `flash()` to send a success message and `redirect(url_for('login'))`.
- **Configuration**: Ensure `app.secret_key` is defined to enable Flask's flashing system.

### 3. Template Layer (`templates/register.html`)
Modify the registration template:
- **Form Config**: Ensure `<form method="post" action="{{ url_for('register') }}">` is used.
- **Input Names**: Add `name` attributes to all inputs: `name`, `email`, `password`, and `confirm_password`.
- **Messaging**: Ensure the template can display flashed messages (e.g., via a loop over `get_flashed_messages()`).

## Critical Files
- `database/db.py`
- `app.py`
- `templates/register.html`

## Verification Plan
- **Happy Path**: Register a new user $\rightarrow$ Verify success flash message $\rightarrow$ Verify redirect to `/login` $\rightarrow$ Confirm record in `spendly.db`.
- **Password Mismatch**: Register with `password != confirm_password` $\rightarrow$ Verify error flash message $\rightarrow$ Confirm no record created in DB.
- **Duplicate Email**: Register with an email already in the system $\rightarrow$ Verify "Email already registered" flash message $\rightarrow$ Confirm no duplicate record created.
- **Empty Fields**: Submit form with missing fields $\rightarrow$ Verify validation error message.
- **Security Check**: Directly query `spendly.db` to ensure `password_hash` is a salted hash and not plain text.
