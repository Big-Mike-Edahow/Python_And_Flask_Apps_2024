# app.py
# Flask SQLite Loveable Pets

from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("./data/database.db")
    curs =conn.cursor()
    pets = curs.execute("SELECT * FROM pets").fetchall()
    conn.close()
    return render_template("index.html", pets=pets)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

