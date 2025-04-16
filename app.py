from flask import Flask, request, redirect, render_template, url_for, session
import sqlite3, datetime

app = Flask(__name__)
app.secret_key = 'donsail-secret'

def connect_db():
    return sqlite3.connect('donsail.db')

def create_tables():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            product TEXT,
            status TEXT,
            date TEXT
        )
        """)
create_tables()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'donsail' and request.form['password'] == 'donyaismail':
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    with connect_db() as conn:
        orders = conn.execute("SELECT * FROM orders").fetchall()
    return render_template("dashboard.html", orders=orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    name = request.form['customer_name']
    product = request.form['product']
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with connect_db() as conn:
        conn.execute("INSERT INTO orders (customer_name, product, status, date) VALUES (?, ?, ?, ?)", (name, product, 'جديد', date))
    return redirect('/dashboard')

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    with connect_db() as conn:
        conn.execute("DELETE FROM orders WHERE id=?", (order_id,))
    return redirect('/dashboard')

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    with connect_db() as conn:
        if request.method == 'POST':
            conn.execute("UPDATE orders SET customer_name=?, product=?, status=? WHERE id=?", (
                request.form['customer_name'], request.form['product'], request.form['status'], order_id
            ))
            return redirect('/dashboard')
        order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    return render_template('edit_order.html', order=order)

if __name__ == '__main__':
    app.run(debug=True)
