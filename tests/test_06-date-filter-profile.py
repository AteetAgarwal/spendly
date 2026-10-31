import pytest
from app import app as flask_app
from database.db import init_db, get_db
import sqlite3
import database.db

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': ':memory:',
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })

    # We use a shared connection for the :memory: database across the test
    # because each call to sqlite3.connect(':memory:') creates a NEW database.
    original_get_db = database.db.get_db
    test_conn = sqlite3.connect(':memory:', check_same_thread=False)
    test_conn.execute("PRAGMA foreign_keys = ON")
    test_conn.row_factory = sqlite3.Row

    def mocked_get_db():
        return test_conn

    database.db.get_db = mocked_get_db

    with flask_app.app_context():
        init_db()
        yield flask_app

    database.db.get_db = original_get_db

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """A test client that is already logged in."""
    client.post('/register', data={'name': 'Test User', 'email': 'test@example.com', 'password': 'testpass', 'confirm_password': 'testpass'})
    client.post('/login', data={'email': 'test@example.com', 'password': 'testpass'})
    return client

@pytest.fixture
def seed_expenses(auth_client):
    """Seeds the database with expenses across different dates for a specific user."""
    with flask_app.app_context():
        db = get_db()
        user = db.execute("SELECT id FROM users WHERE email = ?", ('test@example.com',)).fetchone()
        user_id = user['id']

        expenses = [
            (user_id, 100.0, 'Food', '2023-01-01', 'Jan Expense'),
            (user_id, 200.0, 'Transport', '2023-01-15', 'Jan Mid Expense'),
            (user_id, 300.0, 'Bills', '2023-02-01', 'Feb Start Expense'),
            (user_id, 400.0, 'Health', '2023-02-15', 'Feb Mid Expense'),
            (user_id, 500.0, 'Entertainment', '2023-03-01', 'Mar Start Expense'),
        ]
        db.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses
        )
        db.commit()
    return True

class TestDateFilterProfile:

    def test_profile_auth_guard(self, client):
        """Ensure the profile page requires authentication."""
        response = client.get('/profile')
        assert response.status_code == 302
        assert '/login' in response.location, "Unauthenticated user should be redirected to login"

    def test_profile_happy_path_date_range(self, auth_client, seed_expenses):
        """Filtering with both start_date and end_date produces correct results."""
        # Filter for January 2023
        response = auth_client.get('/profile?start_date=2023-01-01&end_date=2023-01-31')
        assert response.status_code == 200

        # Expected total: 100 + 200 = 300
        assert b'300' in response.data, "Total spent should be 300 for January"
        assert b'Jan Expense' in response.data
        assert b'Jan Mid Expense' in response.data
        assert b'Feb Start Expense' not in response.data
        assert b'Mar Start Expense' not in response.data

    def test_profile_filter_only_start_date(self, auth_client, seed_expenses):
        """Filtering with only start_date provided."""
        # From Feb 1 onwards
        response = auth_client.get('/profile?start_date=2023-02-01')
        assert response.status_code == 200

        # Expenses from Feb 1, Feb 15, Mar 1 (300 + 400 + 500 = 1200)
        assert b'1200' in response.data
        assert b'Feb Start Expense' in response.data
        assert b'Mar Start Expense' in response.data
        assert b'Jan Expense' not in response.data

    def test_profile_filter_only_end_date(self, auth_client, seed_expenses):
        """Filtering with only end_date provided."""
        # Up to Jan 31
        response = auth_client.get('/profile?end_date=2023-01-31')
        assert response.status_code == 200

        # Expenses from Jan 1, Jan 15 (100 + 200 = 300)
        assert b'300' in response.data
        assert b'Jan Expense' in response.data
        assert b'Feb Start Expense' not in response.data

    def test_profile_filter_invalid_range(self, auth_client, seed_expenses):
        """Invalid date range (start_date > end_date) should handle gracefully."""
        response = auth_client.get('/profile?start_date=2023-03-01&end_date=2023-01-01')
        assert response.status_code == 200
        assert b'Jan Expense' not in response.data
        assert b'Mar Start Expense' not in response.data

    def test_profile_filter_no_data_in_range(self, auth_client, seed_expenses):
        """Dates outside the range of existing data should return no results."""
        response = auth_client.get('/profile?start_date=2020-01-01&end_date=2020-12-31')
        assert response.status_code == 200
        assert b'Jan Expense' not in response.data
        assert b'Feb Start Expense' not in response.data

    def test_profile_ui_persistence(self, auth_client, seed_expenses):
        """Verify that start_date and end_date are passed back to the template."""
        start = '2023-01-01'
        end = '2023-01-31'
        response = auth_client.get(f'/profile?start_date={start}&end_date={end}')
        assert response.status_code == 200
        assert start.encode() in response.data, f"Start date {start} should be persisted"
        assert end.encode() in response.data, f"End date {end} should be persisted"

    def test_profile_clear_filter(self, auth_client, seed_expenses):
        """Clear filter returns the all-time view."""
        auth_client.get('/profile?start_date=2023-01-01&end_date=2023-01-31')
        response = auth_client.get('/profile')
        assert response.status_code == 200

        # All expenses (100+200+300+400+500 = 1500)
        assert b'1500' in response.data
        assert b'Jan Expense' in response.data
        assert b'Mar Start Expense' in response.data

    @pytest.mark.parametrize("invalid_date", ["not-a-date", "2023-13-45", ""])
    def test_profile_invalid_date_format(self, auth_client, seed_expenses, invalid_date):
        """Invalid date formats should not crash the application."""
        response = auth_client.get(f'/profile?start_date={invalid_date}&end_date={invalid_date}')
        assert response.status_code == 200
