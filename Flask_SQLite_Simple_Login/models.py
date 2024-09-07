# models.py

from flask import session, flash, redirect, url_for
import sqlite3


def insertUser(username, password):
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    storedUsername = curs.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if storedUsername:
        session.pop('_flashes', None)
        flash("Username not available.")
        return redirect(url_for("index"))
    else:
        curs.execute("INSERT INTO users(username,password) VALUES(?,?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

def selectUsers():
    conn = sqlite3.connect("./data/database.db")
    curs = conn.cursor()
    users = curs.execute("SELECT * FROM users").fetchall()
    conn.close()
    return users
