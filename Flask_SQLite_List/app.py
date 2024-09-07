# app.py
# Flask SQLite CRUD

from flask import Flask, flash, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Some things I do better than others."

basedir = os.path.abspath(os.path.dirname(__file__))

def getDB():
    conn = sqlite3.connect(basedir + "/data/database.db")
    return conn

@app.route('/')
def index():
    conn = getDB() 
    curs = conn.cursor()
    entries = curs.execute("SELECT * FROM entries").fetchall()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or not description:
            session.pop('_flashes', None)
            flash("Please fill out title and description.")
        else:
            conn = getDB()
            curs = conn.cursor()
            curs.execute('INSERT INTO entries (title, description) VALUES (?, ?)',(title, description))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    return render_template("index.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == "GET":
        conn = getDB() 
        curs = conn.cursor()
        entry = curs.execute("SELECT * FROM entries WHERE id=?", (id,)).fetchone()
        conn.close()
        return render_template('edit.html', entry=entry)
    if request.method == "POST":
            form = request.form
            title = form.get('title')
            description = form.get('description')
            if not title or not description:
                session.pop('_flashes', None)
                flash("Please fill out title and description.")
                return redirect(url_for('update', id=id))
            else:
                conn = getDB()
                curs = conn.cursor()
                curs.execute('UPDATE entries SET title = ?, description = ? WHERE id = ?', (title, description, id))
                conn.commit()
                conn.close()
            return redirect(url_for('index'))
    
@app.route('/turn/<int:id>/<int:status>')
def turn(id, status):
    status = not status
    conn = getDB()
    curs = conn.cursor()
    curs.execute("UPDATE entries SET status = ? WHERE id=?", (status, id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
    conn = getDB()  
    curs = conn.cursor()
    curs.execute("DELETE FROM entries WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

