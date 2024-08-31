# app.py
# Simple Todo List App

from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "Peeking over your shoulder."

@app.route('/')
def index():
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    todos = curs.execute("SELECT * FROM todos").fetchall()
    completed = curs.execute("SELECT * FROM completed").fetchall()
    conn.close()
    return render_template('index.html', todos=todos, completed=completed)

@app.route('/addTodo')
def addTodo():
    todo = request.args.get('todo')
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO todos(todo) VALUES(?)", (todo,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/getTodo', methods=['GET'])
def getTodo():
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    todo = curs.execute("SELECT * FROM todos").fetchone()
    conn.close()
    
    return render_template("index.html", todo=todo)

@app.route('/completed/<int:id>/<string:todo>')
def completed(id, todo):
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO completed(todo, todo_id) VALUES(?,?)", (todo,id))
    curs.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/deleteTodo/<int:id>')
def deleteTodo(id):
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    curs.execute("DELETE FROM todos WHERE id=?", (id,))
    conn.commit()

    return redirect('/')

@app.route('/deleteCompleted/<int:id>')
def deleteCompleted(id):
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    curs.execute("DELETE FROM completed WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)

