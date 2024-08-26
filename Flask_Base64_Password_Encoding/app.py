# app.py
# Python and Flask base64() password encoding and decoding.

from flask import Flask, request, render_template, session
from datetime import timedelta
import sqlite3
import base64
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "Be satisfied with what you have."
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if "username" in session:
            return render_template("index.html", username=session["username"])
        else:
            info = "Please login first."
            return render_template("index.html", info=info)
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password = base64.b64encode(password.encode("utf-8"))
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = list(curs.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password,),))

        if user:
            session["loggedin"] = True
            session["id"] = user[0][0]
            session["username"] = user[0][1]
            info = "Logged in successfully!"
            return render_template(
                "index.html", info=info, username=session["username"]
            )
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
        password = base64.b64encode(password.encode("utf-8"))

        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = curs.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchone()

        if user:
            info = 'Account already exists!'
            return render_template("register.html", info=info)
        if not re.match(r'[A-Za-z0-9]+', username):
            info = 'Username must contain only characters and numbers.'
            return render_template("register.html", info=info)
        else:
            curs.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
            conn.commit()
            conn.close()
            session["user"] = username
            info = f"Successfully registered username - {session['user']}."
            return render_template("index.html", info=info)

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
