# app.py
# Flask SQLite Markdown Notes

from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import markdown

def getDB():
    conn = sqlite3.connect("./data/database.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = "I thought I saw a tweety bird."

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        conn = getDB()
        curs = conn.cursor()
        db_notes = curs.execute("SELECT * FROM notes").fetchall()
        conn.close()
        notes = []
        for note in db_notes:
            note = dict(note)
            note['content'] = markdown.markdown(note['content'])
            notes.append(note)
        return render_template('index.html', notes=notes)
    elif request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))
        conn = getDB()
        curs = conn.cursor()
        curs.execute("INSERT INTO notes(content) VALUES(?)", (content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
@app.route("/delete/<int:id>")
def delete(id):
    conn = getDB()
    curs = conn.cursor()
    curs.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)

