# app.py
# Flask Tourist Attractions

import sqlite3
from flask import Flask, flash, render_template, request, redirect, abort

app = Flask(__name__)
app.config["SECRET_KEY"] = "Some things I can understand better than others."

def getAttraction(id):
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    attraction = curs.execute("SELECT * FROM attractions WHERE id = ?", (id,)).fetchone()
    conn.close()
    if attraction is None:
        abort(404)
    return attraction

def getAllAttractions():
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    attractions = curs.execute("SELECT * FROM attractions").fetchall()
    conn.close()
    if attractions is None:
        abort(404)
    return attractions

@app.route("/")
def index():
    attractions = getAllAttractions()
    return render_template("index.html", attractions=attractions)

@app.route("/view")
def view():
    id = request.args.get("id")
    attraction = getAttraction(id)
    return render_template("view.html", attraction=attraction)

@app.route("/create/", methods=("GET", "POST"))
def create():
    if request.method == "GET":
        return render_template("create.html")
    elif request.method == "POST":
        attraction = request.form["attraction"]
        description = request.form["description"]
        status = request.form["status"]
        image_url = request.form["image_url"]
        if not attraction or not description or not status or not image_url:
            flash("Please fill out all of the fields.")
            return render_template("create.html")
        else:
            conn = sqlite3.connect("./data/database.db")
            curs = conn.cursor()
            curs.execute(
                "INSERT INTO attractions(attraction, description, status, image_url) VALUES(?, ?, ?, ?)",
                (attraction, description, status, image_url),)
            conn.commit()
            conn.close()
            return redirect("/")

@app.route('/edit', methods=('GET', 'POST'))
def edit():
    if request.method == "GET":
        id = request.args.get("id")
        attraction = getAttraction(id)
        return render_template("edit.html", attraction=attraction)
    elif request.method == 'POST':
        id = request.form["id"]
        attraction = request.form["attraction"]
        description = request.form["description"]
        status = request.form["status"]
        image_url = request.form["image_url"]
        if not attraction or not description or not status or not image_url:
            flash("Please fill out all of the fields.")
            attraction = getAttraction(id)
            return render_template("edit.html", attraction=attraction)
        else:
            conn = sqlite3.connect("./data/database.db")
            curs = conn.cursor()
            curs.execute("UPDATE attractions SET attraction = ?, description = ?, status = ?, image_url = ? WHERE id = ?",
                         (attraction, description, status, image_url, id))
            conn.commit()
            conn.close()
            return redirect("/")

@app.route('/delete')
def delete():
    id = request.args.get("id")
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    curs.execute('DELETE FROM attractions WHERE id = ?', id,)
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
