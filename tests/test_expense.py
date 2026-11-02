import pytest
from app import app
from database.db import get_db, delete_expense


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_delete_expense_helper():
    # Insert a test expense
    db = get_db()
    cursor = db.execute("INSERT INTO expenses (user_id, amount, category, date, description, created_at) VALUES (1, 50.0, 'Test', '2023-01-01', 'Test expense', '2023-01-01 00:00:00')")
    expense_id = cursor.lastrowid
    db.commit()

    # Delete the expense
    result = delete_expense(expense_id)
    assert result is True

    # Ensure it no longer exists
    expense = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    assert expense is None


def test_delete_expense_route(client):
    # Log in as user 1
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "User1"

    # Insert a test expense
    db = get_db()
    cursor = db.execute("INSERT INTO expenses (user_id, amount, category, date, description, created_at) VALUES (1, 100.0, 'Test', '2023-01-02', 'Test expense route', '2023-01-02 00:00:00')")
    expense_id = cursor.lastrowid
    db.commit()

    # Attempt delete
    response = client.get(f"/expenses/{expense_id}/delete", follow_redirects=True)
    assert b"Expense deleted successfully." in response.data

    # Ensure expense no longer exists
    expense = db.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    assert expense is None


def test_delete_expense_nonexistent(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/expenses/999999/delete")
    assert response.status_code == 404


def test_delete_expense_not_owner(client):
    # Log in as user 1
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    # Insert an expense owned by user 2
    db = get_db()
    cursor = db.execute("INSERT INTO expenses (user_id, amount, category, date, description, created_at) VALUES (2, 200.0, 'Test', '2023-01-03', 'Other user expense', '2023-01-03 00:00:00')")
    expense_id = cursor.lastrowid
    db.commit()

    response = client.get(f"/expenses/{expense_id}/delete")
    assert response.status_code == 403

