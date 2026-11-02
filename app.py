from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email, create_user, create_expense
from database.queries import get_user_by_id, get_summary_stats, get_recent_transactions, get_category_breakdown, get_user_by_id
from database.db import get_expense_by_id, update_expense




app = Flask(__name__)
app.secret_key = "dev_secret_key_for_flashing"



# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")

        try:
            hashed_password = generate_password_hash(password)
            create_user(name, email, hashed_password)
            flash("Account created successfully! Please sign in.")
            return redirect(url_for("login"))
        except Exception as e:
            if "UNIQUE constraint failed: users.email" in str(e):
                flash("Email already registered.")
            else:
                flash("An unexpected error occurred. Please try again.")
            return render_template("register.html")

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.")
            return render_template("login.html")

        user = get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Welcome back, " + user["name"] + "!")
            return redirect(url_for("profile"))

        flash("Invalid email or password.")
        return render_template("login.html")

    return render_template("login.html")



@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("landing"))



@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your profile.")
        return redirect(url_for("login"))

    user = get_user_by_id(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for("login"))

    # Date filters from query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    stats = get_summary_stats(user_id, start_date=start_date, end_date=end_date)
    transactions = get_recent_transactions(user_id, start_date=start_date, end_date=end_date)
    categories = get_category_breakdown(user_id, start_date=start_date, end_date=end_date)

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
        start_date=start_date,
        end_date=end_date
    )


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to add an expense.")
        return redirect(url_for("login"))

    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description")

        if not amount or not category or not date:
            flash("All required fields must be filled.")
            return render_template("add_expense.html")

        try:
            # Ensure amount is a valid number
            amount_val = float(amount)
            if amount_val <= 0:
                flash("Amount must be greater than zero.")
                return render_template("add_expense.html")

            from database.db import create_expense
            create_expense(user_id, amount_val, category, date, description)
            flash("Expense added successfully!")
            return redirect(url_for("profile"))
        except ValueError:
            flash("Invalid amount entered.")
            return render_template("add_expense.html")
        except Exception as e:
            flash("An unexpected error occurred. Please try again.")
            return render_template("add_expense.html")

    return render_template("add_expense.html")



@app.route("/expenses/<int:id>/edit-form")
def edit_expense_form(id):
    user_id = session.get("user_id")
    if not user_id:
        return "", 403

    expense = get_expense_by_id(id)
    if not expense:
        return "Not found", 404

    if expense["user_id"] != user_id:
        return "Forbidden", 403

    return render_template("edit_expense_form.html", expense=expense, errors={}, form_data=None)


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to edit an expense.")
        return redirect(url_for("login"))

    expense = get_expense_by_id(id)
    if not expense:
        abort(404)

    if expense["user_id"] != user_id:
        abort(403)

    if request.method == "POST":
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description")

        errors = {}
        if not amount or not category or not date:
            if not amount:
                errors["amount"] = "Amount is required."
            if not category:
                errors["category"] = "Category is required."
            if not date:
                errors["date"] = "Date is required."

        if errors:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {"success": False, "errors": errors}, 400
            else:
                return render_template("edit_expense.html", expense=expense, errors=errors, form_data=request.form)

        try:
            amount_value = float(amount)
            update_expense(id, amount_value, category, date, description)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {"success": True}
            else:
                flash("Expense updated successfully.")
                return redirect(url_for("profile"))
        except ValueError:
            errors["amount"] = "Invalid amount."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {"success": False, "errors": errors}, 400
            else:
                return render_template("edit_expense.html", expense=expense, errors=errors, form_data=request.form)

    return render_template("edit_expense.html", expense=expense, errors={}, form_data=None)



@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
