from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# ADD EXPENSE
# ==========================

@app.route("/add", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO expenses(title, amount, category, date)
        VALUES (?, ?, ?, ?)
        """, (title, amount, category, date))

        conn.commit()
        conn.close()

        return redirect("/expenses")

    return render_template("add_expense.html")


# ==========================
# VIEW & SEARCH EXPENSES
# ==========================

@app.route("/expenses")
def view_expenses():

    search = request.args.get("search")

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT * FROM expenses
        WHERE title LIKE ?
        OR category LIKE ?
        """, (
            '%' + search + '%',
            '%' + search + '%'
        ))

    else:

        cursor.execute("""
        SELECT * FROM expenses
        ORDER BY id DESC
        """)

    expenses = cursor.fetchall()

    conn.close()

    return render_template(
        "view_expenses.html",
        expenses=expenses
    )


# ==========================
# DELETE EXPENSE
# ==========================

@app.route("/delete/<int:id>")
def delete_expense(id):

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/expenses")


# ==========================
# UPDATE EXPENSE
# ==========================

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_expense(id):

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        cursor.execute("""
        UPDATE expenses
        SET title=?, amount=?, category=?, date=?
        WHERE id=?
        """, (
            title,
            amount,
            category,
            date,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/expenses")

    cursor.execute(
        "SELECT * FROM expenses WHERE id=?",
        (id,)
    )

    expense = cursor.fetchone()

    conn.close()

    return render_template(
        "update_expense.html",
        expense=expense
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)