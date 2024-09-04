# Flask SQLite Manage Users

import sqlite3
from datetime import date
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "A walkin' I will go..."

def getDB():
    conn = sqlite3.connect("./data/database.db")
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    errors = ""
    today = date.today()
    if request.method == "POST":
        user = request.form["user"]

        if user != "":
            try:
                conn = getDB()
                curs = conn.cursor()
                curs.execute(
                    "INSERT INTO users(user) VALUES(?)", (user,))
                conn.commit()
                conn.close()

                return render_template("results.html", user=user, today=today)

            except Exception as e:
                errors = f"[!] Errors found: {e}"
        else:
            errors = "You must insert a username first"

    return render_template("index.html", today=today, errors=errors)

# render admin page
@app.route("/admin", methods=["GET", "POST"])
def admin():
    PASSWORD = "admin"
    user_list = ""
    invalid = ""

    if request.method == "POST":
        psw = request.form["password"]

        if psw == PASSWORD:
            conn = getDB()
            curs = conn.cursor()
            user_list = curs.execute("SELECT * FROM users").fetchall()
            conn.close()
        else:
            invalid = "[!!!] Wrong password"

    return render_template("admin.html", user_list=user_list, invalid=invalid)

@app.route("/delete/<int:id>")
def delete(id):
    conn = getDB()
    curs = conn.cursor()
    curs.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

# render error page 404
@app.errorhandler(404)
def page_not_found(e):
    return '''<h1>OOPS</h1> <h2> Page not found </h2> <img src="../static/images/404.png">''', 404


if __name__ == "__main__":
    app.run(debug=True)
