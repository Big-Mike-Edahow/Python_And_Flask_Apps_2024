# app.py
# Flask SQLite Birthdays App

import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["Secret Key"] = "It's the simple life for me"


def get_db():
    conn = sqlite3.connect("./database.db")
    return conn

def get_birthday(id):
    conn = get_db()
    curs = conn.cursor()
    birthday = curs.execute("SELECT * FROM birthdays WHERE id = ?", (id,)).fetchone()
    return birthday

def get_birthdays():
    conn = get_db()
    curs = conn.cursor()
    birthdays = curs.execute("SELECT * FROM birthdays")
    return birthdays


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        month = request.form["month"]
        day = request.form["day"]
        
        conn = get_db()
        curs = conn.cursor()
        curs.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)",
            (name, month, day),
        )
        conn.commit()

        birthdays = get_birthdays()
        return render_template("index.html", birthdays=birthdays)
    else:
        birthdays = get_birthdays()
        return render_template("index.html", birthdays=birthdays)

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/edit", methods=("GET", "POST"))
def edit():
    id = request.args.get("id")
    birthday = get_birthday(id)

    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        conn = get_db()
        curs =conn.cursor()
        curs.execute(
            "UPDATE birthdays SET name = ?, month = ?, day = ?" " WHERE id = ?",
            (name, month, day, id),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("edit.html", birthday=birthday)

@app.route("/delete")
def delete():
    id = request.args.get("id")
    conn = get_db()
    curs = conn.cursor()
    curs.execute(
        "DELETE FROM birthdays WHERE id = ?",
        id,
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

