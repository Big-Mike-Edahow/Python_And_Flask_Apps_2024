# app.py
# Flask Session Tutorial

from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "I like to get my routine down."
app.permanent_session_lifetime = timedelta(minutes=5)

# Dictionary with login credentials.
database = {"Big_Mike" : "foobar"}

@app.route("/")
def index():
	if "username" in session:
		return render_template("index.html", username=session["username"])
	else:
		info = "Please login first."
		return render_template("index.html", info=info)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if username in database and database[username] == password:
			session.permanent = True
			session['username'] = username
			session['loggedin'] = True
			return render_template("index.html", username=username)
		elif username == "":
			info = "Please enter a username."
			return render_template("login.html", info=info)
		elif username in database and password == "":
			info = "Please enter a password."
			username = username
			return render_template("login.html", info=info, username=username)
		elif username in database and password not in database:
			info = "Please enter a valid password."
			username = username
			return render_template("login.html", info=info,username=username)
		elif username not in database or database[username] != password:
			info = "Invalid username or password."
			return render_template("login.html", info=info)
	elif request.method == "GET":
			if "username" in session:
				info = "Already logged in."
				return render_template("index.html", info=info, username=session["username"])
			else:
				return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

