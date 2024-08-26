# app.py
# Flask Confession Wall App

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "I like to roll out of bed and get to work."

@app.route("/")
def index():
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    data = curs.execute("SELECT * FROM confessions").fetchall()
    conn.commit()
    conn.close()

    return render_template("index.html", data=data)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    elif request.method == "POST":
        title = request.form["title"]
        confession = request.form["confession"]
        if title == "" or confession == "":
            return redirect("/", code=302)
        
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        curs.execute(
            "INSERT INTO confessions(title, confession) VALUES(?, ?)",(title,confession),)
        conn.commit()
        conn.close()
        return redirect("/", code=302)
    
@app.route("/confession")
def confession():
    id = request.args.get("id")
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    confession = curs.execute("SELECT * FROM confessions WHERE id=?", (id,)).fetchone()
    conn.commit()
    conn.close()
    return render_template("confession.html", confession=confession)
    
@app.route("/delete")
def delete():
    id = request.args.get("id")

    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute("DELETE FROM confessions WHERE id=?", id)
    conn.commit()
    conn.close()

    return redirect("/", code=302)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

