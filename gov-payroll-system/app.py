from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'secretkey123'

def init_db():
    if os.path.exists('payroll.db'):
        return
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    c.execute("CREATE TABLE payments (id INTEGER PRIMARY KEY, employee TEXT, amount TEXT, added_by TEXT)")
    users = [
        (1, 'admin', 'admin123', 'admin'),
        (2, 'user1', 'user123', 'employee'),
        (3, 'user2', 'user123', 'employee'),
        (4, 'user3', 'user123', 'employee'),
        (5, 'user4', 'user123', 'employee'),
        (6, 'user5', 'user123', 'employee'),
        (7, 'user6', 'user123', 'employee'),
        (8, 'user7', 'user123', 'employee'),
        (9, 'user8', 'user123', 'employee'),
        (10, 'user9', 'user123', 'employee'),
        (11, 'user10', 'user123', 'employee')
    ]
    payments = [
        (1, 'user1', '4500', 'admin'),
        (2, 'user2', '5000', 'admin'),
        (3, 'user3', '5500', 'admin'),
        (4, 'user4', '6000', 'admin'),
        (5, 'user5', '6500', 'admin'),
        (6, 'user6', '7000', 'admin'),
        (7, 'user7', '7500', 'admin'),
        (8, 'user8', '8000', 'admin'),
        (9, 'user9', '8500', 'admin'),
        (10, 'user10', '9000', 'admin')
    ]
    for u in users:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", u)
    for p in payments:
        c.execute("INSERT INTO payments VALUES (?, ?, ?, ?)", p)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        conn = sqlite3.connect('payroll.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE username='{uname}' AND password='{pword}'")
        user = c.fetchone()
        if user:
            session['user'] = user[1]
            session['role'] = user[3]
            return redirect('/dashboard')
        return render_template("error.html", msg="Invalid credentials")
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template("dashboard.html", user=session['user'], role=session['role'])

@app.route('/payment')
def payment():
    if 'user' not in session:
        return redirect('/')
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    user = request.args.get('employee', session['user'])
    c.execute(f"SELECT * FROM payments WHERE employee='{user}'")
    data = c.fetchall()
    return render_template("payment.html", data=data)

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return render_template("error.html", msg="Access Denied")
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT * FROM payments")
    payments = c.fetchall()
    return render_template("admin.html", payments=payments)

@app.route('/all-payments')
def all_payments():
    if 'user' not in session:
        return redirect('/')
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute("SELECT * FROM payments")
    payments = c.fetchall()
    return render_template("all_payments.html", payments=payments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
