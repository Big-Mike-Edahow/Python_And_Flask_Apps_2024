# app.py
# Flask Drones List App

# Import required modules.
from flask import Flask, render_template, url_for
import sqlite3

# Create an instance of the Flask app.
app = Flask(__name__)
app.config["SECRET_KEY"] = "I like my summer traditions."

@app.route('/')
def index():
    conn = sqlite3.connect('./data/database.db')
    curs = conn.cursor()
    drones = curs.execute("SELECT * FROM drones").fetchall()
    conn.close()

    return render_template('index.html', drones=drones)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

