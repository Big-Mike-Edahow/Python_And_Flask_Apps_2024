# app.py
# Flask SQLite3 Todo App

from flask import Flask, flash, render_template, request, redirect, abort, url_for, session
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "I love peaches and bananas."

def getTodo(id):
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    todo = curs.execute('SELECT * FROM todos WHERE id = ?', (id,)).fetchone()
    conn.close()
    if todo is None:
        abort(404)
    return todo

@app.route("/")
def index():
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    todos = curs.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def addTodo():
    todo = request.form["todo"]
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute("INSERT INTO todos (todo) VALUES (?)", (todo,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if request.method == 'GET':
        todo = getTodo(id)
        return render_template('edit.html', todo=todo)
    elif request.method == 'POST':
        todo = request.form['todo']
        if todo == "":
            session.pop('_flashes', None)
            flash("Please enter a todo.")
            return redirect(url_for('edit', id=id ))
        else:
            conn = sqlite3.connect('./data/database.db')
            curs = conn.cursor()
            curs.execute('UPDATE todos SET todo = ? WHERE id = ?', (todo, id))
            conn.commit()
            conn.close()
            return redirect("/")

@app.route("/delete/<int:id>")
def deleteTodo(id):
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

