import os
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(Config)

# -----------------------------
# Database Connection Helper
# -----------------------------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            Config.DATABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.DatabaseError as e:
        logging.error(f"Database connection error: {e}")
        return None

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    sort_by = request.args.get("sort_by", "entry_date")
    order = request.args.get("order", "desc")
    
    # Simple validation against SQL injection for dynamic sorting
    valid_sort_columns = ["entry_date", "amount", "category"]
    if sort_by not in valid_sort_columns:
        sort_by = "entry_date"
    
    order = "asc" if order.lower() == "asc" else "desc"

    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database. Please try again later.", "danger")
        return render_template("index.html", expenses=[])

    try:
        cur = conn.cursor()
        query = f"SELECT ctid::text as expense_id, * FROM expense_records ORDER BY {sort_by} {order}"
        cur.execute(query)
        expenses = cur.fetchall()
        
    except psycopg2.Error as e:
        logging.error(f"Error fetching expenses: {e}")
        flash("An error occurred while retrieving expenses.", "danger")
        expenses = []
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()

    return render_template("index.html", expenses=expenses, sort_by=sort_by, order=order)

# -----------------------------
# Add Expense
# -----------------------------
@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        entry_date = request.form.get("entry_date")
        category = request.form.get("category")
        description = request.form.get("description", "")
        amount = request.form.get("amount")
        location = request.form.get("location", "")
        payment_mode = request.form.get("payment_mode", "")

        if not all([entry_date, category, amount]):
            flash("Date, Category, and Amount are required fields.", "warning")
            return redirect(url_for("add_expense"))

        conn = get_db_connection()
        if not conn:
            flash("Failed to connect to the database.", "danger")
            return redirect(url_for("add_expense"))

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO expense_records
                (entry_date, category, description, amount, location, payment_mode)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (entry_date, category, description, amount, location, payment_mode))
            conn.commit()
            flash("Expense Added Successfully", "success")
            return redirect(url_for("home"))
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Error adding expense: {e}")
            flash("Failed to add expense. Please try again.", "danger")
        finally:
            if 'cur' in locals() and cur:
                cur.close()
            if conn:
                conn.close()

    return render_template("add_expense.html")

# -----------------------------
# Edit Expense
# -----------------------------
@app.route("/edit/<string:id>", methods=["GET", "POST"])
def edit_expense(id):
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        entry_date = request.form.get("entry_date")
        category = request.form.get("category")
        description = request.form.get("description", "")
        amount = request.form.get("amount")
        location = request.form.get("location", "")
        payment_mode = request.form.get("payment_mode", "")

        if not all([entry_date, category, amount]):
            flash("Date, Category, and Amount are required fields.", "warning")
            return redirect(url_for("edit_expense", id=id))

        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE expense_records
                SET entry_date=%s, category=%s, description=%s, amount=%s, location=%s, payment_mode=%s
                WHERE ctid=%s::tid
            """, (entry_date, category, description, amount, location, payment_mode, id))
            conn.commit()
            flash("Expense Updated Successfully", "success")
            return redirect(url_for("home"))
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Error updating expense: {e}")
            flash("Failed to update expense.", "danger")
        finally:
            if 'cur' in locals() and cur:
                cur.close()
            if conn:
                conn.close()

    else:
        try:
            cur = conn.cursor()
            cur.execute("SELECT ctid::text as expense_id, * FROM expense_records WHERE ctid=%s::tid", (id,))
            expense = cur.fetchone()
            if not expense:
                flash("Expense not found.", "warning")
                return redirect(url_for("home"))
        except psycopg2.Error as e:
            logging.error(f"Error fetching expense {id}: {e}")
            flash("An error occurred.", "danger")
            expense = None
        finally:
            if 'cur' in locals() and cur:
                cur.close()
            if conn:
                conn.close()

        return render_template("edit_expense.html", expense=expense)


# -----------------------------
# Delete Expense
# -----------------------------
@app.route("/delete/<string:id>", methods=["POST"])
def delete_expense(id):
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "danger")
        return redirect(url_for("home"))

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM expense_records WHERE ctid=%s::tid", (id,))
        conn.commit()
        flash("Expense Deleted Successfully", "success")
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Error deleting expense {id}: {e}")
        flash("Failed to delete expense.", "danger")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()

    return redirect(url_for("home"))

# -----------------------------
# Delete All Expenses
# -----------------------------
@app.route("/delete_all", methods=["POST"])
def delete_all():
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "danger")
        return redirect(url_for("home"))

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM expense_records")
        conn.commit()
        flash("All Expenses Deleted", "success")
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Error deleting all expenses: {e}")
        flash("Failed to delete all expenses.", "danger")
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()

    return redirect(url_for("home"))

# -----------------------------
# Search Expense
# -----------------------------
@app.route("/search")
def search():
    query = request.args.get("query", "").strip()

    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for("home"))

    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "danger")
        return redirect(url_for("home"))

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ctid::text as expense_id, * FROM expense_records
            WHERE category ILIKE %s
               OR description ILIKE %s
               OR location ILIKE %s
               OR payment_mode ILIKE %s
            ORDER BY entry_date DESC
        """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        expenses = cur.fetchall()
    except psycopg2.Error as e:
        logging.error(f"Error searching expenses: {e}")
        flash("An error occurred during search.", "danger")
        expenses = []
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if conn:
            conn.close()

    return render_template("search_results.html", expenses=expenses, query=query)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)