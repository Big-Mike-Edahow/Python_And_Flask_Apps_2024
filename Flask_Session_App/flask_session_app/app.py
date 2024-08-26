# app.py

from flask import session
from flask import Flask, render_template, request, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Situation normal, all fouled up."
app.permanent_session_lifetime = timedelta(minutes=1) # Session timeout 1 minute

@app.route("/")
def index():
    if not session.get('user'):
        session['notify'] = "User not logged in."
    return render_template("index.html")

# Route for Registering Username
@app.route("/add", methods=["GET", "POST"])
def add():
    session['message'] = "Enter your username to continue."
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        session['greet'] = f"Successfully registered username - {session['user']}."
        return redirect(url_for("index"))
 
    return render_template("add.html")

# Route for Removing Username
@app.route("/remove")
def remove():
    session.pop('user')
    session['notify'] = "Username Removed from Session Storage."
    return redirect(url_for("logged_out"))

@app.route("/logged_out")
def logged_out():
    return render_template("logged_out.html")

if __name__ == '__main__':
    app.run(debug=True)

