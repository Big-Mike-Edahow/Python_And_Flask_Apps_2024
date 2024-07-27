# app.py
# Flask SQLite Grocery List.

# Import necessary python modules.
from flask import Flask, session, render_template, request, g
import sqlite3
import random

# Create an instance of the Flask App.
app = Flask(__name__)
app.config["SECRET_KEY"] = "Ice cream with the cherry on top."
app.config["SESSION_COOKIE_NAME"] = "XLR8-AA1689"

def get_db():
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    all_data = curs.execute("SELECT name FROM groceries;").fetchall()
    all_data = [str(val[0]) for val in all_data]
    shopping_list = all_data.copy()
    random.shuffle(shopping_list)
    shopping_list = shopping_list[:5]
    return all_data, shopping_list

@app.route("/", methods=["POST", "GET"])
def index():
    session["all_items"], session["shopping_items"] = get_db()
    return render_template(
        "index.html",
        all_items=session["all_items"],
        shopping_items=session["shopping_items"],
    )

@app.route("/add_items", methods=["post"])
def add_items():
    session["shopping_items"].append(request.form["select_items"])
    session.modified = True
    return render_template(
        "index.html",
        all_items=session["all_items"],
        shopping_items=session["shopping_items"],
    )

@app.route("/remove_items", methods=["post"])
def remove_items():
    checked_boxes = request.form.getlist("check")

    for item in checked_boxes:
        if item in session["shopping_items"]:
            idx = session["shopping_items"].index(item)
            session["shopping_items"].pop(idx)
            session.modified = True

    return render_template(
        "index.html",
        all_items=session["all_items"],
        shopping_items=session["shopping_items"],
    )

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
