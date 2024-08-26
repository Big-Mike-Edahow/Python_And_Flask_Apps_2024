# app.py
# Codecademy Accounts Dinner Party

from flask import Flask, flash, render_template, redirect, request, session
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "It's slow and steady that wins the race."
app.permanent_session_lifetime = timedelta(minutes=15)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        if "username" in session:
            username = session["username"]
            conn = sqlite3.connect("./data/database.db")
            curs = conn.cursor()
            parties = curs.execute("SELECT * FROM parties").fetchall()
            conn.close()
            return render_template('index.html', username=username, parties=parties)
        else:
            session.pop('_flashes', None)
            flash("Please login first.")
            return render_template("index.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = list(curs.execute("SELECT * FROM users WHERE username = ?",(username,),).fetchall())
        if user:
            if check_password_hash(user[0][2], password):
                session["loggedin"] = True
                session["id"] = user[0][0]
                session["username"] = user[0][1]
                parties = curs.execute("SELECT * FROM parties").fetchall()
                conn.close()
                return render_template("index.html", username=username, parties=parties)
            else:
                session.pop('_flashes', None)
                flash("Incorrect username or password.")
                return render_template("index.html")
        else:
            session.pop('_flashes', None)
            flash("Incorrect username or password.")
            return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        session.pop('_flashes', None)
        flash("Please fill out and submit the form.")
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password = generate_password_hash(password)

        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = curs.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchone()

        if user:
            session.pop('_flashes', None)
            flash("Account already exists!")
            return render_template("register.html")
        if not re.match(r'[A-Za-z0-9]+', username):
            session.pop('_flashes', None)
            flash("Username must contain only characters and numbers.")
            return render_template("register.html")
        else:
            curs.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
            conn.commit()
            conn.close()
            session["username"] = username
            session.pop('_flashes', None)
            msg =  f"Successfully registered username - {session['username']}."
            flash(msg)
            return render_template("index.html")

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        username = session.get('username')
        if username is not None:
            conn = sqlite3.connect("./data/database.db")
            curs = conn.cursor()
            parties = (curs.execute("SELECT * FROM parties WHERE username = ?",(username,),).fetchall())
            conn.commit()
            conn.close()
            return render_template("profile.html", username=username, parties=parties)
        else:
            return redirect("/", code=302)
    elif request.method == "POST":
        username = request.form["username"]
        date = request.form["date"]
        venue = request.form["venue"]
        main_dish = request.form["main_dish"]
        attendees = request.form["attendees"]
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        curs.execute("INSERT INTO parties(username, date, venue, main_dish, attendees) VALUES(?, ?, ?, ?, ?)", (username, date, venue, main_dish, attendees))
        conn.commit()
        conn.close()
        return redirect("/", code=302)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop('_flashes', None)
    flash("You have been logged out.")
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

