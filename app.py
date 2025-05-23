from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'inventory.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Initialize DB on app startup
def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    conn = get_db()
    items = conn.execute('SELECT * FROM inventory').fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    conn = get_db()
    conn.execute('INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)',
                 (name, quantity, price))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db()
    conn.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
