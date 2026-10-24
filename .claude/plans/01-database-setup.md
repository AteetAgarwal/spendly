# Implementation Plan: Database Setup

## Context
The goal of this task is to implement the data layer foundation for Spendly. This involves creating a SQLite database with `users` and `expenses` tables, implementing helper functions for database connectivity and initialization, and integrating these into the Flask app startup sequence. This establishes the necessary infrastructure for authentication and expense tracking features.

## Recommended Approach

### 1. Database Schema Implementation (`database/db.py`)
I will implement three core functions:
- `get_db()`:
    - Establish connection to `spendly.db`.
    - Execute `PRAGMA foreign_keys = ON` to enforce referential integrity.
    - Set `conn.row_factory = sqlite3.Row` for name-based column access.
- `init_db()`:
    - Create the `users` table with `id` (PK), `name`, `email` (UNIQUE), `password_hash`, and `created_at`.
    - Create the `expenses` table with `id` (PK), `user_id` (FK), `amount` (REAL), `category`, `date` (YYYY-MM-DD), `description`, and `created_at`.
    - Use `CREATE TABLE IF NOT EXISTS` to ensure idempotency.
- `seed_db()`:
    - Check for existing data in `users` to prevent duplicate seeding.
    - Insert a demo user (`Demo User`, `demo@spendly.com`) with a hashed password using `werkzeug.security.generate_password_hash`.
    - Insert 8 sample expenses (INR ₹) covering all required categories: Food, Transport, Bills, Health, Entertainment, Shopping, and Other.

### 2. Application Integration (`app.py`)
- Import `init_db` and `seed_db` from `database.db`.
- In the `if __name__ == "__main__":` block, wrap the initialization calls within `with app.app_context():` to ensure the database is ready before the server starts.

## Critical Files
- `database/db.py`: Implementation of DB helpers and schema.
- `app.py`: Startup integration.

## Verification Plan
I will verify the implementation using a standalone script to test the following:
1. **Schema Integrity**: Confirm tables are created with correct columns and types.
2. **Foreign Key Enforcement**: Verify that inserting an expense with a non-existent `user_id` raises a `sqlite3.IntegrityError`.
3. **Unique Constraint**: Verify that inserting a duplicate email raises a `sqlite3.IntegrityError`.
4. **Row Access**: Confirm that `get_db()` returns rows that can be accessed by column name.
5. **Seeding Idempotency**: Run `seed_db()` multiple times and verify that only one demo user is present.
6. **App Startup**: Launch the app and confirm it starts without errors and creates `spendly.db`.