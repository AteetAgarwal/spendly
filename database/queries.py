import sqlite3
from database.db import get_db
from datetime import datetime

def get_user_by_id(user_id):
    """
    Fetches user details and formats the membership date.
    """
    with get_db() as conn:
        user = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if not user:
            return None

        # Format created_at (YYYY-MM-DD HH:MM:SS) to "Month YYYY"
        dt = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S")
        member_since = dt.strftime("%B %Y")

        return {
            "name": user["name"],
            "email": user["email"],
            "member_since": member_since
        }

def get_summary_stats(user_id):
    """
    Calculates total spent, transaction count, and identifies the top category.
    """
    with get_db() as conn:
        # Total and Count
        stats = conn.execute(
            "SELECT SUM(amount) as total, COUNT(id) as count FROM expenses WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        total_spent = stats["total"] if stats["total"] else 0.0
        transaction_count = stats["count"] if stats["count"] else 0

        # Top Category
        top_cat_row = conn.execute(
            """
            SELECT category FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()

        top_category = top_cat_row["category"] if top_cat_row else "—"

        return {
            "total_spent": total_spent,
            "transaction_count": transaction_count,
            "top_category": top_category
        }

def get_recent_transactions(user_id, limit=10):
    """
    Fetches the most recent transactions for a user.
    """
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT date, description, category, amount
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, created_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        ).fetchall()

        return [dict(row) for row in rows]

def get_category_breakdown(user_id):
    """
    Fetches spending per category with integer percentages that sum to 100.
    """
    with get_db() as conn:
        # Get totals per category
        rows = conn.execute(
            """
            SELECT category as name, SUM(amount) as amount
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY amount DESC
            """,
            (user_id,)
        ).fetchall()

        if not rows:
            return []

        total_sum = sum(row["amount"] for row in rows)
        if total_sum == 0:
            return []

        breakdown = []
        running_pct_sum = 0

        # Calculate percentages with rounding
        for i, row in enumerate(rows):
            pct = round((row["amount"] / total_sum) * 100)

            # For the last item, adjust to ensure sum is exactly 100
            if i == len(rows) - 1:
                pct = 100 - running_pct_sum

            breakdown.append({
                "name": row["name"],
                "amount": row["amount"],
                "pct": pct
            })
            running_pct_sum += pct

        return breakdown
