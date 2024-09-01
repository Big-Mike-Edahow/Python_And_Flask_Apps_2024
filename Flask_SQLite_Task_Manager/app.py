# app.py
# Python Flask SQLite Task Manager

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    tasks = curs.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if len(task.strip()) > 0:
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        curs.execute("INSERT INTO tasks(task) VALUES(?)", (task,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/complete/<int:id>')
def complete(id):
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute("UPDATE tasks SET completed = 1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        curs.execute("DELETE FROM tasks WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

