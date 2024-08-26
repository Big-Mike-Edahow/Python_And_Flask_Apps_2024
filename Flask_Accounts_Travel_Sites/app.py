# app.py
# Flask Accounts Travel Sites

from flask import Flask, request, render_template, redirect, session
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "I'll do it another way."
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if "username" in session:
            conn = sqlite3.connect("./data/database.db")
            curs = conn.cursor()
            posts = curs.execute("SELECT * FROM posts").fetchall()
            conn.close()
            return render_template("index.html", username=session["username"], posts=posts)
        else:
            info = "Please login first."
            return render_template("index.html", info=info)
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = list(curs.execute("SELECT * FROM travelers WHERE username = ?",(username,),).fetchall())
        if check_password_hash(user[0][2], password):
            session["loggedin"] = True
            session["id"] = user[0][0]
            session["username"] = user[0][1]
            posts = curs.execute("SELECT * FROM posts").fetchall()
            conn.close()
            return render_template(
                "index.html", username=session["username"], posts=posts)
        else:
            info = "Incorrect username/password!"
            return render_template("index.html", info=info)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        info = "Please fill out and submit the form."
        return render_template("register.html", info=info)
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password = generate_password_hash(password)

        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = curs.execute("SELECT * FROM travelers WHERE username = ?", (username, )).fetchone()

        if user:
            info = 'Account already exists!'
            return render_template("register.html", info=info)
        if not re.match(r'[A-Za-z0-9]+', username):
            info = 'Username must contain only characters and numbers.'
            return render_template("register.html", info=info)
        else:
            curs.execute("INSERT INTO travelers(username, password) VALUES(?, ?)", (username, password))
            conn.commit()
            conn.close()
            session["user"] = username
            info = f"Successfully registered username - {session['user']}."
            return render_template("index.html", info=info)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == 'GET':
        if "username" in session:
            username = session["username"]
        elif request.args.get("username") and "username" in session:
            username = request.args.get("username")
        elif request.args.get("username") and "username" not in session:
            return redirect("/", code=302)
        else:
            return redirect("/", code=302)
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        posts = (curs.execute("SELECT * FROM posts WHERE username = ?",(username,),).fetchall())
        conn.commit()
        conn.close()
        return render_template("user.html", username=username, posts=posts)
    elif request.method == "POST":
        username = request.form["username"]
        city = request.form["city"]
        country = request.form["country"]
        description = request.form["description"]
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        curs.execute("INSERT INTO posts(username, city, country, description) VALUES(?, ?, ?, ?)", (username, city, country, description))
        conn.commit()
        conn.close()
        return redirect("/", code=302)

@app.route("/logout")
def logout():
    session.pop("username")
    info = "You have been logged out."
    return render_template("index.html", info=info)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

