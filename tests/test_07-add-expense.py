import pytest
from app import app as flask_app
from database.db import init_db, get_db
import sqlite3

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': ':memory:',  # Use in-memory DB for isolation
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })

    # We need to override get_db to use the in-memory connection across the app
    # since Flask app_context doesn't automatically propagate a sqlite3 connection
    # unless the app's get_db helper is designed for it.
    # Based on database/db.py, we can set get_db._test_conn.

    conn = sqlite3.connect(':memory:')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    get_db._test_conn = conn

    with flask_app.app_context():
        init_db()
        yield flask_app

    conn.close()
    get_db._test_conn = None

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in."""
    # Register a user first
    client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    })
    # Log in
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    return client

class TestAddExpense:

    # --- Authentication Guard ---

    def test_get_add_expense_unauthenticated_redirects_to_login(self, client):
        response = client.get('/expenses/add')
        assert response.status_code == 302
        assert '/login' in response.location, "Unauthenticated user should be redirected to login"

    def test_post_add_expense_unauthenticated_redirects_to_login(self, client):
        response = client.post('/expenses/add', data={'amount': '100', 'category': 'Food', 'date': '2023-01-01'})
        assert response.status_code == 302
        assert '/login' in response.location, "Unauthenticated user should be redirected to login"

    # --- Happy Path (GET) ---

    def test_get_add_expense_authenticated_renders_form(self, auth_client):
        response = auth_client.get('/expenses/add')
        assert response.status_code == 200
        assert b'amount' in response.data, "Expense form should contain amount field"
        assert b'category' in response.data, "Expense form should contain category field"
        assert b'date' in response.data, "Expense form should contain date field"

    # --- Happy Path (POST) ---

    def test_post_add_expense_valid_data_redirects_to_profile(self, auth_client):
        data = {
            'amount': '150.50',
            'category': 'Food',
            'date': '2023-10-31',
            'description': 'Dinner at restaurant'
        }
        response = auth_client.post('/expenses/add', data=data, follow_redirects=False)

        assert response.status_code == 302
        assert '/profile' in response.location, "Successful submission should redirect to profile"

        # Verify flash message (requires following redirect or checking session/app context)
        response = auth_client.get('/profile')
        assert b'Expense added successfully!' in response.data

    def test_post_add_expense_database_side_effect(self, auth_client, app):
        # First, find the user_id of the authenticated user
        # We can do this by getting the session or querying the DB
        # For this test, we know the email we used in auth_client
        with app.app_context():
            conn = get_db()
            user = conn.execute("SELECT id FROM users WHERE email = ?", ('test@example.com',)).fetchone()
            user_id = user['id']

        data = {
            'amount': '200.00',
            'category': 'Transport',
            'date': '2023-10-31',
            'description': 'Taxi ride'
        }
        auth_client.post('/expenses/add', data=data)

        with app.app_context():
            conn = get_db()
            expense = conn.execute(
                "SELECT * FROM expenses WHERE user_id = ? AND amount = ? AND category = ?",
                (user_id, 200.00, 'Transport')
            ).fetchone()

            assert expense is not None, "Expense should be saved in the database"
            assert expense['description'] == 'Taxi ride'
            assert expense['date'] == '2023-10-31'

    # --- Validation Errors ---

    @pytest.mark.parametrize("missing_field", [
        {'amount': '', 'category': 'Food', 'date': '2023-10-31'},
        {'amount': '100', 'category': '', 'date': '2023-10-31'},
        {'amount': '100', 'category': 'Food', 'date': ''},
        {'amount': None, 'category': 'Food', 'date': '2023-10-31'},
    ])
    def test_post_add_expense_missing_required_fields_shows_error(self, auth_client, missing_field):
        response = auth_client.post('/expenses/add', data=missing_field)

        assert response.status_code == 200, "Should re-render the form"
        assert b'All required fields must be filled' in response.data

    @pytest.mark.parametrize("invalid_amount", [
        '-50',       # Negative
        '0',         # Zero
        'abc',       # Non-numeric
        '10.5.2',     # Malformed numeric
    ])
    def test_post_add_expense_invalid_amount_shows_error(self, auth_client, invalid_amount):
        data = {
            'amount': invalid_amount,
            'category': 'Food',
            'date': '2023-10-31'
        }
        response = auth_client.post('/expenses/add', data=data)

        assert response.status_code == 200, "Should re-render the form"
        # The app has different flash messages for <= 0 vs non-numeric
        # We just check that some error message regarding the amount is present
        assert any(msg in response.data for msg in [
            b'Amount must be greater than zero',
            b'Invalid amount entered'
        ])
