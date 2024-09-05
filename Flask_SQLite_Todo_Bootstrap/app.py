# app.py
# Flask SQLite Blog Bootstrap

from flask import Flask, flash, request, url_for, render_template, redirect, session
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect("./data/database.db")  
    curs = conn.cursor()
    posts = curs.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route("/view/<int:id>")
def view(id):
    conn = sqlite3.connect("./data/database.db")  
    curs = conn.cursor()
    post = curs.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('view.html', post=post)

@app.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == "GET":
        return render_template('create.html')
    elif request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        if title == "" or content == "":
            session.pop('_flashes', None)
            flash("Please fill out title and content.")
        else:
            conn = sqlite3.connect('./data/database.db')
            curs = conn.cursor()
            curs.execute('INSERT INTO posts (title, content) VALUES (?, ?)',(title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
        return render_template('create.html')

@app.route("/edit/<int:id>", methods=('GET', 'POST'))
def edit(id):
    if request.method == "GET":
        conn = sqlite3.connect("./data/database.db")  
        curs = conn.cursor()
        post = curs.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
        conn.close()
        return render_template("edit.html", post=post)
    elif request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect("./data/database.db")  
        curs = conn.cursor()
        curs.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("./data/database.db")  
    curs = conn.cursor()
    curs.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)

