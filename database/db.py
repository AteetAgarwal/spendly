import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_PATH = "spendly.db"

def get_db():
    """
    Returns a SQLite connection with row_factory and foreign keys enabled.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # Ensure foreign key constraints are enforced in SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    # Allow accessing columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Creates all tables using CREATE TABLE IF NOT EXISTS.
    """
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)
        conn.commit()

def seed_db():
    """
    Inserts sample data for development.
    """
    with get_db() as conn:
        # Check if users already exist to avoid duplicates
        cursor = conn.execute("SELECT 1 FROM users LIMIT 1")
        if cursor.fetchone():
            return

        # Insert demo user
        demo_user = {
            "name": "Demo User",
            "email": "demo@spendly.com",
            "password": generate_password_hash("demo123")
        }

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (demo_user["name"], demo_user["email"], demo_user["password"])
        )
        user_id = cursor.lastrowid

        # Sample expenses (INR ₹)
        expenses = [
            (user_id, 450.00, 'Food', '2026-10-01', 'Grocery shopping'),
            (user_id, 120.00, 'Transport', '2026-10-02', 'Auto rickshaw to office'),
            (user_id, 2100.00, 'Bills', '2026-10-05', 'Internet Bill'),
            (user_id, 800.00, 'Health', '2026-10-08', 'Pharmacy meds'),
            (user_id, 1200.00, 'Entertainment', '2026-10-12', 'Movie ticket & Popcorn'),
            (user_id, 3500.00, 'Shopping', '2026-10-15', 'New shoes'),
            (user_id, 200.00, 'Other', '2026-10-18', 'Gift wrap'),
            (user_id, 300.00, 'Food', '2026-10-20', 'Lunch at cafe'),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses
        )
        conn.commit()