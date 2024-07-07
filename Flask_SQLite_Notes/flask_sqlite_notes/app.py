# app.py
# Flask SQLite Notes App

import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Big Mike likes to make simple Go and Python web apps.'

def get_db():
    conn = sqlite3.connect('database.db')
    return conn

def get_note(id):
    conn = get_db()
    note = conn.execute('SELECT * FROM notes WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if note is None:
        abort(404)
    return note

@app.route("/")
def index():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()

    return render_template("index.html", notes=notes)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db()

    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return render_template("create.html")
        conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit', methods=('GET', 'POST'))
def edit():
    id = request.args.get("id")
    note = get_note(id)
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
        else:
            conn = get_db()
            conn.execute("UPDATE notes SET content = ? WHERE id = ?",
                         (content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', note=note)

@app.route('/delete')
def delete():
    id = request.args.get("id")
    conn = get_db()
    curs = conn.cursor()
    curs.execute('DELETE FROM notes WHERE id = ?', id,)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)

