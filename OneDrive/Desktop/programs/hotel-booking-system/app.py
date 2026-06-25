from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret Key
app.secret_key = "hotel_booking_secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel_booking'

mysql = MySQL(app)


# ==========================
# HOME PAGE
# ==========================

@app.route('/')
def home():
    return render_template('user/home.html')


# ==========================
# REGISTER
# ==========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO users(name,email,phone,password)
            VALUES(%s,%s,%s,%s)
            """,
            (name, email, phone, hashed_password)
        )

        mysql.connection.commit()
        cur.close()

        flash("Registration Successful", "success")

        return redirect(url_for('login'))

    return render_template('user/register.html')


# ==========================
# LOGIN
# ==========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            [email]
        )

        user = cur.fetchone()

        cur.close()

        if user:

            db_password = user[4]

            if check_password_hash(db_password, password):

                session['user_id'] = user[0]
                session['user_name'] = user[1]

                flash("Login Successful", "success")

                return redirect(url_for('home'))

            else:
                flash("Invalid Password", "danger")

        else:
            flash("User Not Found", "danger")

    return render_template('user/login.html')


# ==========================
# LOGOUT
# ==========================

@app.route('/logout')
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect(url_for('login'))


# ==========================
# MY BOOKINGS
# ==========================

@app.route('/my-bookings')
def my_bookings():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('user/my_bookings.html')


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True,port=5007)