# app.py
# Geek Python Flask Session Example

# Importing required modules
from flask import session
from flask import Flask, render_template, request, redirect, url_for
from datetime import timedelta

# Creating Flask App
app = Flask(__name__)
# Setting up Secret Key for Session Management
app.secret_key = "The final weeks of summer..."
# Setting Lifetime of Sessions
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session['message'] = "Enter your username to continue."
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        session['greet'] = f"Successfully registered username - {session['user']}."
        return redirect(url_for("index"))
 
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user')
    session['notify'] = "Username Removed from Session Storage."
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

