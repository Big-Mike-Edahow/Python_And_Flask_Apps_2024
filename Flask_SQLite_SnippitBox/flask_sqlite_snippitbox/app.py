# app.py
# Flask SQLite3 SnippetBox

import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config["SECRET_KEY"] = "The west is the best"

def get_db():
    conn = sqlite3.connect("./database.db")
    return conn

def get_snippet(id):
    conn = get_db()
    snippet = conn.execute('SELECT * FROM snippets WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if snippet is None:
        abort(404)
    return snippet

@app.route("/")
def index():
    conn = get_db()
    snippets = conn.execute("SELECT * FROM snippets;").fetchall()
    conn.close()
    return render_template("index.html", snippets=snippets)

@app.route("/view")
def view():
    id = request.args.get("id")
    snippet = get_snippet(id)
    return render_template("view.html", snippet=snippet)

@app.route("/create/", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        firstline = request.form["firstline"]
        secondline = request.form["secondline"]
        thirdline = request.form["thirdline"]
        author = request.form["author"]

        if not title:
            flash("Title is required!")
        elif not firstline:
            flash("Firstline is required!")
        elif not secondline:
            flash('Secondline is required!')
        elif not thirdline:
            flash('Thirdline is required!')
        elif not author:
            flash("Author is required!")
        else:
            conn = get_db()
            conn.execute(
                "INSERT INTO snippets (title, firstline, secondline, thirdline, author) VALUES (?, ?, ?, ?, ?)",
                (title, firstline, secondline, thirdline, author),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("create.html")

@app.route('/edit', methods=('GET', 'POST'))
def edit():
    id = request.args.get("id")
    snippet = get_snippet(id)

    if request.method == 'POST':
        title = request.form['title']
        firstline = request.form['firstline']
        secondline = request.form['secondline']
        thirdline = request.form['thirdline']
        author = request.form['author']

        if not title:
            flash('Title is required!')
        elif not firstline:
            flash('Firstline is required!')
        elif not secondline:
            flash('Secondline is required!')
        elif not thirdline:
            flash('Thirdline is required!')
        elif not author:
            flash('Author is required!')
        else:
            conn = get_db()
            conn.execute('UPDATE snippets SET title = ?, firstline = ?, secondline = ?, thirdline = ?, author = ?'
                         ' WHERE id = ?',
                         (title, firstline, secondline, thirdline, author, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', snippet=snippet)

@app.route('/delete')
def delete():
    id = request.args.get("id")
    conn = get_db()
    curs = conn.cursor()
    curs.execute('DELETE FROM snippets WHERE id = ?', id,)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
