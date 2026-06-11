from Database.db_connection import get_db_connection


# ==========================================
# GET ALL EXPENSES
# ==========================================
def get_all_expenses():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC
    """)

    expenses = cur.fetchall()

    cur.close()
    conn.close()

    return expenses


# ==========================================
# GET SINGLE EXPENSE
# ==========================================
def get_expense_by_id(expense_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM expenses
        WHERE expense_id = %s
    """, (expense_id,))

    expense = cur.fetchone()

    cur.close()
    conn.close()

    return expense


# ==========================================
# ADD EXPENSE
# ==========================================
def add_expense(
    expense_date,
    category,
    description,
    amount,
    location,
    payment_mode
):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO expenses
        (
            expense_date,
            category,
            description,
            amount,
            location,
            payment_mode
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """,
    (
        expense_date,
        category,
        description,
        amount,
        location,
        payment_mode
    ))

    conn.commit()

    cur.close()
    conn.close()


# ==========================================
# UPDATE EXPENSE
# ==========================================
def update_expense(
    expense_id,
    expense_date,
    category,
    description,
    amount,
    location,
    payment_mode
):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE expenses
        SET
            expense_date = %s,
            category = %s,
            description = %s,
            amount = %s,
            location = %s,
            payment_mode = %s
        WHERE expense_id = %s
    """,
    (
        expense_date,
        category,
        description,
        amount,
        location,
        payment_mode,
        expense_id
    ))

    conn.commit()

    cur.close()
    conn.close()


# ==========================================
# DELETE EXPENSE
# ==========================================
def delete_expense(expense_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM expenses
        WHERE expense_id = %s
    """, (expense_id,))

    conn.commit()

    cur.close()
    conn.close()


# ==========================================
# DELETE ALL EXPENSES
# ==========================================
def delete_all_expenses():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM expenses
    """)

    conn.commit()

    cur.close()
    conn.close()


# ==========================================
# SEARCH EXPENSES
# ==========================================
def search_expenses(query):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM expenses
        WHERE
            category ILIKE %s
            OR description ILIKE %s
            OR location ILIKE %s
            OR payment_mode ILIKE %s
        ORDER BY expense_date DESC
    """,
    (
        f"%{query}%",
        f"%{query}%",
        f"%{query}%",
        f"%{query}%"
    ))

    expenses = cur.fetchall()

    cur.close()
    conn.close()

    return expenses


# ==========================================
# TOTAL EXPENSE
# ==========================================
def get_total_expense():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(amount),0) AS total
        FROM expenses
    """)

    total = cur.fetchone()

    cur.close()
    conn.close()

    return total["total"]


# ==========================================
# TOTAL RECORDS
# ==========================================
def get_total_records():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM expenses
    """)

    total = cur.fetchone()

    cur.close()
    conn.close()

    return total["total"]