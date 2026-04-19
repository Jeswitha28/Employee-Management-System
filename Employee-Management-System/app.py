import os
import io
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Fix for server environments
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jeshu@0701'
app.config['MYSQL_DB'] = 'employee_db'
from flask_mysqldb import MySQL
mysql = MySQL(app)


# ---------------- LOGIN ---------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect('/dashboard')
        else:
            flash("Invalid username or password")
            return redirect('/')

    return render_template('login.html')


# ---------------- LOGOUT ---------------- #
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- DASHBOARD ---------------- #
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html', role=session['role'])


# ---------------- REGISTER ---------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        cur = mysql.connection.cursor()

        # Check if user already exists
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            flash("User already exists")
            return redirect('/register')

        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, role))
        mysql.connection.commit()
        cur.close()

        flash("Registration successful")
        return redirect('/')

    return render_template('register.html')


# ---------------- EMPLOYEES ---------------- #
@app.route('/employees')
def employees():
    if 'username' not in session:
        return redirect('/')

    if session['role'] not in ['admin', 'hr']:
        return "Access denied"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()

    return render_template('employees.html', employees=data)


# ---------------- EXPORT EXCEL ---------------- #
@app.route('/export/excel')
def export_excel():
    if 'username' not in session or session['role'] not in ['admin', 'hr']:
        return "Access denied"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    cur.close()

    df = pd.DataFrame(rows, columns=['ID', 'Name', 'Department', 'Salary'])

    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output, download_name="employees.xlsx", as_attachment=True)


# ---------------- EXPORT PDF ---------------- #
@app.route('/export/pdf')
def export_pdf():
    if 'username' not in session or session['role'] not in ['admin', 'hr']:
        return "Access denied"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    cur.close()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Employee Report")

    y = 780
    for row in rows:
        p.drawString(50, y, f"{row[0]} - {row[1]} - {row[2]} - {row[3]}")
        y -= 20

    p.save()
    buffer.seek(0)

    return send_file(buffer, download_name='employees.pdf', as_attachment=True)


# ---------------- SALARY CHART ---------------- #
@app.route('/salary_chart')
def salary_chart():
    if 'username' not in session or session['role'] not in ['admin', 'hr']:
        return "Access denied"

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, salary FROM employees")
    data = cur.fetchall()
    cur.close()

    df = pd.DataFrame(data, columns=['Name', 'Salary'])

    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    plt.figure(figsize=(10, 6))
    plt.bar(df['Name'], df['Salary'])
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = os.path.join(static_dir, 'salary_chart.png')
    plt.savefig(chart_path)
    plt.close()

    return render_template('salary_chart.html', chart_url='static/salary_chart.png')


# ---------------- ATTENDANCE ---------------- #
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'username' not in session or session['role'] not in ['admin', 'hr']:
        return "Access denied"

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        date = request.form['date']

        for key, value in request.form.items():
            if key.startswith('emp_'):
                emp_id = key.split('_')[1]

                cur.execute(
                    "INSERT INTO attendance (employee_id, date, status) VALUES (%s, %s, %s)",
                    (emp_id, date, value)
                )

        mysql.connection.commit()
        cur.close()
        flash("Attendance marked successfully")
        return redirect('/attendance')

    cur.execute("SELECT id, name FROM employees")
    employees = cur.fetchall()
    cur.close()

    return render_template('attendance.html', employees=employees)


# ---------------- VIEW ATTENDANCE ---------------- #
@app.route('/attendance/view')
def view_attendance():
    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.name, a.date, a.status
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        ORDER BY a.date DESC
    """)
    logs = cur.fetchall()
    cur.close()

    return render_template('attendance_logs.html', logs=logs)


# ---------------- RUN APP ---------------- #
if __name__ == '__main__':
    app.run(debug=True)