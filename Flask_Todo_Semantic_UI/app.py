# app.py
# Python Flask SQLite Todo Semantic UI

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def getDB():
    conn = sqlite3.connect("./data/database.db")
    return conn

@app.route('/')
def index():
    conn = getDB()
    curs = conn.cursor()
    todos = curs.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    if len(todo.strip()) > 0:
        conn = getDB()
        curs = conn.cursor()
        curs.execute("INSERT INTO todos(todo) VALUES(?)", (todo,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/update/<int:id>/<int:status>')
def update(id, status):
    status = not status
    conn = getDB()
    curs = conn.cursor()
    curs.execute("UPDATE todos SET completed = ? WHERE id=?", (status, id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
        conn = getDB()
        curs = conn.cursor()
        curs.execute("DELETE FROM todos WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

