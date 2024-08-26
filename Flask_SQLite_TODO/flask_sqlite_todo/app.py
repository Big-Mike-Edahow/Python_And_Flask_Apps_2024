# app.py
# Flask_SQLite_TODO

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "Big Mike likes SQLite"

def get_db():
    conn = sqlite3.connect("./database.db")
    return conn

@app.route('/')
def index():
    conn = get_db()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form["todo"]
    conn = get_db()
    curs = conn.cursor()
    curs.execute("INSERT INTO todos (todo) values (?)",
            (todo,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete')
def complete():
    id = request.args.get("id")
    conn = get_db()
    curs = conn.cursor()
    curs.execute("UPDATE todos SET done = 1 WHERE id = ?", id,)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete')
def delete():
    id = request.args.get("id")
    conn = get_db()
    curs = conn.cursor()
    curs.execute('DELETE FROM todos WHERE id = ?', id,)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

