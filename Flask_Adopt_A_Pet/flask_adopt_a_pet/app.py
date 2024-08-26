# app.py
# Adopt a Pet project

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect("./data/database.db")
    curs =conn.cursor()
    pets = curs.execute("SELECT * FROM pets").fetchall()
    conn.close()

    return render_template("index.html", pets=pets)

@app.route('/view')
def view():
    id = request.args.get("id")

    conn = sqlite3.connect("./data/database.db")
    curs =conn.cursor()
    pet = curs.execute("SELECT * FROM pets WHERE id = ?", id).fetchone()
    conn.close()

    return render_template("view.html", pet=pet)

@app.route('/about')
def about():
    return render_template("about.html")
  
if __name__ == '__main__':
  app.run(debug=True)

